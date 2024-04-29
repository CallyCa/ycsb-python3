import os
import json

class YCSBCommand:
    """
    Manages the YCSB commands configuration, providing easy access to command details.
    """

    def __init__(self):
        """
        Initializes the command dictionary by loading YCSB command details from a JSON file.
        """
        self.json_path = os.path.join(os.path.dirname(__file__), '..', 'databases', 'json', 'commands.json')
        self.commands = self.load_commands()

    def load_commands(self):
        """
        Loads command configurations from a JSON file.

        :return: A dictionary containing all command configurations.
        """
        with open(self.json_path, 'r') as file:
            return json.load(file)

    def get_command_details(self, command_name):
        """
        Retrieves the details for a specified command.

        :param command_name: The name of the command to retrieve details for.
        :return: A dictionary containing the command's details or None if the command does not exist.
        """
        return self.commands.get(command_name)

    def list_commands(self):
        """
        Lists all available commands and their descriptions.

        :return: A list of tuples containing command names and their descriptions.
        """
        return [(cmd, details['description']) for cmd, details in self.commands.items()]
