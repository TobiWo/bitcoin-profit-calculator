from src.datafetcher import BitmexTradingHistoryFetcher
from src.datawriter import DataWriter
from src.datacalculator import DataCalculator
from src.apikeys import APIKeyLoader
from tqdm import tqdm
import os

key_loader = APIKeyLoader()
bitmex_keys: dict = key_loader.get_keys()

for dict_key, dict_value in bitmex_keys.items():
    for key, secret in dict_value.items():
        fetcher = BitmexTradingHistoryFetcher(key, secret)
        data_writer = DataWriter()

        year_to_fetch = 2019
        month_to_fetch = 8

        position_data, funding_data = fetcher.fetch_data_for_period(year_to_fetch, month_to_fetch)
        column_names = fetcher.get_response_keys() + fetcher.get_new_data_columns()

        data_calculator = DataCalculator()
        position_data_df = data_calculator.transform_json_list_to_dataframe(column_names, position_data)
        funding_data_df = data_calculator.transform_json_list_to_dataframe(column_names, funding_data)

        final_data_frame = data_calculator.calculate_taxes(position_data_df, funding_data_df, 'realised_profit_or_loss_in_usd', 0.263750, 601.00)

        data_writer.write_final_data_frame(final_data_frame, year_to_fetch, month_to_fetch)
        data_writer.write_funding_data(column_names, funding_data, year_to_fetch, month_to_fetch)
        data_writer.write_position_data(column_names, position_data, year_to_fetch, month_to_fetch)