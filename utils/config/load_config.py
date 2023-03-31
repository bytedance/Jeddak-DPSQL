import configparser
import os


def load_config(file_name, conf_name):
    thisfolder = os.path.dirname(os.path.abspath(__file__))
    initfile = os.path.join(thisfolder, file_name)
    config = configparser.ConfigParser()
    config.read(initfile)
    config_items = config.items(conf_name)
    config_dict = dict(config_items)
    return config_dict
