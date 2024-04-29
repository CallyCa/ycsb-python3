import os
import json

class Options:
    """
    Manages configuration options for YCSB command execution, loading options from a JSON file.
    """

    def __init__(self):
        """
        Initializes the options dictionary by loading from a JSON file.
        """
        self.json_path = os.path.join(os.path.dirname(__file__), '..', 'databases', 'json', 'options.json')
        self.options = self.load_options()

    def load_options(self):
        """
        Loads options configurations from a JSON file.

        :return: A dictionary containing all option configurations.
        """
        with open(self.json_path, 'r') as file:
            return json.load(file)

    def get_option_description(self, option_key):
        """
        Retrieves the description for a specified option.

        :param option_key: The key of the option to retrieve the description for.
        :return: A string containing the description of the option or None if the option does not exist.
        """
        return self.options.get(option_key)

    def list_options(self):
        """
        Lists all available options and their descriptions.

        :return: A list of tuples containing option keys and their descriptions.
        """
        return [(key, desc) for key, desc in self.options.items()]
