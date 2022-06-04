from sqlalchemy import MetaData
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from setup_psql_enironment import get_database
import sql_classes

def create_database():
    # Setup environment and create a session
    db = get_database()
    Session = sessionmaker(bind=db)
    meta = MetaData(bind=db)
    session = Session()

    # Create database from SQLAlchemy models
    sql_classes.Base.metadata.create_all(db)

if __name__ == "__main__":
    create_database()
