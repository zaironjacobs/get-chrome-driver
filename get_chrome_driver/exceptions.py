class GetChromeDriverError(Exception):
    pass


class ReleaseUrlError(GetChromeDriverError):
    pass


class UnknownPlatformError(GetChromeDriverError):
    pass


class UnknownReleaseError(GetChromeDriverError):
    pass


class DownloadError(GetChromeDriverError):
    pass
