import pandas as pd

class DataCalculator:

    tax_df_columns = ['sum_positions', 'sum_fundings', 'total_profit_loss', 'total_taxes']

    def transform_json_list_to_dataframe(self, keys: list, data_list: list):
        transformed_data_list = [ self._get_list_from_json_structure(json) for json in data_list ]
        data_frame = pd.DataFrame(transformed_data_list, columns = keys, dtype = float) 
        return data_frame

    def calculate_taxes(self, positions_data_frame, funding_data_frame, usd_profit_loss_column_name: str, tax_rate: float = None, tax_free_limit: float = None):
        positions_sum = positions_data_frame[usd_profit_loss_column_name].sum()
        fundings_sum = funding_data_frame[usd_profit_loss_column_name].sum()
        profit_loss_sum = positions_sum + fundings_sum
        total_taxes = None
        if (tax_rate is None):
            total_taxes = 0
        else:
            if (profit_loss_sum >= 0 and tax_free_limit is None):
                total_taxes = profit_loss_sum * tax_rate
            elif (profit_loss_sum >= 0 and tax_free_limit is not None):
                if (profit_loss_sum > tax_free_limit):
                    total_taxes = profit_loss_sum * tax_rate
                else:
                    total_taxes = 0
            else: 
                total_taxes = 0
        sum_and_tax_list = [positions_sum, fundings_sum, profit_loss_sum, total_taxes]
        return pd.DataFrame(list(zip(self.tax_df_columns, sum_and_tax_list)), columns = ['name', 'value'], dtype = float)

    def _get_list_from_json_structure(self, json_item):
        return [ value for key, value in json_item.items() ]