import yaml
from sqlalchemy import create_engine

"""
Train/Test data
"""
def get_conn(fname):

    # Read config file first
    with open("../config.yaml", "r") as stream:
        config = yaml.safe_load(stream)

    db = create_engine(f"postgresql://{config['DB']['USER']}:{config['DB']['PASSWD']}@{config['DB']['HOST']}:{config['DB']['PORT']}/{config['DB']['DB_NAME']}")
    conn = db.connect()

    return conn


def insert_data():
    conn = get_conn("config.yaml")