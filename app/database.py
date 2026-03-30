from __future__ import annotations

from contextlib import contextmanager
from pathlib import Path
import sqlite3


class DatabaseManager:
    """Manage SQLite connections and database initialization."""

    def __init__(self, db_path: str | Path, schema_path: str | Path) -> None:
        self.db_path = str(db_path)
        self.schema_path = Path(schema_path)

    @contextmanager
    def get_connection(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.db_path)
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys = ON;")
        try:
            yield connection
            connection.commit()
        except Exception:
            connection.rollback()
            raise
        finally:
            connection.close()

    def initialize(self) -> None:
        """Create database tables/indexes from schema.sql if they do not exist."""
        schema_sql = self.schema_path.read_text(encoding="utf-8")
        with self.get_connection() as connection:
            connection.executescript(schema_sql)

