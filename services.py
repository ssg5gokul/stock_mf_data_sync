from StockAPI import StockData
from mfAPI import MfData
import DAO
import my_logger


logger_services = my_logger.config_logger(__name__)

def insert_mutual_funds_symbols():
    """It deletes the past data and inserts new."""
    mfunds = MfData()
    scheme_codes = mfunds.client.mf_schemes

    if len(scheme_codes) > 0:
        DAO.delete_funds()
        DAO.insert_funds(scheme_codes)

    else:
        logger_services.warning("No scheme codes are available to be inserted. Please check mfAPI logs for further "
                             "information.")

def insert_stock_etf_symbols():
    """It deletes the past data and inserts new."""
    stock = StockData()
    stock_symbols = stock.client.stock_symbols
    if len(stock_symbols) > 0:
        DAO.delete_stocks()
        DAO.insert_stocks(stock_symbols)

    else:
        logger_services.warning("No scheme codes are available to be inserted. Please check StockAPI logs for further "
                             "information.")


def update_current_value():
    mfunds = MfData()
    stock = StockData()

    DAO.investment_growth()
    invest = DAO.get_investments()

    for inv in invest:
        try:
            inv_id = inv.get('investment_id')
            mode = inv.get('investment_mode')
            code = inv.get('market_code').strip()
            if mode == 'Mutual Funds':
                mfunds.code = code
                current_value = mfunds.get_current_nav()

            elif mode == 'Stocks':
                stock.symbol = code
                current_value = stock.closing_value

            else:
                logger_services.error(f"Received an incorrect mode of investment: {mode} for code:{code}.")
                continue

            if current_value is None:
                logger_services.warning(f"Skipping update for {code} due to missing current value")
                continue

            DAO.update_current_value(inv_id, current_value)

        except Exception as e:
            logger_services.error(
                f"Failed to update current value for {inv} | {e}"
            )