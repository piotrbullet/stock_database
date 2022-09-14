from sqlalchemy import create_engine
from getpass import getpass
import yaml


def get_database():
    try:
        engine = get_connection_from_profile()
        print("Connected to PostgreSQL database!")
    except IOError:
        print("Failed to get database connection!")
        return None, 'fail'
    return engine


def get_connection_from_profile(config_file_name="setup_psql_environment.yaml"):
    with open(config_file_name, 'r') as f:
        vals = yaml.safe_load(f)
    if not ('PGHOST' in vals.keys() and
            'PGUSER' in vals.keys() and
            'PGDATABASE' in vals.keys() and
            'PGPORT' in vals.keys()):
        raise Exception('Bad config file: ' + config_file_name)
    return get_engine(vals['PGDATABASE'], vals['PGUSER'], vals['PGHOST'], vals['PGPORT'], vals['PGPASS'])


def get_engine(db, user, host, port, passwd):
    url = 'postgresql://{user}:{passwd}@{host}:{port}/{db}'.format(
        user=user, passwd=passwd, host=host, port=port, db=db)
    engine = create_engine(url, pool_size=50, echo=True)
    return engine
