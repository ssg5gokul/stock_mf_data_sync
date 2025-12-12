import mftool

mf = mftool.Mftool()
class MfData:
    def __init__(self, code=""):
        self.code = code
        self.__nav = 0

    @staticmethod
    def mf_schemes():
        schemes = mf.get_available_schemes("")
        mf_schemes = list(schemes.items())[1:]
        return mf_schemes

    def get_current_nav(self):
        try:
            nav = mf.get_scheme_quote(self.code)['nav']
        except TypeError:
            nav = 0

        return nav

