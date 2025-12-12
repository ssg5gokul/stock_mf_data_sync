from StockAPI import StockData
from mfAPI import MfData
import DAO

mfunds = MfData()
stock = StockData()

def insert_mutual_funds_symbols():
    """It deletes the past data and inserts new."""
    DAO.delete_funds()
    DAO.insert_funds(mfunds.mf_schemes())

def insert_stock_etf_symbols():
    """It deletes the past data and inserts new."""
    DAO.delete_stocks()
    DAO.insert_stocks(stock.stock_symbols())

def update_current_value():
    DAO.savings_summary()
    invst = DAO.get_investments()

    for i in invst:
        mode = i.get('investment_mode')
        code = i.get('scheme_symbols').strip()
        if mode == 'Mutual Funds':
            mfunds.code = code
            current_value = mfunds.get_current_nav()

        elif mode == 'Stocks':
            stock.symbol = code
            current_value = stock.closing_value

        else:
            current_value = 0

        DAO.update_current_value(code, current_value)





