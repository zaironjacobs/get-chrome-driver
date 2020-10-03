class Platforms:

    def __init__(self):
        self.win = self.__win()
        self.linux = self.__linux()
        self.mac = self.__mac()
        self.list = self.__list()

        self.win_arch = self.__win_arch()
        self.linux_arch = self.__linux_arch()
        self.mac_arch = self.__mac_arch()

    def __win(self):
        return 'win'

    def __linux(self):
        return 'linux'

    def __mac(self):
        return 'mac'

    def __win_arch(self):
        return 'win32'

    def __linux_arch(self):
        return 'linux64'

    def __mac_arch(self):
        return 'mac64'

    def __list(self):
        return [self.__win(), self.__linux(), self.__mac()]
