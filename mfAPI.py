import mftool
import my_logger

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
    def __init__(self, code=""):
        self.client = MfClient()
        self.code = code
        self.connected = self.client.connect()
        self.__nav = None



    def get_current_nav(self):
        if not self.connected:
            return None

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

