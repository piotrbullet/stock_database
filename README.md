# Stock prices 

## Dtabase setup

1. Launch database and pg_admin

```bash
cd docker/
docker-compose up
```

2. Setup database

```bash
python3 create_database.py
```

2. Connect to pg_admin

Go to http://localhost:5050/

login: admin@admin.com
pass: root

3. Setup database view

- rightclik Servers -> Create -> Server
- General -> Name: stock_data
- Connection -> Host name: pg, username: root, password: root

4. Verify setup

stock_data -> stock_data -> Schemas -> Tables

## Database connection

Refer to `connection_test.ipynb`

docker run --name postgres-db -e POSTGRES_PASSWORD=root -p 5433:5432 -d postgres

5. Create and populate database

Run create_database.py script, this will create a database structure.

After creating database structure run populate_database.py, this script will populate
database with a single exchange, securities with .csv file and then it will start to populate
daily prices on the basis of yahoo finance.