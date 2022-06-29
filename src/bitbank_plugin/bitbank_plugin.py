import datetime
import uuid
from decimal import Decimal
from enum import Enum, auto
from typing import Union

from dateutil.parser import parse
from senkalib.caaj_journal import CaajJournal
from senkalib.platform.transaction import Transaction
from senkalib.token_original_id_table import TokenOriginalIdTable


class BitbankSupport(Enum):
    EXCHANGE = auto()
    UNSUPPORTED = auto()


class BitbankPlugin:
    platform = "bitbank"
    application = "bitbank"

    @classmethod
    def can_handle(cls, transaction: Transaction) -> bool:
        return (
            BitbankPlugin._get_transaction_type(transaction)
            != BitbankSupport.UNSUPPORTED
        )

    @classmethod
    def get_caajs(
        cls, address: str, transaction: Transaction, token_table: TokenOriginalIdTable
    ) -> Union[list[CaajJournal], None]:
        if BitbankPlugin._get_transaction_type(transaction) == BitbankSupport.EXCHANGE:
            return BitbankPlugin._get_caaj_exchange(transaction, token_table)
        else:
            raise ValueError("Invalid transaction data type")

    @classmethod
    def _get_caaj_exchange(
        cls, transaction: Transaction, token_table: TokenOriginalIdTable
    ) -> list[CaajJournal]:
        caaj = []
        amount_lose = Decimal(0)
        amount_get = Decimal(0)
        token_original_id_lose = ""
        token_original_id_get = ""
        uti_lose = ""
        uti_get = ""
        uti_fee = ""

        datetime_jst = parse(transaction.get_timestamp())
        datetime_utc = (datetime_jst - datetime.timedelta(hours=9)).strftime(
            "%Y-%m-%d %H:%M:%S%z"
        )
        token_pair = transaction.get_token_pair().split("_")
        trade_uuid = str(uuid.uuid4())
        fee = transaction.get_transaction_fee()

        trade_type = transaction.get_side()
        if trade_type == "buy":
            token_original_id_get = token_pair[0]
            token_original_id_lose = token_pair[1]
            amount_get = transaction.get_amount()
            amount_lose = transaction.get_amount() * transaction.get_price()
            uti_lose = token_table.get_uti(
                BitbankPlugin.platform,
                token_original_id_lose,
            )

            uti_get = token_table.get_uti(
                BitbankPlugin.platform,
                token_original_id_get,
            )
            uti_fee = uti_lose

        elif trade_type == "sell":
            token_original_id_get = token_pair[1]
            token_original_id_lose = token_pair[0]
            amount_lose = transaction.get_amount()
            amount_get = transaction.get_amount() * transaction.get_price()
            uti_lose = token_table.get_uti(
                BitbankPlugin.platform,
                token_original_id_lose,
            )

            uti_get = token_table.get_uti(
                BitbankPlugin.platform,
                token_original_id_get,
            )

            uti_fee = uti_get

        caaj_journal_lose = CaajJournal(
            datetime_utc,
            cls.platform,
            cls.application,
            "exchange",
            transaction.get_transaction_id(),
            trade_uuid,
            "lose",
            amount_lose,
            uti_lose,
            "self",
            "bitbank",
            "",
        )

        caaj_journal_get = CaajJournal(
            datetime_utc,
            cls.platform,
            cls.application,
            "exchange",
            transaction.get_transaction_id(),
            trade_uuid,
            "get",
            amount_get,
            uti_get,
            "self",
            "bitbank",
            "",
        )

        caaj.append(caaj_journal_lose)
        caaj.append(caaj_journal_get)

        if fee > Decimal(0):
            caaj_journal_fee = CaajJournal(
                datetime_utc,
                cls.platform,
                cls.application,
                "exchange",
                transaction.get_transaction_id(),
                trade_uuid,
                "lose",
                fee,
                uti_fee,
                "self",
                "bitbank",
                "",
            )
            caaj.append(caaj_journal_fee)

        return caaj

    @staticmethod
    def _get_transaction_type(transaction: Transaction) -> BitbankSupport:
        if transaction.transaction.keys() == set(
            [
                "注文ID",
                "取引ID",
                "通貨ペア",
                "タイプ",
                "売/買",
                "数量",
                "価格",
                "手数料",
                "M/T",
                "取引日時",
            ]
        ):
            return BitbankSupport.EXCHANGE
        else:
            return BitbankSupport.UNSUPPORTED
