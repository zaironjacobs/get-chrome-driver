class GetChromeDriverError(Exception):
    pass


class VersionUrlError(GetChromeDriverError):
    pass


class UnknownPlatformError(GetChromeDriverError):
    pass


class UnknownVersionError(GetChromeDriverError):
    pass


class DownloadError(GetChromeDriverError):
    pass


class VersionError(GetChromeDriverError):
    pass
