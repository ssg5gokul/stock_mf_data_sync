import my_logger
import datetime
import nsetools

TODAY = str(datetime.date.today())
logger_StockAPI = my_logger.config_logger(__name__)

class StockClient:
    def __init__(self):
        self.nse_stocks = None
        self.__stock_symbols = []

    def connect(self):
        try:
            self.nse_stocks = nsetools.nse.Nse()
            return True

        except Exception as e:
            logger_StockAPI.error(f"ConnectionError: Failed to resolve 'nseindia.com' - {e}")
            return False

    @property
    def stock_symbols(self):
        try:
            self.__stock_symbols = [(i,) for i in self.nse_stocks.get_stock_codes()]

        except AttributeError as e:
            logger_StockAPI.warning(f"No stock symbols were returned due to error - {e}")

        return self.__stock_symbols


class StockData:
    def __init__(self, symbol=""):
        self.client = StockClient()
        self.connected = self.client.connect()
        self.symbol = symbol
        self.__data = None
        self.__closing_value = None
        self.__last_refreshed = None

    @property
    def data(self):
        try:
            self.__data = self.client.nse_stocks.get_quote(self.symbol)

        except Exception as e:
            logger_StockAPI.info(f"No data returned with error - {e}")

        return self.__data


    @property
    def closing_value(self):
        try:
            self.__closing_value = self.data['close']

        except KeyError:
            self.__closing_value = None
            logger_StockAPI.debug(f"There is no closing value for {self.symbol} on {TODAY}.")

        return self.__closing_value

