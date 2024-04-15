import json
import os

def load_key(json_file="config.json"):
    """
    Read a JSON file and load its content into a dictionary.

    Args:
        json_file (str): Path to the JSON file.

    Returns:
        str: Dictionary containing the JSON data.
    """

    # Get the directory of the script
    base_dir = os.path.dirname(os.path.abspath(__file__))

    # Construct the path to the config.json file
    config_path = os.path.join(base_dir, "..", "config", json_file)


    with open(config_path, "r") as file:
        data = json.load(file)

    if data:
        os.environ['OPENAI_API_KEY'] = data['OPENAI_API_KEY']
        print("OPENAI_API_KEY exported successfully.")
    else:
        print("Failed to set OPENAI_API_KEY.")
