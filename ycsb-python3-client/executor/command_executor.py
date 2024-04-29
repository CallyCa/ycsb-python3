import os
import subprocess
import logging
import threading

# Logger configuration
logger = logging.getLogger('CommandExecutor')
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

# Ensure the log directory exists
log_directory = 'workload-logs'
if not os.path.exists(log_directory):
    os.makedirs(log_directory)

# Handler for file logging
file_handler = logging.FileHandler(os.path.join(log_directory, 'command-executor.log'))
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# Handler for console output
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.DEBUG)
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)

class CommandExecutor:
    """
    This class is responsible for executing external system commands, providing robust error handling,
    output capturing, asynchronous execution options, and timeout management, with comprehensive logging to a file and console.
    """

    @staticmethod
    def execute_command(command, capture_output=True, wait=True, timeout=None):
        """
        Executes a system command with options to capture outputs, execute asynchronously, and manage execution time
        with a timeout, while logging all activities to a file and console.
        """
        logger.info(f"Executing command: {' '.join(command)}")
        try:
            process = subprocess.Popen(
                command,
                stdout=subprocess.PIPE if capture_output else None,
                stderr=subprocess.PIPE if capture_output else None,
                text=True,
                bufsize=1
            )
            if capture_output:
                # Capture stdout and stderr
                threading.Thread(target=CommandExecutor.log_output, args=(process.stdout, logger.info)).start()
                threading.Thread(target=CommandExecutor.log_output, args=(process.stderr, CommandExecutor.classify_stderr)).start()

            if wait:
                process.wait(timeout=timeout)
                return {'returncode': process.returncode}
            return process
        except subprocess.TimeoutExpired:
            process.kill()
            logger.error("Command timeout expired")
            return {'returncode': -1}
        except Exception as e:
            CommandExecutor.log_error(f"Failed to execute command: {e}")
            raise

    @staticmethod
    def classify_stderr(line):
        """
        Classify the stderr output to determine if it should be logged as an error or info.
        """
        if "ERROR" in line or "Exception" in line:
            logger.error(line)
        else:
            logger.info(line)

    @staticmethod
    def log_output(pipe, log_function):
        """
        Logs output from subprocess' stdout or stderr.
        """
        with pipe:
            for line in iter(pipe.readline, ''):
                log_function(line.strip())

    @staticmethod
    def log_error(message):
        """
        Logs an error message to the file and console, prefixed with [ERROR].
        """
        logger.error(message)
