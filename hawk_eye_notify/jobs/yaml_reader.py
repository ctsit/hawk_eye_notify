import yaml

def get_config(config_file_path, config_to_get):
    config = __read_config(config_file_path)
    return config.get(config_to_get, None)


def __read_config(config_file_path):
    config = None
    with open(config_file_path, 'r') as config_file:
        try:
           config = yaml.load(config_file.read())
        except yaml.YAMLError as exc:
            print(exc)

    return config
