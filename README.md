# Python YCSB Client

This repository contains the Python 3 implementation of the Yahoo! Cloud Serving Benchmark (YCSB) client. It provides an interface to conduct performance benchmarks on different database systems.

## Directory Structure

Below is an overview of the main directories and files in this project:

```
ycsb-python3/
│
├── cli/                  # Command Line Interface utilities and main entry points
│   ├── argument_parser.py
│   ├── environment_configurator.py
│   ├── __init__.py
│   ├── usage.py
│   └── ycsb_main.py
│
├── commands/             # Definitions of YCSB commands like load, run, and shell
│   ├── __init__.py
│   └── ycsb_command.py
│
├── databases/            # Database configurations and JSON definitions
│   ├── database_loader.py
│   ├── __init__.py
│   └── json/
│       ├── commands.json
│       ├── databases.json
│       ├── deprecated_clients.json
│       └── options.json
│
├── executor/             # Execution logic for running YCSB commands
│   ├── command_executor.py
│   └── __init__.py
│
├── options/              # Configuration options for YCSB operations
│   ├── __init__.py
│   └── options.py
│
└── util/                 # Utility functions and classes
    ├── classpath_configurator.py
    ├── deprecated_clients.py
    └── __init__.py
```

## Available Commands

- `shell`: Enter the interactive mode.
- `load`: Execute the load phase to populate the database.
- `run`: Execute the transaction phase to benchmark the database.

## Configuration Options

- `-P file`: Specify the workload file.
- `-p key=value`: Override a workload property.
- `-s`: Print status updates to stderr.
- `-target n`: Target operations per second (default: unthrottled).
- `-threads n`: Number of client threads (default: 1).
- `-cp path`: Additional Java classpath entries.
- `-jvm-args args`: Additional JVM arguments.

## Getting Started

### Prerequisites

Ensure you have Python 3.6 or later installed. Depending on the database you plan to benchmark, additional software may be required, such as Java for YCSB core functionalities.

### Installation

Clone the repository and navigate into the project directory:

```bash
git clone https://github.com/CallyCa/ycsb-python3.git
cd ycsb-python3
```

## Running YCSB

To run the YCSB client, use one of the following commands from the root directory of the project:

#### Load Phase

```bash
python -m cli.ycsb_main load -P workloads/workloada -p recordcount=1000000 -db site.ycsb.db.YourDbClient -s
```

#### Run Phase

```bash
python -m cli.ycsb_main run -P workloads/workloada -p operationcount=1000000 -db site.ycsb.db.YourDbClient -s
```

#### Interactive Shell

```bash
python -m cli.ycsb_main shell
```

After executing any of these commands, a log file will be created in the root directory of the project under the directory `workload-logs`. The log file is named `command-executor.log` and contains information about the execution process.

Replace `site.ycsb.db.YourDbClient` with the appropriate database client class and adjust workload files as needed.

#### Notes

Running the `ycsb` command without any argument will print the usage.

See <https://github.com/brianfrankcooper/YCSB/wiki/Running-a-Workload> for a detailed documentation on how to run a workload.

See <https://github.com/brianfrankcooper/YCSB/wiki/Core-Properties> for the list of available workload properties.

## Building from source

YCSB requires the use of Maven 3; if you use Maven 2, you may see [errors
such as these](https://github.com/brianfrankcooper/YCSB/issues/406).

To build the full distribution, with all database bindings:

```bash
mvn clean package
```

To build a single database binding:

```bash
mvn -pl site.ycsb:mongodb-binding -am clean package
```

## Contributing

Contributions are welcome. Please fork the repository and submit pull requests with your enhancements.

## License

This project is licensed under the [MIT License](LICENSE.txt).
