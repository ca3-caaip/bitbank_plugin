import datetime
import uuid
from typing import Union

from senkalib.caaj_journal import CaajJournal
from senkalib.chain.transaction import Transaction
from senkalib.token_original_id_table import TokenOriginalIdTable


class BitbankPlugin:
    chain = "bitbank"
    platform = "bitbank"

    @classmethod
    def can_handle(cls, transaction: Transaction) -> bool:
        chain_type = transaction.get_transaction_data_type()
        return cls.chain in chain_type

    @classmethod
    def get_caajs(
        cls, transaction: Transaction, token_table: TokenOriginalIdTable
    ) -> Union[list, None]:
        caaj = []
        caaj_journal_lose = None
        caaj_journal_get = None
        caaj_journal_fee = None

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
                BitbankPlugin.chain, token_original_id_lose
            )
            symbol_uuid_lose = token_table.get_symbol_uuid(
                BitbankPlugin.chain, token_original_id_lose
            )
            token_symbol_get = token_table.get_symbol(
                BitbankPlugin.chain, token_original_id_get
            )
            symbol_uuid_get = token_table.get_symbol_uuid(
                BitbankPlugin.chain, token_original_id_get
            )

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

            caaj_journal_fee = CaajJournal(
                datetime_utc,
                cls.chain,
                cls.platform,
                "exchange",
                transaction.get_transaction_id(),
                trade_uuid,
                "lose",
                fee,
                token_symbol_lose,
                token_original_id_lose,
                symbol_uuid_lose,
                "self",
                "bitbank",
                "",
            )

        elif trade_type == "sell":
            token_original_id_get = token_pair[1]
            token_original_id_lose = token_pair[0]
            amount_lose = transaction.get_amount()
            amount_get = transaction.get_amount() * transaction.get_price()
            token_symbol_lose = token_table.get_symbol(
                BitbankPlugin.chain, token_original_id_lose
            )
            symbol_uuid_lose = token_table.get_symbol_uuid(
                BitbankPlugin.chain, token_original_id_lose
            )
            token_symbol_get = token_table.get_symbol(
                BitbankPlugin.chain, token_original_id_get
            )
            symbol_uuid_get = token_table.get_symbol_uuid(
                BitbankPlugin.chain, token_original_id_get
            )

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

            caaj_journal_fee = CaajJournal(
                datetime_utc,
                cls.chain,
                cls.platform,
                "exchange",
                transaction.get_transaction_id(),
                trade_uuid,
                "lose",
                fee,
                token_symbol_get,
                token_original_id_get,
                symbol_uuid_get,
                "self",
                "bitbank",
                "",
            )
        caaj.append(caaj_journal_lose)
        caaj.append(caaj_journal_get)
        caaj.append(caaj_journal_fee)

        return caaj

    @classmethod
    def _get_uuid(cls) -> str:
        return str(uuid.uuid4())
