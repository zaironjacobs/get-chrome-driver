import typer

from get_chrome_driver import __version__
from get_chrome_driver.enums import Phase, OsPlatform
from get_chrome_driver.exceptions import GetChromeDriverError
from get_chrome_driver.get_driver import GetChromeDriver

app = typer.Typer(name="Get ChromeDriver", add_completion=False)
get_driver = GetChromeDriver()


@app.command()
def main(
    beta_version: bool = typer.Option(
        default=False, help="Print the beta version", show_default=False
    ),
    stable_version: bool = typer.Option(
        default=False, help="Print the stable version", show_default=False
    ),
    latest_urls: bool = typer.Option(
        default=False,
        help="print the beta and stable version download urls for all platforms",
        show_default=False,
    ),
    version_url: str = typer.Option(
        default=None, help="Print the version download url", show_default=False
    ),
    beta_url: bool = typer.Option(
        default=False, help="Print the beta version download url", show_default=False
    ),
    stable_url: bool = typer.Option(
        default=False, help="Print the stable version download url", show_default=False
    ),
    auto_download: bool = typer.Option(
        default=False,
        help="Download a ChromeDriver version for the installed Chrome Version",
        show_default=False,
    ),
    download_beta: bool = typer.Option(
        default=False, help="Download beta version", show_default=False
    ),
    download_stable: bool = typer.Option(
        default=False, help="Download stable version", show_default=False
    ),
    download_version: str = typer.Option(
        default=None, help="Download a specific version", show_default=False
    ),
    extract: bool = typer.Option(
        default=False, help="Extract the compressed driver file", show_default=False
    ),
    driver_filename: bool = typer.Option(
        default=False, help="Driver filename", show_default=False
    ),
    chromium: bool = typer.Option(
        default=False,
        help="Auto download will look for the installed Chromium version instead of Chrome.",
        show_default=False,
    ),
    version: bool = typer.Option(
        default=False, help="Application version", show_default=False
    ),
):
    """
    Main.
    """

    if beta_version:
        __print_latest_version(phase=Phase.beta)

    elif stable_version:
        __print_latest_version(phase=Phase.stable)

    elif latest_urls:
        __print_latest_urls()

    elif version_url:
        __print_version_url(version=version_url)

    elif beta_url:
        __print_latest_url(phase=Phase.beta)

    elif stable_url:
        __print_latest_url(phase=Phase.stable)

    elif auto_download:
        __auto_download(extract=extract, chromium=chromium)

    elif download_beta:
        __download_latest_version(phase=Phase.beta, extract=extract)

    elif download_stable:
        __download_latest_version(phase=Phase.stable, extract=extract)

    elif download_version:
        __download_version(version=download_version, extract=extract)

    elif driver_filename:
        print(get_driver.driver_filename())

    elif version:
        print(f"v{__version__}")


def __print_latest_version(phase: Phase):
    """
    Print latest stable version or latest beta version.

    :param phase: Stable or beta.
    """

    error = "No latest version found"
    if phase == Phase.beta:
        try:
            print(get_driver.beta_version())
        except GetChromeDriverError:
            print(error)
    elif phase == Phase.stable:
        try:
            print(get_driver.stable_version())
        except GetChromeDriverError:
            print(error)
    else:
        print(error)


def __print_latest_urls():
    """
    Print the stable and beta url version for all platforms.
    """

    get_driver_win = GetChromeDriver(OsPlatform.win)
    get_driver_linux = GetChromeDriver(OsPlatform.linux)
    get_driver_mac = GetChromeDriver(OsPlatform.mac)
    get_drivers = {
        "Windows": get_driver_win,
        "Linux": get_driver_linux,
        "macOS": get_driver_mac,
    }

    result = ""
    for index, (key, value) in enumerate(get_drivers.items()):
        try:
            result += f"Latest beta and stable version for {key}:\n"
            result += f"stable : {value.stable_version_url()}\n"
            result += f"beta   : {value.beta_version_url()}"
            if index < len(get_drivers) - 1:
                result += "\n"
        except GetChromeDriverError:
            continue

    print(result)


def __print_version_url(version: str):
    """
    Print the url of a version.

    :param version: Chromedriver version.
    """

    error = "Could not find version url"

    try:
        print(get_driver.version_url(version))
    except GetChromeDriverError:
        print(error)


def __print_latest_url(phase: Phase):
    """
    Print latest stable url or latest beta url.

    :param phase: Stable or beta.
    """

    error = "Could not find version url"

    if phase == Phase.beta:
        try:
            print(get_driver.beta_version_url())
        except GetChromeDriverError:
            print(error)
    elif phase == Phase.stable:
        try:
            print(get_driver.stable_version_url())
        except GetChromeDriverError:
            print(error)


def __auto_download(extract: bool, chromium: bool):
    """
    Auto download driver.

    :param extract: Extract the downloaded driver or not.
    :param chromium: Look for the installed Chromium version instead of Chrome.
    """

    try:
        get_driver.auto_download(extract=extract, chromium=chromium)
        print("Download finished")
    except GetChromeDriverError:
        print("An error occurred at downloading")


def __download_latest_version(phase: Phase, extract: bool):
    """
    Download the driver for the stable version or beta version.

    :param phase: Stable or beta.
    :param extract: Extract the downloaded driver or not.
    """

    download_complete = "Download complete"
    beta_error = "Could not download beta version"
    stable_error = "Could not download stable version"

    if phase == Phase.beta:
        try:
            get_driver.download_beta_version(extract=extract)
            print(download_complete)
        except GetChromeDriverError:
            print(beta_error)
    elif phase == Phase.stable:
        try:
            get_driver.download_stable_version(extract=extract)
            print(download_complete)
        except GetChromeDriverError:
            print(stable_error)


def __download_version(version: str, extract: bool):
    """
    Download driver version.

    :param version: Chromedriver version.
    :param extract: Extract the downloaded driver or not.
    """

    try:
        get_driver.download_version(version=version, extract=extract)
        print("Download finished")
    except GetChromeDriverError:
        print("Could not download version")
