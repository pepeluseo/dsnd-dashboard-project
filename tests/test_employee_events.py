import sqlite3
from pathlib import Path

import pytest


@pytest.fixture
def db_path():
    """
    Return the path to the employee_events SQLite database.
    """
    project_root = Path(__file__).resolve().parents[1]
    return project_root / "python-package" / "employee_events" / "employee_events.db"


def table_exists(db_path, table_name):
    """
    Check whether a table exists in the SQLite database.
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT name
        FROM sqlite_master
        WHERE type = 'table'
        AND name = ?;
        """,
        (table_name,),
    )

    result = cursor.fetchone()
    conn.close()

    return result is not None


def test_db_exists(db_path):
    """
    Test that the SQLite database file exists.
    """
    assert db_path.exists()


def test_employee_table_exists(db_path):
    """
    Test that the employee table exists.
    """
    assert table_exists(db_path, "employee")


def test_team_table_exists(db_path):
    """
    Test that the team table exists.
    """
    assert table_exists(db_path, "team")


def test_employee_events_table_exists(db_path):
    """
    Test that the employee_events table exists.
    """
    assert table_exists(db_path, "employee_events")

def test_notes_table_exists(db_path):
    """
    Test that the notes table exists.
    """
    assert table_exists(db_path, "notes")
