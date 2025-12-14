import mysql.connector
import my_logger
from datetime import date
from mysql.connector import Error
from contextlib import contextmanager

logger_DAO = my_logger.config_logger(__name__)


@contextmanager
def get_db_cursor(commit=False):
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="expense_manager"
    )

    if connection.is_connected():
        logger_DAO.debug("DB Connection is established")

    else:
        logger_DAO.error("DB Connection couldn't be established")

    cursor = connection.cursor(dictionary=True)

    # yield cursor
    # connection.commit()
    #
    # cursor.close()
    # connection.close()

    try:
        yield cursor
        if commit:
            connection.commit()

    except Exception:
        connection.rollback()
        logger_DAO.exception("Database transaction failed")
        raise

    finally:
        cursor.close()
        connection.close()


def insert_funds(schemes):
    with get_db_cursor(commit=True) as cursor:
        cursor.executemany("insert into asset_master (scheme_symbol, scheme_name, asset_type) values (%s, %s, "
                           "'Mutual Funds')", schemes)

        if cursor.rowcount == 0:
            logger_DAO.warning(
                f"No funds inserted on {date.today()}"
            )

        else:
            logger_DAO.info(f"Inserted {cursor.rowcount} new funds into asset_master table.")


def delete_funds():
    with get_db_cursor(commit=True) as cursor:
        cursor.execute("delete from asset_master where asset_type='Mutual Funds'")

        deleted = cursor.rowcount

    logger_DAO.info(f"Deleted {deleted} funds from the asset_master table.")


def insert_stocks(stocks):
    with get_db_cursor(commit=True) as cursor:
        cursor.executemany("insert into asset_master (scheme_symbol, asset_type) values (%s, 'Stocks')", stocks)

        if cursor.rowcount == 0:
            logger_DAO.warning(
                f"No Stocks inserted on {date.today()}"
            )

    logger_DAO.info(f"Inserted {cursor.rowcount} new stock symbols into asset_master table.")


def delete_stocks():
    with get_db_cursor(commit=True) as cursor:
        cursor.execute("delete from asset_master where asset_type='Stocks'")

        deleted = cursor.rowcount

    logger_DAO.info(f"Deleted {deleted} stocks from the asset_master table.")


def savings_summary():
    with get_db_cursor(commit=True) as cursor:
        cursor.callproc('set_investment_growth_value')

        if cursor.rowcount == 0:
            logger_DAO.warning(
                f"No stock/fund codes were inserted on {date.today()}"
            )

    logger_DAO.info("Inserted the invested stock/fund codes, and initialized the current value as 0.")


def update_current_value(code, val):
    with get_db_cursor(commit=True) as cursor:
        cursor.execute("update investment_growth set current_value =%s where scheme_symbols = %s and `date`= %s",
                       (val, code, date.today()))

        if cursor.rowcount == 0:
            logger_DAO.warning(
                f"No row updated for {code} on {date.today()}"
            )

    logger_DAO.info("Updated the daily value of the invested stock/funds.")


def get_investments():
    with get_db_cursor() as cursor:
        cursor.execute("SELECT investment_mode, scheme_symbols FROM investment_growth where `date`=CURDATE()")
        investments = cursor.fetchall()
        return investments
