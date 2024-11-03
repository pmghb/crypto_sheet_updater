#!/usr/bin/env python3
"""Module that contains types used in main module."""

import sys
from enum import Enum

import numbers_parser
import openpyxl
import openpyxl.cell
import openpyxl.workbook
import openpyxl.worksheet
import openpyxl.worksheet.table
import openpyxl.worksheet.worksheet

from csu_config import CSUConfig

class SheetType(Enum):
    """Enum from an str type."""
    NUMBERS = 1
    EXCEL = 2

class NumbersDoc:
    """Stores a numbers document."""
    doc: numbers_parser.Document
    sheets: list[numbers_parser.Sheet]
    table: numbers_parser.Table
    rows: list[list[numbers_parser.Cell]]

    def __init__(self, doc, sheets, table, rows):
        self.doc = doc
        self.sheets = sheets
        self.table = table
        self.rows = rows

class ExcelDoc:
    """Stores an excel document."""
    doc: openpyxl.workbook
    sheets: list[openpyxl.worksheet.worksheet.Worksheet]
    table: openpyxl.worksheet.table.Table
    rows: list[list[openpyxl.cell.Cell]]

    def __init__(self, doc, sheets, table, rows):
        self.doc = doc
        self.sheets = sheets
        self.table = table
        self.rows = rows

class Coin:
    """Stores values retrieved from CMC API."""
    name: str
    price: float

    def __init__(self, name: str, price: float):
        self.name = name
        self.price = price

class Config:
    """Checks and stores config parameters."""
    def __init__(self, config: CSUConfig):

        sheet_type = config.doc["type"]
        if sheet_type == "numbers":
            self.sheet_type = SheetType.NUMBERS
        elif sheet_type == "excel":
            self.sheet_type = SheetType.EXCEL
        else:
            sys.exit(f"Unsupported sheet type '{sheet_type}'. Choose between numbers or excel types.")

        self.input_path = config.doc["input_path"]
        if not self.input_path:
            sys.exit("input_path is empty.")

        self.output_path = config.doc["output_path"]
        if not self.output_path:
            sys.exit("output_path is empty.")

        self.sheet_index = config.sheet["index"]
        if self.sheet_index < 0:
            sys.exit("sheet_index cannot be inferior to O.")

        self.table_name = config.table["name"]
        if not self.table_name:
            sys.exit("table_name cannot be empty.")

        self.table_start_row_index = config.table["start_row_index"]
        if self.table_start_row_index < 0:
            sys.exit("table_start_row_index cannot be inferior to O.")

        self.table_end_row_index = config.table["end_row_index"]
        if self.table_end_row_index > 0:
            sys.exit("table_end_row_index cannot be superior to O.")

        self.table_coin_name_col_index = config.table["coin_name_col_index"]
        if self.table_coin_name_col_index < 0:
            sys.exit("table_coin_name_col_index cannot be inferior to O.")

        self.table_coin_price_col_index = config.table["coin_price_col_index"]
        if self.table_coin_price_col_index < 0:
            sys.exit("table_coin_price_col_index cannot be inferior to O.")

        self.table_date_col_index = config.table["date_col_index"]
        if self.table_coin_price_col_index < -1:
            sys.exit("table_coin_price_col_index cannot be inferior to -1.")

        self.cmc_api_url = config.cmc_api["url"]
        if not self.input_path:
            sys.exit("cmc_api_url is empty.")

        self.cmc_api_token = config.cmc_api["token"]
        if not self.input_path:
            sys.exit("cmc_api_token is empty.")
