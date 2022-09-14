import pandas as pd
from sqlalchemy import MetaData
from sqlalchemy.orm import sessionmaker
from setup_psql_enironment import get_database
from wallstreet import wallstreet
from requests.exceptions import HTTPError, ReadTimeout
from time import sleep
from sqlalchemy.exc import IntegrityError


def insert_exchange(engine, name: str, currency: str) -> None:
    sql = f"INSERT INTO exchange (name, currency) VALUES ('{name}', '{currency}')"
    with engine.connect() as connection:
        with connection.begin():
            connection.execute(sql)


def populate_securities_with_csv(engine, csv_path: str) -> None:
    nyse = pd.read_csv(csv_path)
    nyse.drop(['Last Sale', 'Net Change', 'Market Cap', 'Country',
               'IPO Year', 'Volume', '% Change'], axis=1, inplace=True)
    nyse.columns = ['Ticker', 'Name', 'Sector', 'Industry']
    nyse['exchange_id'] = 1

    for row in nyse.itertuples(index=False):
        with engine.connect() as connection:
            with connection.begin():
                try:
                    connection.execute(f"INSERT INTO security (ticker, name, sector, industry, exchange_id) "
                                       f"VALUES ('{row.Ticker}', '{row.Name}', '{row.Sector}', '{row.Industry}',"
                                       f" {row.exchange_id})")
                except:
                    continue
                    connection.execute(f"INSERT INTO security (ticker, name, exchange_id) "
                                       f"VALUES ('{row.Ticker}', '{row.Name}', {row.exchange_id})")


def populate_prices(engine, days_back: int) -> None:
    with engine.connect() as connection:
        with connection.begin():
            tickers_with_id = connection.execute("SELECT ticker, id FROM security").fetchall()
            result = connection.execute("SELECT DISTINCT ticker_id FROM price").fetchall()
            ids_present_in_db = [i[0] for i in result]

    for ticker, _id in tickers_with_id:
        if _id in ids_present_in_db:
            continue
        try:
            stock = wallstreet.Stock(ticker)
            df = stock.historical(days_back=days_back)
        except IndexError as e:
            print(e)
            continue
        except KeyError as e:
            print(e)
            continue
        except HTTPError as e:
            continue
        except LookupError as e:
            print(e)
            continue
        except ReadTimeout as e:
            print(f"{e}\nWaiting for 60 seconds, because yahoo finance is a piece of shit.")
            sleep(60)
            continue
        for index, row in df.iterrows():
            with engine.connect() as connection:
                with connection.begin():
                    try:
                        connection.execute(f"INSERT INTO price (ticker_id, date, open, high, "
                                           f"low, close, adj_close, volume) "
                                           f"VALUES ('{_id}', '{row[0].strftime('%Y-%m-%d')}', {row[1]}, {row[2]}, "
                                           f"{row[3]}, {row[4]}, {row[5]}, {int(row[6])})")
                    except:
                        continue


if __name__ == "__main__":
    db = get_database()
    Session = sessionmaker(bind=db)
    meta = MetaData(bind=db)
    session = Session()
    highest_id = 0

    try:
        with db.connect() as connection:
            with connection.begin():
                insert_exchange(db, 'NYSE', 'USD')
        with db.connect() as connection:
            with connection.begin():
                populate_securities_with_csv(db, './data/nyse_data.csv')
    except:
        pass

    while highest_id < 7918:
        with db.connect() as connection:
            with connection.begin():
                highest_id = connection.execute("SELECT MAX(ticker_id) FROM price").fetchall()[0][0]
        populate_prices(db, 50)