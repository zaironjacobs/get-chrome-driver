class Platforms:

    @property
    def win(self):
        return 'win'

    @property
    def linux(self):
        return 'linux'

    @property
    def mac(self):
        return 'mac'

    @property
    def win_32(self):
        return 'win32'

    @property
    def win_64(self):
        return 'win64'

    @property
    def linux_32(self):
        return 'linux32'

    @property
    def linux_64(self):
        return 'linux64'

    @property
    def mac_32(self):
        return 'mac32'

    @property
    def mac_64(self):
        return 'mac64'

    @property
    def list(self):
        return [self.win, self.linux, self.mac]
