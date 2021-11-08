import yaml

def read_config(fpath:str, key_list:list) -> list:
    """
    The function to read config yaml file
    ---
    params

    fpath: configuration file path
    key_list: list of key for configurations
    ---
    return
    
    list of configuration
    """
    # Read config file first
    with open(fpath, "r") as stream:
        config = yaml.safe_load(stream)
    # Get variables from config
    return [config[key] for key in key_list]

