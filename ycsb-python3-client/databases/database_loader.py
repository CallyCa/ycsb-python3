import os
import json
from typing import Dict, Any

class DatabaseLoader:
    """
    Loads and caches database configurations from a JSON file, checking file modification to refresh cache as needed.
    """

    def __init__(self):
        """
        Initializes the DatabaseLoader with the path to the JSON configuration file.
        """
        self.json_path = os.path.join(os.path.dirname(__file__), 'json', 'databases.json')
        self.cache = None
        self.last_mod_time = None

    def load_databases_from_json(self) -> Dict[str, Any]:
        """
        Loads the database configurations from a JSON file. Checks the file's last modification time to decide whether to use cached data or reload.

        :return: A dictionary with database configurations.
        """
        current_mod_time = os.path.getmtime(self.json_path)
        if self.cache is not None and self.last_mod_time == current_mod_time:
            return self.cache

        try:
            with open(self.json_path, 'r') as file:
                self.cache = json.load(file)
                self.last_mod_time = current_mod_time
                return self.cache
        except FileNotFoundError:
            raise Exception("Database configuration file not found.")
        except json.JSONDecodeError:
            raise Exception("Error decoding the JSON database configuration file.")

    def reload_databases(self) -> Dict[str, Any]:
        """
        Forces a reload of the database configurations from the JSON file, regardless of the modification time.

        :return: A dictionary with the updated database configurations.
        """
        self.cache = None
        return self.load_databases_from_json()
