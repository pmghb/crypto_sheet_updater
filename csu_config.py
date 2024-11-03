#!/usr/bin/env python3
"""Configuration file."""

class CSUConfig:
    doc = {
        # Spreadsheet type.
        # Supported values : numbers or excel.
        "type": "excel",

        # Path to the spreadsheet file that contains the coins names.
        "input_path": "test_sheet.xlsx",

        # Path to the spreadsheet file that will be updated with the new values.
        # You can use the same as input_path but formats may be altered or file broken.
        # If you are using the same file, make a save!
        "output_path": "test_sheet_update.xlsx"
    }

    sheet = {
        # Index of the sheet to use in the doc, between 0 and +n.
        "index": 0
    }

    table = {
        # Name of the table to use in the sheet. Respect case and whitespaces.
        "name": "table_1",

        # Index of the first row of data, rows before will be ignored. Index 0 is frequently the row title.
        # Between 0 and +n.
        "start_row_index": 1,

        # Parameter to use to ignore lines at the end of the table, for example the sum.
        # Specify a negative number corresponding to the number of lines in the table to ignore starting from the end.
        # Otherwise, set to 0.
        "end_row_index": 0,

        # Index of the table column that contains the coin name (BTC for Bitcoin) in the input file.
        # Between 0 and +n.
        "coin_name_col_index": 0,

        # Index of the table column that contains the coin price to be written in the output file.
        # Between 0 and +n.
        "coin_price_col_index": 3,

        # Index of the table column that contains an updated date to be written in the output file. If not used, set it to -1.
        # Between -1 and +n.
        "date_col_index": 2
    }

    cmc_api = {
        # URL of CoinMarketCap API. Should not be changed unless they update it.
        "url": "https://pro-api.coinmarketcap.com/v2/cryptocurrency/quotes/latest",

        # Your personnal token to access the API. Create an account on https://pro.coinmarketcap.com/ to get one.
        "token": "TOKEN"
    }
