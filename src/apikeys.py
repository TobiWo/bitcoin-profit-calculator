import json
import os

class APIKeyLoader:

    def __init__(self, path_to_keyfile: str = None):
        if (path_to_keyfile is None):
            self.path_to_keyfile: str = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..' ,'resources', 'api_keys.json'))
        else:
            self.path_to_keyfile = path_to_keyfile

    def get_keys(self) -> dict:
        keys = dict()
        with open(self.path_to_keyfile) as json_file:
            data = json.load(json_file)
            keys['bitmex'] = self._load_bitmex_keys(data)
        return keys
    
    def _load_bitmex_keys(self, json_file) -> dict:
        bitmex_keys_dict = dict()
        bitmex_keys_json_list = json_file['bitmex']['key_pairs']
        for item in bitmex_keys_json_list:
            bitmex_keys_dict[item['key']] = item['secret']
        return bitmex_keys_dict