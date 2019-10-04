import csv
import os

class DataWriter:

    def __init__(self):
        self.output_path: str = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'out'))
        self._create_out_dir()

    def _create_out_dir(self):
        try:
            if not(os.path.exists(self.output_path)):
                os.mkdir(self.output_path)
        except OSError:
            print ("Creation of the directory {0} failed".format(self.output_path))

    def write_position_data(self, column_names: list, final_position_list: list, year_to_fetch: int, month_to_fetch: int = None):
        try:
            full_position_file_name: str = self._get_full_file_name("positions", year_to_fetch, month_to_fetch)
            position_file_writer = csv.writer(open(full_position_file_name, "w", newline=''), delimiter=';')
            self._write_data(position_file_writer, column_names, final_position_list)
        except IOError:
            print("Could not open file! Please close file: {}".format(full_position_file_name))

    def write_funding_data(self, column_names: list, final_funding_list: list, year_to_fetch: int, month_to_fetch: int = None): 
        try:
            full_funding_file_name: str = self._get_full_file_name("fundings", year_to_fetch, month_to_fetch)
            funding_file_writer = csv.writer(open(full_funding_file_name, "w", newline=''), delimiter=';')
            self._write_data(funding_file_writer, column_names, final_funding_list)
        except IOError:
            print("Could not open file! Please close file: {}".format(full_funding_file_name))

    def write_final_data_frame(self, data_frame, year_to_fetch: int, month_to_fetch: int = None):
        try: 
            file_name: str = self._get_full_file_name("final_tax_data", year_to_fetch, month_to_fetch)
            data_frame.to_csv(file_name, ";", index = False)
        except IOError:
            print("Could not open file! Please close file: {}".format(file_name))

    def _write_data(self, file_writer, column_names: list, final_data_list: list):
        file_writer.writerow(column_names)
        for item in final_data_list:
            file_writer.writerow(self._create_writerow(column_names, item))
    
    def _create_writerow(self, column_names: list, item) -> list:
        return [ item[column] for column in column_names ]

    def _get_full_file_name(self, general_file_name: str, year_to_fetch: int, month_to_fetch: int = None) -> str:
        if (month_to_fetch != None):
            return os.path.join(self.output_path, "{0}_{1}_{2}.csv".format(general_file_name, year_to_fetch, month_to_fetch))
        else:
            return os.path.join(self.output_path, "{0}_{1}.csv".format(general_file_name, year_to_fetch))
        