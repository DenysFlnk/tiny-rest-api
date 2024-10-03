import pathlib
import yaml


BASE_DIR = pathlib.Path(__file__).parent
config_path = BASE_DIR / 'config' / 'tiny_rest_api.yaml'


def get_config(path):
    with open(path) as file:
        config = yaml.safe_load(file)
    return config

config = get_config(config_path)