import bitmex
import json
from datetime import datetime
import re
from calendar import monthrange
from time import sleep
import functools
import operator
import collections
from tqdm import tqdm


class BitmexTradingHistoryFetcher:
    
    response_keys: list = ['timestamp', 'orderID', 'orderQty', 'price', 'text', 'avgEntryPrice', 'realisedPnl']
    new_data_columns: list = ['realisedPnl_in_btc', 'realised_profit_or_loss_in_usd']
    funding_string: str = "Funding"
    funding_order_id: str = "00000000-0000-0000-0000-000000000000"

    def __init__(self, api_key: str, api_secret: str):
        self.api_key: str= api_key
        self.api_secret: str = api_secret

    def fetch_data_for_period(self, year_to_fetch: int, month_to_fetch: int = None):
        date_list: list = self._get_date_ranges(year_to_fetch, month_to_fetch)
        raw_responses = self._fetch_raw_responses(date_list)
        none_filtered_flattened_responses = self._filter_for_none_and_flatten_response_list(raw_responses)
        none_filtered_flattened_responses.sort(key=self._get_datetime_from_json)
        filtered_raw_data = self._get_filtered_raw_data(none_filtered_flattened_responses)
        filtered_trades = self._get_trade_chunks(filtered_raw_data)
        cleaned_filtered_trades = self._clean_chunks(filtered_trades)
        final_raw_data_merged = [ item for list_item in cleaned_filtered_trades for item in list_item ]
        final_raw_positions, final_raw_fundings = self._get_final_raw_data(final_raw_data_merged)
        final_positions, final_fundings = self._get_final_modified_responses(final_raw_positions, final_raw_fundings)
        return final_positions, final_fundings

    def get_response_keys(self) -> list:
        return self.response_keys

    def get_new_data_columns(self) -> list:
        return self.new_data_columns

    def _get_final_modified_responses(self, final_raw_positions: list, final_raw_fundings: list) -> list:
        final_positions = [ self._create_final_json_item(json_item) for json_item in final_raw_positions ]
        final_fundings = [ self._create_final_json_item(json_item) for json_item in final_raw_fundings ]
        return final_positions, final_fundings

    def _create_final_json_item(self, json_item) -> str:
        json_item[self.new_data_columns[0]] = self._transform_from_satoshi_to_btc(json_item['realisedPnl'])
        json_item[self.new_data_columns[1]] = round(json_item[self.new_data_columns[0]] * json_item['price'], 2)
        return json_item

    def _get_final_raw_data(self, final_raw_data: list) -> (list, list):
        final_raw_positions = list()
        final_raw_fundings = list()
        for item in final_raw_data: 
            current_order_id = item['orderID']
            if current_order_id == self.funding_order_id and self.funding_string == item['text']:
                final_raw_fundings.append(item)
                continue
            else:
                final_raw_positions.append(item)
        return final_raw_positions, final_raw_fundings

    def _clean_chunks(self, trades: list) -> list:
        new_trades = list()
        for trade in trades:
            close_position: datetime = self._get_datetime_from_json(trade[-1])
            deletions = list()
            for item in trade:
                item_date: datetime = self._get_datetime_from_json(item)
                if (item_date.date() == close_position.date() and item['avgEntryPrice'] != 'None'):
                    deletions.append(item)
            cleaned_trade = [item for item in trade if item not in deletions]
            new_trades.append(cleaned_trade)
        return new_trades


    def _get_trade_chunks(self, final_raw_data: list) -> list:
        all_trades = list()
        chunk = list()
        first_item: str = final_raw_data[0]
        for item in final_raw_data:
            if (item is first_item):
                chunk.append(item)
                continue
            if (item['avgEntryPrice'] == 'None'):
                chunk.append(item)
                all_trades.append(chunk)
                chunk = list()
            else:
                chunk.append(item)
        return all_trades

    def _get_filtered_raw_data(self, flattened_responses: list) -> list:
        filtered_raw_positions, filtered_raw_fundings = self._set_position_and_funding_items(flattened_responses)
        filtered_raw_positions = list(filtered_raw_positions.values())
        filtered_raw_data = filtered_raw_positions + filtered_raw_fundings
        filtered_raw_data.sort(key=self._get_datetime_from_json)
        return filtered_raw_data

    def _set_position_and_funding_items(self, flattened_response_list: list) -> (dict, list):
        filtered_raw_position_dict = dict()
        filtered_raw_funding_list = list()
        for item in flattened_response_list: 
            current_order_id = item['orderID']
            if current_order_id == self.funding_order_id and self.funding_string == item['text']:
                filtered_raw_funding_list.append(item)
                continue
            else:
                self._set_correct_final_raw_position_item(current_order_id, filtered_raw_position_dict, item)
        return filtered_raw_position_dict, filtered_raw_funding_list

    def _set_correct_final_raw_position_item(self, current_order_id: str, filtered_raw_position_dict: dict, loop_item: str):
        if (current_order_id in filtered_raw_position_dict):
            currently_stored_item = filtered_raw_position_dict[current_order_id] 
            if (loop_item['realisedPnl'] < 0 and (currently_stored_item['realisedPnl'] > loop_item['realisedPnl'])):
                filtered_raw_position_dict[current_order_id] = loop_item
            elif (loop_item['realisedPnl'] > 0 and (currently_stored_item['realisedPnl'] < loop_item['realisedPnl'])):
                filtered_raw_position_dict[current_order_id] = loop_item
        else:
            filtered_raw_position_dict[current_order_id] = loop_item

    def _filter_for_none_and_flatten_response_list(self, raw_responses: list) -> list:
        none_filtered_flattened_responses = [ self._create_flattened_json(json_item) for raw_item in raw_responses if raw_item is not None for json_item in raw_item ]
        return none_filtered_flattened_responses
       
    def _fetch_raw_responses(self, date_list: list) -> list:
        client = bitmex.bitmex(test=False, api_key=self.api_key, api_secret=self.api_secret)
        raw_responses: list = list()
        for timestamp in tqdm(date_list):
            response = self._get_data_via_api_call(client, timestamp)
            raw_responses.append(response)
        return raw_responses

    def _sort_for_timestamp(self, json_item):
        return json_item['timestamp']

    def _transform_from_satoshi_to_btc(self, satoshis: int):
        satoshis = str(satoshis)
        if(satoshis.startswith("-")):
            is_negative_value = True
            satoshis = satoshis[1:]
        else:
            is_negative_value = False
        needed_btc_length = 9 - len(satoshis)
        satoshis = "{0}{1}".format(needed_btc_length*"0", satoshis)
        satoshis = "{0}.{1}".format(satoshis[0], satoshis[1:])
        if(is_negative_value): 
            satoshis = "{0}{1}".format("-", satoshis)
        return float(satoshis)

    def _create_flattened_json(self, full_json_item) -> json:
        flattened_dict = {key:self._remove_newline_in_text(key, full_json_item[key]) for key in self.response_keys}
        return json.loads(json.dumps(flattened_dict))

    def _remove_newline_in_text(self, key, value) -> str:
        if key == 'text' and "\n" in value:
            new_value: str = value.replace("\n", " ")
            return new_value
        return value 

    def _get_data_via_api_call(self, client, timestamp) -> json:
        try:
            sleep(1)
            response = client.User.User_getExecutionHistory(symbol="XBTUSD", timestamp = timestamp).result()
        except Exception as e:
            try:
                response = re.search(r"\[{.+}\]", str(e))
                final_response = response.group()
                final_response2 = final_response.replace("'", "\"")
                final_response3 = final_response2.replace("None", "\"None\"")
                final_json = json.loads(final_response3)  
                return final_json
            except Exception as e2:
                return None

    def _get_date_ranges(self, year_to_fetch: int, month_to_fetch: int = None) -> list:
        date_list: list = list()
        if (month_to_fetch != None):
            number_of_days_in_month = monthrange(year_to_fetch, month_to_fetch)[1]
            date_list = [datetime(year_to_fetch, month_to_fetch, day, 12, 0, 0, 0) for day in range(1, number_of_days_in_month+1)]
        else:
            date_list = [ datetime(year_to_fetch, month_number, day, 12, 0, 0, 0) for month_number in range(1, 13) for day in range(1, monthrange(year_to_fetch, month_number)[1]+1) ]
        return date_list
    
    def _get_datetime_from_json(self, json):
        try:
            return datetime.strptime(json['timestamp'], "%Y-%m-%dT%H:%M:%S.%fZ")
        except KeyError:
            return 0