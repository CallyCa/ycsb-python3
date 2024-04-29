import logging
import json
import os

# Logger Configuration
logger = logging.getLogger(__name__)
logger.setLevel(logging.WARNING)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


def load_deprecated_clients():
    """
    Loads deprecated client bindings from a JSON file located in the 'databases/json' directory.

    Returns:
        set: A set of deprecated client bindings.
    """
    base_path = os.path.dirname(__file__)
    json_path = os.path.join(base_path, '..', 'databases', 'json', 'deprecated_clients.json')
    
    try:
        with open(json_path, 'r') as file:
            data = json.load(file)
            return set(data['deprecated_bindings'])
    except FileNotFoundError:
        logging.error("Deprecated clients configuration file not found at {}".format(json_path))
        return set()
    except json.JSONDecodeError:
        logging.error("Error decoding the JSON file at {}".format(json_path))
        return set()

deprecated_bindings = load_deprecated_clients()

def deprecated_clients_check(binding):
    """
    Checks if the specified binding is deprecated and logs a warning if so.

    Args:
        binding (str): The database binding to check.
    """
    if binding in deprecated_bindings:
        logging.warning(f"The '{binding}' client has been deprecated.")
