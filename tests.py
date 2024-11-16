#!/usr/bin/env python3
"""Testing module for csu.py"""

import unittest

from csu_types import Config, CSUConfig, SheetType, Coin
from csu_helpers import round_float
from csu import load_numbers_doc, load_excel_doc, prepare_dataset, get_data_from_cmc_api, update_numbers_sheet, update_excel_sheet

class CSUNumbersConfigTest:
    """Mock of the real config (csu_config.py) with test values for Numbers."""
    doc = {
        "type": "numbers",
        "input_path": "test_sheet.numbers",
        "output_path": "test_sheet_update.numbers"
    }

    sheet = {
        "index": 0
    }

    table = {
        "name": "Table 1",
        "start_row_index": 1,
        "end_row_index": 0,
        "coin_name_col_index": 0,
        "coin_price_col_index": 3,
        "date_col_index": 2
    }

    cmc_api = {
        "url": "https://pro-api.coinmarketcap.com/v2/cryptocurrency/quotes/latest",
        "token": "token1"
    }

class CSUExcelConfigTest:
    """Mock of the real config (csu_config.py) with test values for Excel."""
    doc = {
        "type": "excel",
        "input_path": "test_sheet.xlsx",
        "output_path": "test_sheet_update.xlsx"
    }

    sheet = {
        "index": 0
    }

    table = {
        "name": "table_1",
        "start_row_index": 1,
        "end_row_index": 0,
        "coin_name_col_index": 0,
        "coin_price_col_index": 3,
        "date_col_index": 2
    }

    cmc_api = {
        "url": "https://pro-api.coinmarketcap.com/v2/cryptocurrency/quotes/latest",
        "token": "token1"
    }

class ConfigTests(unittest.TestCase):
    """Tests of configuration functions and types."""
    def test_init_good_config(self):
        """Tries to init a valid configuration. Should return a valid Config object."""
        config = Config(CSUNumbersConfigTest())
        self.assertEqual(config.sheet_type, SheetType.NUMBERS)
        self.assertEqual(config.input_path,"test_sheet.numbers")
        self.assertEqual(config.output_path, "test_sheet_update.numbers")
        self.assertEqual(config.sheet_index, 0)
        self.assertEqual(config.table_name, "Table 1")
        self.assertEqual(config.table_start_row_index, 1)
        self.assertEqual(config.table_end_row_index, 0)
        self.assertEqual(config.cmc_api_url, "https://pro-api.coinmarketcap.com/v2/cryptocurrency/quotes/latest")
        self.assertEqual(config.cmc_api_token, "token1")
        self.assertEqual(config.table_coin_name_col_index, 0)
        self.assertEqual(config.table_coin_price_col_index, 3)
        self.assertEqual(config.table_date_col_index, 2)

    def test_init_bad_sheet_type(self):
        """Tries to init an invalid type in configuration. Execution should stops."""
        pre_config = CSUNumbersConfigTest()
        pre_config.doc["type"] = "fail"

        with self.assertRaises(SystemExit) as log:
            Config(pre_config)

        self.assertEqual(str(log.exception), "Unsupported sheet type 'fail'. Choose between numbers or excel types.")
        pre_config.doc["type"] = "numbers" # Reset to a good value for the next tests.

