import io
import sys

from commands.ycsb_command import YCSBCommand
from databases.database_loader import DatabaseLoader
from options.options import Options

BASE_URL = "https://github.com/brianfrankcooper/YCSB/tree/master/"

class YCSBUsage:
    """
    This class generates the usage information for the YCSB command-line interface,
    including commands, databases, options, and references to workload files.
    """
    
    def __init__(self):
        """
        Initialize the YCSBUsage instance by loading commands, databases, and options from their respective modules.
        """
        self.commands = YCSBCommand().commands
        self.databases = DatabaseLoader().load_databases_from_json()
        self.options = Options().options
        self.usage_info = self.prepare_usage_info()

    def prepare_usage_info(self):
        """
        Precomputes the usage information for faster retrieval on demand.
        """
        output = io.StringIO()
        output.write(f"{sys.argv[0]} command database [options]\n\n")
        
        output.write("Commands:\n")
        for command, details in sorted(self.commands.items(), key=lambda item: item[0]):
            output.write(f"    {command.ljust(14)} {details['description']}\n")
        
        output.write("\nDatabases:\n")
        for db in sorted(self.databases):
            base_url = BASE_URL + db.split('-')[0]
            output.write(f"    {db.ljust(14)} {base_url}\n")
        
        output.write("\nOptions:\n")
        for option, description in sorted(self.options.items(), key=lambda item: item[0]):
            output.write(f"    {option.ljust(14)} {description}\n")
        
        output.write("\nWorkload Files:\n    See https://github.com/brianfrankcooper/YCSB/wiki/Core-Properties for details.\n")
        
        return output.getvalue()

    def generate_usage(self):
        """
        Returns the precomputed usage information.
        """
        return self.usage_info

