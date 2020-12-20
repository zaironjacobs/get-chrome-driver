class Platforms:

    def __init__(self):
        self.win = self.__win()
        self.linux = self.__linux()
        self.mac = self.__mac()

        self.list = self.__list()

        self.win_32 = self.__win_32()
        self.win_64 = self.__win_64()
        self.linux_32 = self.__linux_32()
        self.linux_64 = self.__linux_64()
        self.mac_32 = self.__mac_32()
        self.mac_64 = self.__mac_64()

    def __win(self):
        return 'win'

    def __linux(self):
        return 'linux'

    def __mac(self):
        return 'mac'

    def __win_32(self):
        return 'win32'

    def __win_64(self):
        return 'win64'

    def __linux_32(self):
        return 'linux32'

    def __linux_64(self):
        return 'linux64'

    def __mac_32(self):
        return 'mac32'

    def __mac_64(self):
        return 'mac64'

    def __list(self):
        return [self.__win(), self.__linux(), self.__mac()]
