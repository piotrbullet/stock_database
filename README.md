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

- rightlcik Servers -> Create -> Server
- General -> Name: stock_data
- Connection -> Host name: pg, username: root, password: root

4. Verify setup

stock_data -> stock_data -> Schemas -> Tables