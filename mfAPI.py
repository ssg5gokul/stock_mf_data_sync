import mftool
import pandas as pd

import my_logger
from datetime import datetime

logger_mfAPI = my_logger.config_logger(__name__)

class MfClient:
    def __init__(self):
        self.mf = None
        self.__mf_schemes = []

    def connect(self):
        try:
            self.mf = mftool.Mftool()
            return True

        except Exception as e:
            logger_mfAPI.error(f"Failed to fetch data from 'www.amfiindia.com' with error - {e}")
            return False

    @property
    def mf_schemes(self):
        try:
            schemes = self.mf.get_available_schemes("")
            self.__mf_schemes = list(schemes.items())[1:]

        except AttributeError as e:
            schemes = []
            logger_mfAPI.error(f"No scheme codes were returned due to error - {e}")

        return self.__mf_schemes


class MfData:
    def __init__(self, client, code=""):
        self.client = client
        self.code = code
        self.__nav = None
        self.__hist_nav = []


    def get_current_nav(self):
        try:
            quote = self.client.mf.get_scheme_quote(self.code)
            self.__nav  = quote['nav']

            if self.__nav is None:
                logger_mfAPI.warning(
                    f"No NAV available for scheme {self.code}"
                )

        except Exception as e:
            self.__nav = None
            logger_mfAPI.error(
                f"Failed to fetch NAV for scheme {self.code} | {e}"
            )

        return self.__nav

    def get_historic_nav(self, st_date):
        try:
            quote = self.client.mf.get_scheme_historical_nav_for_dates(code=self.code,start_date=st_date.strftime('%d-%m-%Y'),
                                                                       end_date= datetime.today().strftime('%d-%m-%Y'))
            self.__hist_nav = pd.DataFrame(quote['data'])
            self.__hist_nav['date'] = pd.to_datetime(self.__hist_nav['date'], dayfirst=True)
            self.__hist_nav.rename(columns={'date': 'Date', 'nav': 'Close'}, inplace=True)

        except Exception as e:
            self.__hist_nav = None
            logger_mfAPI.error(
                f"Failed to fetch NAV for scheme {self.code} | {e}"
            )

        return self.__hist_nav
