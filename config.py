import configparser

cfg = configparser.ConfigParser()


print("Reading config files...")
# Parsing configuration from config.cfg
cfg.read("mysql.cfg")

HOST = cfg['mysql']['host']
PORT = int(cfg['mysql']['port'])
USER = cfg['mysql']['user']
PASSWORD = cfg['mysql']['password']
DATABASE = cfg['mysql']['db']