
# Structure
- `main.py`: headless runner
- `db_app/database.py`: SQLite connection handling and schema initialization
- `db_app/dal.py`: inline SQL queries and CRUD/data-access methods
- `db_app/bootstrap.py`: wiring and optional one-time seed data
- `sql/schema.sql`: `CREATE TABLE IF NOT EXISTS` schema script

## Run
```powershell/cmd
python main.py
```

The first run creates `Export/library.db`, applies schema, and seeds starter data.


