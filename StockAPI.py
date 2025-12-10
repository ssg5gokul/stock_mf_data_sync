import datetime
import nsetools

TODAY = str(datetime.date.today())
nse_stocks = nsetools.nse.Nse()

class StockData:
    def __init__(self, symbol=""):
        self.symbol = symbol
        self.__data = None
        self.__closing_value = None
        self.__last_refreshed = None

    @staticmethod
    def stock_symbols():
        stock_symbols = [(i, ) for i in nse_stocks.get_stock_codes()]
        return stock_symbols

    @property
    def data(self):
        self.__data = nse_stocks.get_quote(self.symbol)
        return self.__data


    @property
    def closing_value(self):
        try:
            self.__closing_value = self.data['close']
        except KeyError:
            self.__closing_value = None

        return self.__closing_value

