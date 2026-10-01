import pytest
import sqlite3
from pathlib import Path
from inflammation.sqlite_example import connect_to_database, query_database
from unittest.mock import Mock

@pytest.fixture(scope="session")
def database_fn_fixture(tmp_path_factory):
    """
    Uses tmp_path_factory to create a filename in a temp directory
    """
    yield tmp_path_factory.mktemp("data") / "test.db"


def test_query_database_mock(database_fn_fixture):
    """Mock the query_database function to show the principle
    """
    sql = "SELECT * FROM Animals"
    conn = connect_to_database(database_fn_fixture)
    query_database = Mock()
    query_database.return_value = ("Jerry", "Mouse", 1)
    assert query_database(sql, connection=conn) == ("Jerry", "Mouse", 1)
    query_database.assert_called_once_with(sql, connection=conn)


def test_query_db_mocked_connection():
    """Mock the database connection and cursor to ensure the correct methods
    are called within the query_database function
    """
    sqlite3.connect = Mock()
    # create a fake cursor and define the data fetchall() returns
    mock_cursor = sqlite3.connect.return_value.cursor.return_value
    mock_cursor.fetchall.return_value = [("Jerry", "Mouse", 1)]
    # make our fake connection
    conn = sqlite3.connect("my_non_existent_file")
    sql = "SELECT * FROM Animals"
    # test what query_database does with our fake connection
    result = query_database(sql, connection=conn)
    assert result[0] == ("Jerry", "Mouse", 1)
    # check that query_database passes our SQL string to cursor.execute()
    mock_cursor.execute.assert_called_once_with(sql)
    # check that fetchall() was called
    mock_cursor.fetchall.assert_called_once()
    # check that query_database closes the connection
    conn.close.assert_called_once()