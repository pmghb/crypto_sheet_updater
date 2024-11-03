# Crp sheet updater

## Description
This project allows to quickly update a token portfolio managed in an Apple Numbers or Microsoft Excel spreadsheet.

It takes a spreadsheet file as input, retrieves all the names of the tokens being tracked, contacts CoinMarketCap API to retrieve the latest prices and updates the spreadsheet file.

Configuration is done via the `csu_config.py` file. The documentation related to the variables can be consulted directly in the file, in the form of comments.

## Table of Contents
- [Prerequisites](#prerequisites)
- [Usage](#usage)

## Prerequisites
### Python 3
You will need a working Python 3 environment to run the script.
- For Windows or Mac, you can go to https://www.python.org/downloads/ to download and install it.
- For a Debian based Linux, you can run the following command lines:
    ```sh
    sudo apt update
    sudo apt install python3
    ```
### CoinMarketCap token
To access the CoinMarketCap API, you will need a personal token. To get one go to https://pro.coinmarketcap.com/signup/ , create an account and a personal token on Basic Plan.

### Spreadsheet format
In order for the script to read and edit the spreadsheet correctly, it must include:
- a named table to retrieve and update;
- a column with the token identifier (ex BTC). You can find identifiers on https://coinmarketcap.com with the research function;
- a column with the item price;
- an optional date column, if you wish to update the last update date (see date_col_index in config).

Your spreadsheet may contains multiple sheets, tables or columns in any order, this is not important because you can adapt the script parser via the configuration.

The repository contains two test files (test_sheet) that you can consult. They contain several tables for testing purposes, but only one is needed:\
<img src="sc_1_example.png" alt="Sheet example" width="400"/>

## Usage
Either download the project zip and extract it, or clone the repository via the command line, and open the project folder.
```sh
git clone https://github.com/pmghb/crp_sheet_updater.git
cd crp_sheet_updater
```

Open the file `csu_config.py` and adapt the configuration to match your spreadsheet file.

Before running the script, run the test module with the following command line:
```sh
python3 -m unittest -v tests.py
```

All tests should pass if your configuration is good:\
<img src="sc_2_log.png" alt="Success log" width="200"/>

If you have an error, check the logs to try to identify the problem. If this seems to be a bug, please create a ticket in the repository.

Otherwise, if all is well, you can run the main script:
```sh
python3 csu.py
```
You should now have the latest price of all your tokens.