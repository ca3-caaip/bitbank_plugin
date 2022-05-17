import json
from decimal import Decimal
from typing import Union
from unittest.mock import MagicMock

from senkalib.chain.bitbank.bitbank_transaction import BitbankTransaction

from bitbank_plugin.bitbank_plugin import BitbankPlugin


class TestBitbankPlugin:
    def test_can_handle_bitbank(self):
        test_data = TestBitbankPlugin._get_test_data(
            "tests/data/bitbank_sample_with_data_type.json", 0
        )
        transaction = BitbankTransaction(test_data)
        chain_type = BitbankPlugin.can_handle(transaction)
        assert chain_type

    def test_get_caajs_buy_lose(self):
        test_data = TestBitbankPlugin._get_test_data(
            "tests/data/bitbank_sample_with_data_type.json", 0
        )
        transaction = BitbankTransaction(test_data)
        mock = TestBitbankPlugin._get_token_table_mock()
        caajs = BitbankPlugin.get_caajs(transaction, mock)
        assert caajs[0].executed_at == "2022/03/14 11:55:24"
        assert caajs[0].chain == "bitbank"
        assert caajs[0].platform == "bitbank"
        assert caajs[0].application == "exchange"
        assert caajs[0].transaction_id == "1215140489"
        assert caajs[0].type == "lose"
        assert caajs[0].amount == Decimal("59577.0126674")
        assert caajs[0].token_symbol == "test_symbol"
        assert caajs[0].token_original_id == "jpy"
        assert caajs[0].caaj_from == "self"
        assert caajs[0].token_symbol_uuid == "3a2570c5-15c4-2860-52a8-bff14f27a236"
        assert caajs[0].caaj_to == "bitbank"
        assert caajs[0].comment == ""

    def test_get_caajs_buy_get(self):
        test_data = TestBitbankPlugin._get_test_data(
            "tests/data/bitbank_sample_with_data_type.json", 0
        )
        transaction = BitbankTransaction(test_data)
        mock = TestBitbankPlugin._get_token_table_mock()
        caajs = BitbankPlugin.get_caajs(transaction, mock)
        assert caajs[1].executed_at == "2022/03/14 11:55:24"
        assert caajs[1].chain == "bitbank"
        assert caajs[1].platform == "bitbank"
        assert caajs[1].application == "exchange"
        assert caajs[1].transaction_id == "1215140489"
        assert caajs[1].type == "get"
        assert caajs[1].amount == Decimal("537.8006")
        assert caajs[1].token_symbol == "test_symbol"
        assert caajs[1].token_original_id == "mona"
        assert caajs[1].caaj_from == "self"
        assert caajs[1].token_symbol_uuid == "3a2570c5-15c4-2860-52a8-bff14f27a236"
        assert caajs[1].caaj_to == "bitbank"
        assert caajs[1].comment == ""

    def test_get_caajs_sell_lose(self):
        test_data = TestBitbankPlugin._get_test_data(
            "tests/data/bitbank_sample_with_data_type.json", 1
        )
        transaction = BitbankTransaction(test_data)
        mock = TestBitbankPlugin._get_token_table_mock()
        caajs = BitbankPlugin.get_caajs(transaction, mock)
        assert caajs[0].executed_at == "2022/03/14 11:55:24"
        assert caajs[0].chain == "bitbank"
        assert caajs[0].platform == "bitbank"
        assert caajs[0].application == "exchange"
        assert caajs[0].transaction_id == "1215140486"
        assert caajs[0].type == "lose"
        assert caajs[0].amount == Decimal("537.8006")
        assert caajs[0].token_symbol == "test_symbol"
        assert caajs[0].token_original_id == "mona"
        assert caajs[0].caaj_from == "self"
        assert caajs[0].token_symbol_uuid == "3a2570c5-15c4-2860-52a8-bff14f27a236"
        assert caajs[0].caaj_to == "bitbank"
        assert caajs[0].comment == ""

    def test_get_caajs_sell_get(self):
        test_data = TestBitbankPlugin._get_test_data(
            "tests/data/bitbank_sample_with_data_type.json", 1
        )
        transaction = BitbankTransaction(test_data)
        mock = TestBitbankPlugin._get_token_table_mock()
        caajs = BitbankPlugin.get_caajs(transaction, mock)
        assert caajs[1].executed_at == "2022/03/14 11:55:24"
        assert caajs[1].chain == "bitbank"
        assert caajs[1].platform == "bitbank"
        assert caajs[1].application == "exchange"
        assert caajs[1].transaction_id == "1215140486"
        assert caajs[1].type == "get"
        assert caajs[1].amount == Decimal("59577.0126674")
        assert caajs[1].token_symbol == "test_symbol"
        assert caajs[1].token_original_id == "jpy"
        assert caajs[1].caaj_from == "self"
        assert caajs[1].token_symbol_uuid == "3a2570c5-15c4-2860-52a8-bff14f27a236"
        assert caajs[1].caaj_to == "bitbank"
        assert caajs[1].comment == ""

    @staticmethod
    def _get_test_data(filename: str, number: int = 0) -> Union[dict, list]:
        test_data = json.load(open(filename))[number]
        return test_data

    @classmethod
    def _get_token_table_mock(cls):
        def _mock_get_symbol(chain: str, token_original_id: str) -> Union[str, None]:
            return "test_symbol"

        def _mock_get_symbol_uuid(chain: str, token_original_id: str) -> str:
            return "3a2570c5-15c4-2860-52a8-bff14f27a236"

        mock = MagicMock()
        mock.get_symbol.side_effect = _mock_get_symbol
        mock.get_symbol_uuid.side_effect = _mock_get_symbol_uuid
        return mock
