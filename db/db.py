import yaml
from sqlalchemy import create_engine

"""
Getting a connection for postgresql
"""
def get_conn(fname):

    # Read config file first
    with open("../config.yaml", "r") as stream:
        config = yaml.safe_load(stream)

    db = create_engine(f"postgresql://{config['DB']['USER']}:{config['DB']['PASSWD']}@{config['DB']['HOST']}:{config['DB']['PORT']}/{config['DB']['DB_NAME']}")
    conn = db.connect()

    return conn


def insert_data(table):
    conn = get_conn("config.yaml")
    query = f"""
        INSERT INTO {table} VALUES ()
    """