from fastapi import FastAPI, Query
from StockAPI import StockData
from mfAPI import MfData
import DB_helper

app = FastAPI()
mf = MfData()
stock = StockData()

@app.post("/mututal_funds_symbols")
def insert_mutual_funds_symbols():
    """It deletes the past data and inserts new."""
    DB_helper.delete_funds()
    DB_helper.insert_funds(mf.mf_schemes)

@app.post("/stock_etf_symbols")
def insert_stock_etf_symbols():
    """It deletes the past data and inserts new."""
    DB_helper.delete_stocks()
    DB_helper.insert_stocks(stock.stock_symbols())


@app.put("/current_value")
def update_current_value():
    DB_helper.savings_summary()
    invst = DB_helper.get_investments()

    for i in invst:
        mode = i.get('investment_mode')
        code = i.get('scheme_symbols').strip()
        if mode == 'Mutual Funds':
            current_value = mf.get_current_nav(code)

        elif mode == 'Stocks':
            stock.symbol = code
            current_value = stock.closing_value

        else:
            current_value = 0

        DB_helper.update_current_value(code, current_value)





