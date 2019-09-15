from src.datafetcher import BitmexTradingHistoryFetcher
from src.datawriter import DataWriter
from src.datacalculator import DataCalculator
from src.apikeys import APIKeyLoader
from tqdm import tqdm
import os
import argparse
import sys

api_keys_path: str = os.path.abspath(os.path.join(os.path.dirname( __file__ ), 'resources', 'api_keys.json'))

parser = argparse.ArgumentParser()
parser.add_argument("-k", "--keys", type=str, help="Path to api-keys. Default path is <project_dir>/resources/api_keys.json", action="store", default=api_keys_path)
parser.add_argument("-y", "--year", type=int, help="Fetch data for defined year", action="store", default=None)
parser.add_argument("-m", "--month", type=int, help="Fetch data for defined month", action="store", default=None)
parser.add_argument("-t", "--tax_rate", type=float, help="Tax rate specified as fraction of one: 0.x", action="store", default=None)
parser.add_argument("-l", "--tax_limit", type=float, help="Limit until no taxes are calculated", action="store", default=None)
args = parser.parse_args()

if (args.year is None):
    print("Flag -y or --year is mandatory. Please define a year for which data should be fetched!")
    sys.exit()
else:
    final_fetch_parameter_string = "You defined the following parameters: \n" \
        "Paths of api-key: {0}\n" \
        "Year: {1}\n" \
        "Month: {2}\n" \
        "Tax rate: {3}\n" \
        "Tax limit: {4}" 
    print(final_fetch_parameter_string.format(args.keys, args.year, args.month, args.tax_rate, args.tax_limit))
    confirmation = input("Please confirm with 'y' or reject with 'n': ")
    if (confirmation.lower() != "y"):
        sys.exit("You rejected your input or typed a not allowed character!\nPlease try again")
    else:
        start_main(args.keys, args.year, args.month, args.tax_rate, args.tax_limit)

def start_main(path_to_api_keys: str, year_to_fetch: int, month_to_fetch: int, tax_rate: float, tax_limit: float):
    key_loader = APIKeyLoader(path_to_api_keys)
    bitmex_keys: dict = key_loader.get_keys()

    for dict_key, dict_value in bitmex_keys.items():
        for key, secret in dict_value.items():
            fetcher = BitmexTradingHistoryFetcher(key, secret)
            data_writer = DataWriter()
            position_data, funding_data = fetcher.fetch_data_for_period(year_to_fetch, month_to_fetch)
            column_names = fetcher.get_response_keys() + fetcher.get_new_data_columns()

            data_calculator = DataCalculator()
            position_data_df = data_calculator.transform_json_list_to_dataframe(column_names, position_data)
            funding_data_df = data_calculator.transform_json_list_to_dataframe(column_names, funding_data)

            final_data_frame = data_calculator.calculate_taxes(position_data_df, funding_data_df, 'realised_profit_or_loss_in_usd', tax_rate, tax_limit)

            data_writer.write_final_data_frame(final_data_frame, year_to_fetch, month_to_fetch)
            data_writer.write_funding_data(column_names, funding_data, year_to_fetch, month_to_fetch)
            data_writer.write_position_data(column_names, position_data, year_to_fetch, month_to_fetch)