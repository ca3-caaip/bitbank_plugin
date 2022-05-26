import datetime
import uuid
from decimal import Decimal
from enum import Enum, auto
from typing import List, Union

from senkalib.caaj_journal import CaajJournal
from senkalib.chain.transaction import Transaction
from senkalib.token_original_id_table import TokenOriginalIdTable

CHAIN_FROM_ORIGINAL_ID = {"mona": "monacoin", "jpy": "boj"}


class BitbankSupport(Enum):
    EXCHANGE = auto()
    UNSUPPORTED = auto()


class BitbankPlugin:
    chain = "bitbank"
    platform = "bitbank"

    @classmethod
    def can_handle(cls, transaction: Transaction) -> bool:
        return BitbankPlugin._check_support(transaction) == BitbankSupport.EXCHANGE

    @classmethod
    def get_caajs(
        cls, address: str, transaction: Transaction, token_table: TokenOriginalIdTable
    ) -> Union[List[CaajJournal], None]:
        if BitbankPlugin._check_support(transaction) == BitbankSupport.EXCHANGE:
            return BitbankPlugin._get_caaj_exchange(transaction, token_table)
        else:
            raise ValueError("Invalid transaction data type")

    @classmethod
    def _get_caaj_exchange(
        cls, transaction: Transaction, token_table: TokenOriginalIdTable
    ) -> Union[List[CaajJournal], None]:
        caaj = []
        amount_lose = Decimal(0)
        amount_get = Decimal(0)
        token_original_id_lose = ""
        token_original_id_get = ""
        token_original_id_fee = ""
        symbol_uuid_lose = ""
        symbol_uuid_get = ""
        symbol_uuid_fee = ""
        token_symbol_lose = ""
        token_symbol_get = ""
        token_symbol_fee = ""

        datetime_jst = datetime.datetime.strptime(
            transaction.get_timestamp(), "%Y/%m/%d %H:%M:%S"
        )
        datetime_utc = (datetime_jst - datetime.timedelta(hours=9)).strftime(
            "%Y/%m/%d %H:%M:%S%z"
        )
        token_pair = transaction.get_token_pair().split("_")
        trade_uuid = cls._get_uuid()
        fee = transaction.get_transaction_fee()

        trade_type = transaction.get_trade_type()
        if trade_type == "buy":
            token_original_id_get = token_pair[0]
            token_original_id_lose = token_pair[1]
            amount_get = transaction.get_amount()
            amount_lose = transaction.get_amount() * transaction.get_price()
            token_symbol_lose = token_table.get_symbol(
                CHAIN_FROM_ORIGINAL_ID[token_original_id_lose], token_original_id_lose
            )
            symbol_uuid_lose = token_table.get_symbol_uuid(
                CHAIN_FROM_ORIGINAL_ID[token_original_id_lose], token_original_id_lose
            )
            token_symbol_get = token_table.get_symbol(
                CHAIN_FROM_ORIGINAL_ID[token_original_id_get], token_original_id_get
            )
            symbol_uuid_get = token_table.get_symbol_uuid(
                CHAIN_FROM_ORIGINAL_ID[token_original_id_get], token_original_id_get
            )
            token_symbol_fee = token_symbol_lose
            token_original_id_fee = token_original_id_lose
            symbol_uuid_fee = symbol_uuid_lose

        elif trade_type == "sell":
            token_original_id_get = token_pair[1]
            token_original_id_lose = token_pair[0]
            amount_lose = transaction.get_amount()
            amount_get = transaction.get_amount() * transaction.get_price()
            token_symbol_lose = token_table.get_symbol(
                CHAIN_FROM_ORIGINAL_ID[token_original_id_lose], token_original_id_lose
            )
            symbol_uuid_lose = token_table.get_symbol_uuid(
                CHAIN_FROM_ORIGINAL_ID[token_original_id_lose], token_original_id_lose
            )
            token_symbol_get = token_table.get_symbol(
                CHAIN_FROM_ORIGINAL_ID[token_original_id_get], token_original_id_get
            )
            symbol_uuid_get = token_table.get_symbol_uuid(
                CHAIN_FROM_ORIGINAL_ID[token_original_id_get], token_original_id_get
            )
            token_symbol_fee = token_symbol_get
            token_original_id_fee = token_original_id_get
            symbol_uuid_fee = symbol_uuid_get

        caaj_journal_lose = CaajJournal(
            datetime_utc,
            cls.chain,
            cls.platform,
            "exchange",
            transaction.get_transaction_id(),
            trade_uuid,
            "lose",
            amount_lose,
            token_symbol_lose,
            token_original_id_lose,
            symbol_uuid_lose,
            "self",
            "bitbank",
            "",
        )

        caaj_journal_get = CaajJournal(
            datetime_utc,
            cls.chain,
            cls.platform,
            "exchange",
            transaction.get_transaction_id(),
            trade_uuid,
            "get",
            amount_get,
            token_symbol_get,
            token_original_id_get,
            symbol_uuid_get,
            "self",
            "bitbank",
            "",
        )

        caaj.append(caaj_journal_lose)
        caaj.append(caaj_journal_get)

        if fee > Decimal(0):
            caaj_journal_fee = CaajJournal(
                datetime_utc,
                cls.chain,
                cls.platform,
                "exchange",
                transaction.get_transaction_id(),
                trade_uuid,
                "lose",
                fee,
                token_symbol_fee,
                token_original_id_fee,
                symbol_uuid_fee,
                "self",
                "bitbank",
                "",
            )
            caaj.append(caaj_journal_fee)

        return caaj

    @classmethod
    def _get_uuid(cls) -> str:
        return str(uuid.uuid4())

    @staticmethod
    def _check_support(transaction: Transaction) -> BitbankSupport:
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
                "data_type",
            ]
        ):
            return BitbankSupport.EXCHANGE
        else:
            return BitbankSupport.UNSUPPORTED
