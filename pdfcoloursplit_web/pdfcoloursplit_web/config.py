import configparser
import os

#TODO: Switch out for something like argparse?
config_file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)),
    "config.ini")

config = configparser.ConfigParser()
config.read(config_file_path)
