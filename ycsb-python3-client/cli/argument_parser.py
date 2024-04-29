import argparse
import shlex
from cli.usage import YCSBUsage
from commands.ycsb_command import YCSBCommand
from databases.database_loader import DatabaseLoader

class ArgumentParser:
    """
    Handles parsing of command line arguments.
    """
    def __init__(self):
        self.usage = YCSBUsage()
        self.parser = argparse.ArgumentParser(
            usage=self.usage.generate_usage(),
            formatter_class=argparse.RawDescriptionHelpFormatter)
        self._setup_arguments()

    def _setup_arguments(self):
        self.parser.add_argument('-cp', dest='classpath', help="Additional classpath entries, e.g., '-cp /tmp/hbase-1.0.1.1/conf'")
        self.parser.add_argument("-jvm-args", default=[], type=shlex.split, help="Additional JVM arguments, e.g., '-Xmx4g'")
        self.parser.add_argument("command", choices=sorted(YCSBCommand().commands), help="Command to run.")
        self.parser.add_argument("database", choices=sorted(DatabaseLoader().load_databases_from_json()), help="Database to test.")

    def parse(self):
        return self.parser.parse_known_args()