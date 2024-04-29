import os
import sys

from os.path import abspath, dirname

sys.path.append(abspath(dirname(abspath(__file__)) + '/../'))

from cli.argument_parser import ArgumentParser
from cli.environment_configurator import EnvironmentConfigurator
from executor.command_executor import CommandExecutor
from databases.database_loader import DatabaseLoader
from commands.ycsb_command import YCSBCommand
from util.classpath_configurator import ClasspathConfigurator
from util.deprecated_clients import deprecated_clients_check

class YCSBMain:
    """
    Main class to execute the YCSB commands.
    """
    def __init__(self):
        """
        Initialize the argument parser.
        """
        self.args_parser = ArgumentParser()

    def main(self):
        """
        Main execution method, which orchestrates the command parsing, environment setup, and command execution.
        """
        args, remaining = self.args_parser.parse()
        ycsb_home = EnvironmentConfigurator.get_ycsb_home()
        java_path = EnvironmentConfigurator.find_java_path()
        db_classname = DatabaseLoader().load_databases_from_json()[args.database]
        command_details = YCSBCommand().commands[args.command]
        
        classpath = self.configure_classpath(args, ycsb_home)
        ycsb_command = self.build_ycsb_command(args, java_path, classpath, db_classname, command_details["main"], command_details["command"], remaining)
        
        return CommandExecutor.execute_command(ycsb_command)

    def configure_classpath(self, args, ycsb_home):
        """
        Delegates classpath configuration to the ClasspathConfigurator class and
        Configure the classpath based on whether the YCSB is being run as a distribution or from development environment.
        """
        binding = args.database.split("-")[0]
        deprecated_clients_check(binding.split("-")[0])
        configurator = ClasspathConfigurator(args, ycsb_home, binding)
        return configurator.configure_classpath()
    
    def is_distribution(self, ycsb_home):
        """
        Check if the YCSB is running from a distribution by checking for the presence of a 'pom.xml' file.
        """
        return "pom.xml" not in os.listdir(ycsb_home)

    def build_ycsb_command(self, args, java, classpath, db_classname, main_classname, command, remaining):
        """
        Construct the command to be executed in the Java environment, including JVM arguments and database configuration.
        """
        ycsb_command = [java] + args.jvm_args + ["-cp", classpath, main_classname, "-db", db_classname] + remaining
        if command:
            ycsb_command.append(command)
        return ycsb_command

if __name__ == '__main__':
    sys.exit(YCSBMain().main())