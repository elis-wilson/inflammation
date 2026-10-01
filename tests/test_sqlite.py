import pytest
import sqlite3
from pathlib import Path
from unittest.mock import patch
from inflammation.sqlite_example import connect_to_database, query_database


def test_connect_to_db_type():
    """
    Test that connect_to_database function returns sqlite3.Connection
    """
    conn = connect_to_database('test.db')
    assert isinstance(conn, sqlite3.Connection)
    conn.close()

def test_connect_to_db_name():
    """
    Test that connect_to_database function connects to correct DB file
    """
    conn = connect_to_database('test.db')
    cur = conn.cursor()
    # List current databases https://www.sqlite.org/pragma.html#pragma_database_list
    cur.execute('PRAGMA database_list;')
    # Unpack the three parameters returned
    db_index, db_type, db_filepath = cur.fetchone()
    # Extract just the filename from the full filepath
    db_filename = Path(db_filepath).name
    assert db_filename == 'test.db'
    conn.close()

@pytest.fixture
def database_conenction():
    db_filename = 'test.db'
    conn = sqlite3.connect(db_filename)
    yield conn
    conn.close()
    Path.unlink(db_filename)

@pytest.fixture
def database_fn_fixture(tmp_path_factory):
    yield tmp_path_factory.mktemp("data") / "test.db"

@pytest.fixture
def database_connection(database_fn_fixture):
    """
    Create database connection
    """
    conn = sqlite3.connect(database_fn_fixture)
    yield conn
    conn.close()
    Path.unlink(database_fn_fixture)

@pytest.fixture
def setup_database(database_connection):
    conn = database_conenction
    cur = conn.cursor()
    cur.execute("CREATE TABLE Animals(Name, Species, Age)")
    cur.execute("INSERT INTO Animals VALUES ('Bugs', 'Rabbit', 6)")
    conn.commit()
    yield conn
    cur.execute('DROP TABLE Animals')

def test_connect_to_db_type(database_fn_fixture):
    """
    Test that connect_to_db function returns sqlite3.Connection
    """
    conn = connect_to_database(database_fn_fixture)
    assert isinstance(conn, sqlite3.Connection)
    conn.close()

def test_connect_to_db_name(database_fn_fixture):
    """
    Test that connect_to_db function connects to correct DB file
    """
    conn = connect_to_database(database_fn_fixture)
    cur = conn.cursor()
    # List current databases https://www.sqlite.org/pragma.html#pragma_database_list
    cur.execute("PRAGMA database_list;")
    # Unpack the three parameters returned
    db_index, db_type, db_filepath = cur.fetchone()
    # Test that the database filename is the same as the one from the fixture
    assert Path(db_filepath).name == Path(database_fn_fixture).name
    conn.close()

def test_query_database(setup_database):
    """
    Test that query_database retrieves the correct data
    """
    conn = setup_database
  
    # Use query_database to retrieve data
    sql = "SELECT * FROM Animals"
    result = query_database(sql, connection=conn)
    # Result returned is a list (cursor.fetchall)
    assert isinstance(result, list)
    # There should just be one record
    assert len(result) == 1
    # That record should be the data we added
    assert result[0] == ("Bugs", "Rabbit", 6)

def test_query_database_without_connection(setup_database):
    """
    Test the `query_database` function without a provided connection
    """
    conn = setup_database
    sql = 'SELECT * FROM Animals'
    result = query_database(sql, connection = conn)
    # ensure that we get a TypeError
    with pytest.raises(TypeError):
        query_database(sql)

@patch('sqlite3.connect')
def test_query_db_mocked_connection():
    """Mock the database connection and cursor to ensure the correct methods
    are called within the query_database function
    """
    #with patch('sqlite3.connect') as mock_connection:
    mock_cursor = mock_connection.return_value.cursor.return_value
    mock_cursor.fetchall.return_value = [("Jerry", "Mouse", 1)]
    # make our fake connection
    conn = mock_connection("my_non_existent_file")
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