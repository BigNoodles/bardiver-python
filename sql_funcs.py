#!/usr/bin/etc python3

#imports
import sqlite3


def connect(sqlite_file):
    """
    Makes a connection to an SQLite database file
    Returns connection and cursor
    """

    try:
        conn = sqlite3.connect(sqlite_file)
        c = conn.cursor()
        return conn, c
    except Exception as e:
        print(f'Could not connect to {sqlite_file}: {e}')
        return None



def close(conn):
    """
    Close a connection to a database
    """

    conn.close()




def total_rows(c, table_name, print_out=False):
    """
    Returns the total number of rows in the database
    """

    c.execute(f'SELECT COUNT(*) FROM {table_name}')
    count = c.fetchall()

    if print_out:
        print(f'Total rows: {count[0][0]}')

    return count[0][0]




def table_col_info(c, table_name, print_out=False):
    """
    Returns a list of tuples with column info
    """

    c.execute(f'PRAGMA TABLE_INFO({table_name})')
    info = c.fetchall()

    if print_out:
        print(f"Column Info:\nID, Name, Type, NotNull, DefaultVal, PrimaryKey")
        for col in info:
            print(col)

    return info




def values_in_col(c, table_name, print_out=True):
    """
    Returns a dictionary with columns as keys
    Values of not-null entires as values
    """

    c.execute(f'PRAGMA TABLE_INFO({table_name})')
    info = c.fetchall()
    col_dict = dict()
    for col in info:
        col_dict[col[1]] = 0
    for col in col_dict:
        c.execute(f'SELECT ({col}) FROM {table_name} \
                WHERE {col} IS NOT NULL')
        number_rows = len(c.fetchall())
        col_dict[col] = number_rows

    if print_out:
        print(f'Number of entries per column:')
        for i in col_dict.items():
            print(f'{i[0]}: {i[1]}')

    return col_dict




