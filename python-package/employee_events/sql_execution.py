from pathlib import Path
import sqlite3
import pandas as pd


class SQLExecutionMixin:
    """
    Mixin for executing SQL queries against the employee_events SQLite database.
    """

    db_path = Path(__file__).parent / "employee_events.db"

    def query(self, sql, params=None):
        """
        Execute a SQL query and return the result as a pandas DataFrame.
        """
        if params is None:
            params = ()

        with sqlite3.connect(self.db_path) as conn:
            return pd.read_sql_query(sql, conn, params=params)