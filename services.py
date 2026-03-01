import pandas as pd
from StockAPI import StockData, StockClient
from mfAPI import MfData, MfClient
import DAO
import my_logger


logger_services = my_logger.config_logger(__name__)
stock_client = StockClient()
stock_client.connect()


mf_client = MfClient()
mf_client.connect()


def insert_mutual_funds_symbols():
    """It deletes the past data and inserts new."""
    mfunds = MfData(mf_client)
    scheme_codes = mfunds.client.mf_schemes

    if len(scheme_codes) > 0:
        DAO.delete_funds()
        DAO.insert_funds(scheme_codes)

    else:
        logger_services.warning("No scheme codes are available to be inserted. Please check mfAPI logs for further "
                             "information.")

def insert_stock_etf_symbols():
    """It deletes the past data and inserts new."""
    stock = StockData(stock_client)
    stock_symbols = stock.client.get_stock_symbols()
    etf_symbols = stock.client.get_etf_symbols()
    symbols = stock_symbols + etf_symbols

    if len(symbols) > 0:
        DAO.delete_stocks()
        DAO.insert_stocks(symbols)

    else:
        logger_services.warning("No scheme codes are available to be inserted. Please check StockAPI logs for further "
                             "information.")


def update_historic_value():
    invest = DAO.get_investments()
    DAO.delete_historical_value()

    for inv in invest:
        try:
            st_date = inv.get('start_date')
            inv_id = inv.get('investment_id')
            mode = (inv.get('investment_mode') or "").lower()
            code = inv.get('market_code').strip()

            if mode == 'mutual funds':
                mfunds = MfData(client=mf_client, code=code)
                value_datewise_df = mfunds.get_historic_nav(st_date=st_date)

            elif mode == 'stocks':
                stock = StockData(client=stock_client, symbol=code)
                value_datewise_df = stock.get_historical_closing_values(st_date=st_date)

            else:
                logger_services.error(f"Received an incorrect mode of investment: {mode} for code:{code}.")
                continue

            if value_datewise_df is None:
                logger_services.warning(f"Skipping update for {code} due to missing historic value")
                continue

            value_datewise_df['Date'] = value_datewise_df['Date'].dt.strftime('%Y-%m-%d')
            value_datewise_df.insert(loc=1, column="investment_id", value=inv_id)
            results = list(value_datewise_df.itertuples(index=False, name=None))

            DAO.insert_historical_value(results)

        except Exception as e:
            logger_services.error(
                f"Failed to update current value for {inv} | {e}"
            )