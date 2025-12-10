import mysql.connector
from mysql.connector import Error
from contextlib import contextmanager

@contextmanager
def get_db_cursor(commit=False):
    connection = mysql.connector.connect(
        host = "localhost",
        username = "root",
        password = "root",
        database = "expense_manager"
    )

    if connection.is_connected():
        print("DB Connection is established")

    else:
        print("DB Connection couldn't be established")

    cursor = connection.cursor(dictionary=True)

    yield cursor
    connection.commit()

    cursor.close()
    connection.close()


def insert_funds(schemas):
    with get_db_cursor(commit=True) as cursor:
        cursor.executemany("insert into asset_master (scheme_symbol, scheme_name, asset_type) values (%s, %s, 'Mutual Funds')", (schemas))

def delete_funds():
    with get_db_cursor(commit=True) as cursor:
        cursor.execute("delete from asset_master where asset_type='Mutual Funds'")

def insert_stocks(stocks):
    with get_db_cursor(commit=True) as cursor:
        cursor.executemany("insert into asset_master (scheme_symbol, asset_type) values (%s, 'Stocks')", (stocks))

def delete_stocks():
    with get_db_cursor(commit=True) as cursor:
        cursor.execute("delete from asset_master where asset_type='Stocks'")

def savings_summary():
    with get_db_cursor(commit=True) as cursor:
        cursor.callproc('set_investment_growth_value')

def update_current_value(code, val):
    with get_db_cursor(commit=True) as cursor:
        cursor.execute("update investment set current_value =%s where scheme_symbols = %s",(val, code))

def get_investments():
    with get_db_cursor() as cursor:
        cursor.execute("SELECT investment_mode, scheme_symbols FROM investment")
        investments = cursor.fetchall()
        return investments



