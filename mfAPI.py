import mftool

class MfData:
    def __init__(self):
        self.mf = mftool.Mftool()
        self.__mf_schemes = []

    @property
    def mf_schemes(self):
        schemes = self.mf.get_available_schemes("")
        self.__mf_schemes = list(schemes.items())[1:]
        return self.__mf_schemes

    def get_current_nav(self,code):
        try:
            nav = self.mf.get_scheme_quote(code)['nav']
        except TypeError:
            nav = 0

        return nav