class DataTestsWithoutSum(unittest.TestCase):
    """Tests for data management from a table with title and no end sum line."""
    config_nu = Config(CSUNumbersConfigTest())
    numbers_doc = load_numbers_doc(config_nu)

    config_ex = Config(CSUExcelConfigTest())
    excel_doc = load_excel_doc(config_ex)

    def test_load_numbers_data(self):
        """Tries to retireve data from Numbers file."""
        self.assertEqual(self.numbers_doc.rows[1][self.config_nu.table_coin_name_col_index].value, "BTC")
        self.assertEqual(self.numbers_doc.rows[1][self.config_nu.table_coin_price_col_index].value, 68000)
        self.assertEqual(self.numbers_doc.rows[2][self.config_nu.table_coin_name_col_index].value, "ETH")
        self.assertEqual(self.numbers_doc.rows[2][self.config_nu.table_coin_price_col_index].value, 2500)
        self.assertEqual(self.numbers_doc.rows[3][self.config_nu.table_coin_name_col_index].value, "SOL")
        self.assertEqual(self.numbers_doc.rows[3][self.config_nu.table_coin_price_col_index].value, 160)


    def test_load_excel_data(self):
        """Tries to retireve data from Excel file."""
        self.assertEqual(self.excel_doc.rows[1][self.config_ex.table_coin_name_col_index], "BTC")
        self.assertEqual(self.excel_doc.rows[1][self.config_ex.table_coin_price_col_index], 68000)
        self.assertEqual(self.excel_doc.rows[2][self.config_ex.table_coin_name_col_index], "ETH")
        self.assertEqual(self.excel_doc.rows[2][self.config_ex.table_coin_price_col_index], 2500)
        self.assertEqual(self.excel_doc.rows[3][self.config_ex.table_coin_name_col_index], "SOL")
        self.assertEqual(self.excel_doc.rows[3][self.config_ex.table_coin_price_col_index], 160)

    def test_prepare_numbers_dataset_without_sum(self):
        """Tries to format data to send to CoinMarketCap API."""
        data = prepare_dataset(self.numbers_doc, self.config_nu)
        self.assertEqual(data, ["BTC,ETH,SOL"])

    def test_prepare_excel_dataset_without_sum(self):
        """Tries to format data to send to CoinMarketCap API."""
        data = prepare_dataset(self.excel_doc, self.config_ex)
        self.assertEqual(data, ["BTC,ETH,SOL"])

    def test_ecxeed_max_token_limit_dataset_without_sum(self):
        """Method should returns multiple string."""

        excel_doc_tmp = load_excel_doc(self.config_ex)
        control_list = ["BTC,ETH,SOL"]

        l = []
        i = 1
        while i <= 98:
            # Append 98 rows for a total of 101 with the 3 first.
            excel_doc_tmp.rows.append(excel_doc_tmp.rows[1])

            if i < 98:
                # Append 97 tokens for a total of 100 with the 3 first.
                l.append(",BTC")

            i += 1

        control_list[0] = ''.join([control_list[0], ''.join(l)])

        # Append 1 token in a second list.
        control_list.append("BTC")

        data = prepare_dataset(excel_doc_tmp, self.config_ex)
        self.assertEqual(data, control_list)

class DataTestsWithSum(unittest.TestCase):
    """Tests for data management from a table with title and an end sum line."""
    config_nu = Config(CSUNumbersConfigTest())
    config_nu.table_name = "Table 2"
    config_nu.table_end_row_index = -1
    numbers_doc = load_numbers_doc(config_nu)

    config_ex = Config(CSUExcelConfigTest())
    config_ex.table_name = "table_2"
    config_ex.table_end_row_index = -1
    excel_doc = load_excel_doc(config_ex)

    def test_load_numbers_data(self):
        """Tries to retrieve data from Numbers file."""
        self.assertEqual(self.numbers_doc.rows[1][self.config_nu.table_coin_name_col_index].value, "BTC")
        self.assertEqual(self.numbers_doc.rows[1][self.config_nu.table_coin_price_col_index].value, 68000)
        self.assertEqual(self.numbers_doc.rows[2][self.config_nu.table_coin_name_col_index].value, "ETH")
        self.assertEqual(self.numbers_doc.rows[2][self.config_nu.table_coin_price_col_index].value, 2500)
        self.assertEqual(self.numbers_doc.rows[3][self.config_nu.table_coin_name_col_index].value, "SOL")
        self.assertEqual(self.numbers_doc.rows[3][self.config_nu.table_coin_price_col_index].value, 160)
        self.assertEqual(self.numbers_doc.rows[4][self.config_nu.table_coin_name_col_index].value, "TOTAL")
        self.assertEqual(self.numbers_doc.rows[4][self.config_nu.table_coin_price_col_index].value, 70660)

    def test_prepare_numbers_dataset_with_sum(self):
        """Tries to format data to send to CoinMarketCap API."""
        data = prepare_dataset(self.numbers_doc, self.config_nu)
        self.assertEqual(data, ["BTC,ETH,SOL"])

    def test_prepare_excel_dataset_with_sum(self):
        """Tries to format data to send to CoinMarketCap API."""
        data = prepare_dataset(self.excel_doc, self.config_ex)
        self.assertEqual(data, ["BTC,ETH,SOL"])

