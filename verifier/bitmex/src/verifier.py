import os
from datetime import datetime
from datetime import time
from datetime import timedelta
import sys

class BitmexVerifier:
    
    bitmex_wallet_file_pattern: str = "Wallet History"
    fundings_file_pattern: str = "fundings"
    positions_file_pattern: str = "positions"

    bitmex_wallet_file: str = None
    fundings_file: str = None
    positions_file: str = None

    def __init__(self):
        self.resource_path: str = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'resources'))
        self._set_data_file_paths()
        self._check_file_initialisation()

    def _set_data_file_paths(self):
        data_files: list = [ os.path.join(self.resource_path, f) for f in os.listdir(self.resource_path) ]
        if (len(data_files) != 3):
            print("More than three files detected in resource folder.\nBe sure that only the files you want to compare are present in this directory.\nSee the applications ReadMe for further description.")
            sys.exit()
        for resource_file in data_files:
            if (self.bitmex_wallet_file_pattern in resource_file):
                self.bitmex_wallet_file = resource_file
            elif (self.fundings_file_pattern in resource_file):
                self.fundings_file = resource_file
            elif (self.positions_file_pattern in resource_file):
                self.positions_file = resource_file

    def _check_file_initialisation(self):
        if (self.bitmex_wallet_file is None):
            print("No wallet file from bitmex present or file was renamed!")
        if (self.fundings_file is None):
            print("No fundings file from application output present or file was renamed!")
        if (self.positions_file is None):
            print("No positions file from application output present or file was renamed!")

    def _get_trade_chunks(self, final_raw_data: list) -> list:
        all_trades = list()
        chunk = list()
        for index, item in enumerate(final_raw_data):
            if (len(chunk) == 0):
                lower_datetime_border, upper_datetime_border = self._get_upper_and_lower_datetime_border(item[0])
            elif (len(chunk) == 1 and final_raw_data[index-1] == chunk[0]):
                item_datetime = final_raw_data[index-1][0]
                lower_datetime_border, upper_datetime_border = self._get_upper_and_lower_datetime_border(item_datetime)
            current_item_datetime = item[0]
            if (current_item_datetime > lower_datetime_border and current_item_datetime < upper_datetime_border):
                chunk.append(item)
                if (item == final_raw_data[-1]):
                    all_trades.append(chunk)
            else:
                all_trades.append(chunk)
                chunk = list()
                chunk.append(item)
        return all_trades

    def _get_upper_and_lower_datetime_border(self, item_datetime: datetime) -> (datetime, datetime):
        trade_border_time = time(12,0,0,0)
        if (item_datetime.time() > trade_border_time):
            upper_datetime_border = item_datetime + timedelta(days=1)
            upper_datetime_border = upper_datetime_border.replace(hour=12, minute=0, second=0, microsecond=0)
            lower_datetime_border = item_datetime
            lower_datetime_border = lower_datetime_border.replace(hour=12, minute=0, second=0, microsecond=0)
        else:
            lower_datetime_border = item_datetime - timedelta(days=1)
            lower_datetime_border = lower_datetime_border.replace(hour=12, minute=0, second=0, microsecond=0)
            upper_datetime_border = item_datetime
            upper_datetime_border = upper_datetime_border.replace(hour=12, minute=0, second=0, microsecond=0)
        return lower_datetime_border, upper_datetime_border

    def _modify_wallet_line(self, line: str) -> list:
        raw_line: list = line.split(",")
        cleaned_line: list = [ item.strip("\"").strip(" ") for item in raw_line ]
        if (cleaned_line[2] == 'RealisedPNL'):
            trade_date: datetime = datetime.strptime(cleaned_line[0], '%d.%m.%Y')
            flattened_line = list()
            flattened_line.append(trade_date.date())
            flattened_line.append(int(cleaned_line[3]))
            return flattened_line

    def _get_datetime_from_list(self, list_item: list) -> datetime:
        return list_item[0]

    def _modify_pos_line(self, line: str) -> list:
        modified_line: list = list()
        raw_line = line.rstrip("\n").split(";")
        date = datetime.strptime(raw_line[0], '%Y-%m-%dT%H:%M:%S.%fZ')
        modified_line.append(date)
        modified_line.append(int(raw_line[6]))
        return modified_line

    def _get_correct_timestamp(self, trade_chunk: list) -> datetime:
        threshold_time = time(12,0,0,0)
        first_chunk_part: list = trade_chunk[0]
        time_of_chunk = first_chunk_part[0].time()
        if (time_of_chunk > threshold_time):
            return first_chunk_part[0].date() + timedelta(days=1)
        else:
            return first_chunk_part[0].date()

    def _add_correct_timestamp_to_chunk(self, trade_chunk: list) -> list:
        correct_timestamp = self._get_correct_timestamp(trade_chunk)
        trade_chunk.insert(0, [correct_timestamp])
        return trade_chunk