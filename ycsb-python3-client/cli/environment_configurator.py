import os
import sys

class EnvironmentConfigurator:
    """
    Configures and retrieves the environment settings necessary for YCSB.
    """
    @staticmethod
    def get_ycsb_home():
        dir = os.path.abspath(os.path.dirname(sys.argv[0]))
        while "LICENSE.txt" not in os.listdir(dir):
            dir = os.path.join(dir, os.path.pardir)
        return os.path.abspath(dir)

    @staticmethod
    def find_java_path():
        java_home = os.getenv("JAVA_HOME")
        return os.path.join(java_home, "bin", "java") if java_home else "java"