import pandas as pd
import yfinance
import my_logger
import nsetools
from nsefin import nse
from datetime import datetime


TODAY = str(datetime.today())
logger_StockAPI = my_logger.config_logger(__name__)

class StockClient:
    def __init__(self):
        self.nse_stocks = None
        self.nse_etf = None
        self.stock_symbols = []
        self.etf_symbols = []

    def connect(self):
        try:
            self.nse_stocks = nsetools.nse.Nse()
            self.nse_etf = nse
            return True

        except Exception as e:
            logger_StockAPI.error(f"ConnectionError: Failed to resolve 'nseindia.com' - {e}")
            return False

    def get_stock_symbols(self):
        try:
            self.stock_symbols = [(i,) for i in self.nse_stocks.get_stock_codes()]

        except AttributeError as e:
            logger_StockAPI.warning(f"No stock symbols were returned due to error - {e}")

        return self.stock_symbols

    def get_etf_symbols(self):
        try:
            etf_details = self.nse_etf.get_etf_list()
            self.etf_symbols = [(symbol['Symbol'],) for symbol in etf_details.to_dict(orient='records')]

        except AttributeError as e:
            logger_StockAPI.warning(f"No stock symbols were returned due to error - {e}")

        return self.etf_symbols


class StockData:
    def __init__(self, client, symbol=""):
        self.client = client
        self.symbol = symbol
        self.data = self.get_data()
        self.closing_value = self.data.get("close") if self.data else None


    def get_data(self):
        try:
            return self.client.nse_stocks.get_quote(self.symbol)

        except Exception as e:
            logger_StockAPI.info(f"No data returned with error - {e}")


    # def get_closing_value(self):
    #     try:
    #         self.closing_value = self.data['close']
    #
    #     except KeyError:
    #         self.closing_value = None
    #         logger_StockAPI.debug(f"There is no closing value for {self.symbol} on {TODAY}.")
    #
    #     return self.closing_value

    def get_historical_closing_values(self, st_date):
        try:
            df = yfinance.download(
                tickers=f"{self.symbol}.NS",
                start=st_date.strftime('%Y-%m-%d'),
                end=datetime.today().strftime('%Y-%m-%d')
            )

            if df.empty:
                return None

            df = df[['Close']].reset_index()
            return df

        except Exception as e:
            logger_StockAPI.error(f"Error receiving historical data - {e}")
            return None


s = StockData()
s.client.nse_stocks.get_quote()