class CMCAPITests(unittest.TestCase):
    """Tests for Coin Market Cap Api."""
    def test_get_valid_data_from_cmc_api(self):
        """Tries to get valid data from CoinMarketCap API."""
        token_set = "BTC,ETH,SOL"
        config = Config(CSUConfig())

        coins = get_data_from_cmc_api(token_set, config)

        self.assertEqual(coins[0].name, "BTC")
        self.assertGreater(coins[0].price, 0)
        self.assertEqual(coins[1].name, "ETH")
        self.assertGreater(coins[1].price, 0)
        self.assertEqual(coins[2].name, "SOL")
        self.assertGreater(coins[2].price, 0)

    def test_get_valid_data_and_order_from_cmc_api(self):
        """Tries to get valid data and check that order is conserved from CoinMarketCap API."""
        token_set = "BTC,SOL,ETH"
        config = Config(CSUConfig())

        coins = get_data_from_cmc_api(token_set, config)

        self.assertEqual(coins[0].name, "BTC")
        self.assertGreater(coins[0].price, 0)
        self.assertEqual(coins[1].name, "SOL")
        self.assertGreater(coins[1].price, 0)
        self.assertEqual(coins[2].name, "ETH")
        self.assertGreater(coins[2].price, 0)

    def test_get_invalid_data_from_cmc_api(self):
        """Tries to send a bad coin to CoinMarketCap API."""
        token_set = "BTC,ETH,TOTOZ"
        config = Config(CSUConfig())

        coins = get_data_from_cmc_api(token_set, config)

        self.assertEqual(coins[0].name, "BTC")
        self.assertGreater(coins[0].price, 0)
        self.assertEqual(coins[1].name, "ETH")
        self.assertGreater(coins[1].price, 0)
        self.assertEqual(coins[2].name, "TOTOZ")
        self.assertEqual(coins[2].price, 0)

    def test_contact_bad_url(self):
        """Contacts bad URLs. Execution should stops."""
        config = Config(CSUConfig())

        config.cmc_api_url = "false"
        with self.assertRaises(SystemExit) as log:
            get_data_from_cmc_api("", config)
        print(str(log.exception))

        config.cmc_api_url = "https://pro-api.coinmarketcap.com/v2/quotes/latest"
        with self.assertRaises(SystemExit) as log:
            get_data_from_cmc_api("", config)
        print(str(log.exception))

    def test_send_invalid_token_to_cmc_api(self):
        """Tries to send a bad token to CoinMarketCap API. Execution should stops."""
        config = Config(CSUConfig())
        config.cmc_api_token = "false"

        with self.assertRaises(SystemExit):
            get_data_from_cmc_api("", config)

    def test_update_numbers_sheet(self):
        """Tries to write a Numbers sheet and read it to check data."""
        config_test_nu = Config(CSUNumbersConfigTest())

        # Load testing doc and prepare dataset
        numbers_doc = load_numbers_doc(config_test_nu)

        coins = [Coin(numbers_doc.rows[1][0].value, 100000000000000000),
                 Coin(numbers_doc.rows[2][0].value, 7.56),
                 Coin(numbers_doc.rows[3][0].value, 0.27)]
        update_numbers_sheet(numbers_doc, coins, config_test_nu)

        # Reload data from updated doc
        config_test_nu.input_path = config_test_nu.output_path
        numbers_doc = load_numbers_doc(config_test_nu)

        self.assertEqual(numbers_doc.rows[1][config_test_nu.table_coin_price_col_index].value, coins[0].price)
        self.assertEqual(numbers_doc.rows[2][config_test_nu.table_coin_price_col_index].value, coins[1].price)
        self.assertEqual(numbers_doc.rows[3][config_test_nu.table_coin_price_col_index].value, coins[2].price)

    def test_update_excel_sheet(self):
        """Tries to write an Excel sheet and read it to check data."""
        config_test_ex = Config(CSUExcelConfigTest())

        # Load testing doc and prepare dataset
        excel_doc = load_excel_doc(config_test_ex)

        # Retrieve data from CMC API and write doc
        coins = [Coin(excel_doc.rows[1][0], 100000000000000000),
                 Coin(excel_doc.rows[2][0], 7.56),
                 Coin(excel_doc.rows[3][0], 0.27)]
        update_excel_sheet(excel_doc, coins, config_test_ex)

        # Reload data from updated doc
        config_test_ex.input_path = config_test_ex.output_path
        excel_doc = load_excel_doc(config_test_ex)

        self.assertEqual(excel_doc.rows[1][config_test_ex.table_coin_price_col_index], coins[0].price)
        self.assertEqual(excel_doc.rows[2][config_test_ex.table_coin_price_col_index], coins[1].price)
        self.assertEqual(excel_doc.rows[3][config_test_ex.table_coin_price_col_index], coins[2].price)

class HelpersTests(unittest.TestCase):
    """Tests for csu_helpers module."""
    def test_round_float(self):
        """Tries different values with the round_float function."""
        self.assertEqual(round_float(None), 0)
        self.assertEqual(round_float(0), 0)
        self.assertEqual(round_float(0.1), 0.10)
        self.assertEqual(round_float(0.10), 0.10)
        self.assertEqual(round_float(0.155), 0.15)
        self.assertEqual(round_float(0.157), 0.16)
        self.assertEqual(round_float(0.0157), 0.016)
        self.assertEqual(round_float(0.000000000001856), 0.0000000000019)
        self.assertEqual(round_float(1), 1)
        self.assertEqual(round_float(1.000000000001856), 1.0000000000019)
        self.assertEqual(round_float(10), 10)
        self.assertEqual(round_float(100000), 100000)
        self.assertEqual(round_float(1000000000000005), 1000000000000005)

if __name__ == "__main__":
    unittest.main()
