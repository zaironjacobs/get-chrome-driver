import requests
import zipfile
from bs4 import BeautifulSoup

from requests.exceptions import RequestException
from requests.exceptions import HTTPError

from . import constants
from .platforms import Platforms
from . import retriever
from .phase import Phase
from .exceptions import GetChromeDriverError
from .exceptions import UnknownPlatformError
from .exceptions import ReleaseUrlError
from .exceptions import ReleaseVersionError
from .exceptions import UnknownReleaseError
from .exceptions import DownloadError


class GetChromeDriver:

    def __init__(self, platform) -> None:
        self.__available_platforms = Platforms()
        self.__current_set_platform = self.__check_platform(platform)
        self.__phases = Phase()

    def stable_release_version(self) -> str:
        """ Return the latest stable release version """

        return self.__latest_release_version('stable')

    def beta_release_version(self) -> str:
        """ Return the latest beta release version """

        return self.__latest_release_version('beta')

    def __latest_release_version(self, phase) -> str:
        """ Return the stable or beta release version """

        result = requests.get(constants.CHROMEDRIVER_CHROMIUM_URL)
        soup = BeautifulSoup(result.content, 'html.parser')
        ul = soup.select_one(constants.UL_RELEASES_SELECTOR)
        for li in ul:
            li_text = li.text.replace(u'\u00A0', ' ')
            if self.__phases.stable == phase:
                release_str = constants.LATEST_STABLE_RELEASE_STR
            else:
                release_str = constants.LATEST_BETA_RELEASE_STR

            if li_text[:len(release_str)].lower() == release_str.lower():
                try:
                    release = li.a['href'].split('path=')[-1:][0][:-1]
                except TypeError:
                    raise ReleaseVersionError('error: could not find release version')
                else:
                    self.__check_release(release)
                    return release

    def stable_release_url(self) -> str:
        """ Return the latest stable release url """

        return self.release_url(self.__latest_release_version(self.__phases.stable))

    def beta_release_url(self) -> str:
        """ Return the latest beta release url """

        return self.release_url(self.__latest_release_version(self.__phases.beta))

    def release_url(self, release) -> str:
        """ Return the release download url """

        self.__check_release(release)

        url = ''
        if self.__current_set_platform == self.__available_platforms.win:
            url = constants.CHROMEDRIVER_STORAGE_URL + '/' + release + '/' + constants.FILE_NAME_CHROMEDRIVER_WIN_ZIP
        elif self.__current_set_platform == self.__available_platforms.linux:
            url = constants.CHROMEDRIVER_STORAGE_URL + '/' + release + '/' + constants.FILE_NAME_CHROMEDRIVER_LINUX_ZIP
        elif self.__current_set_platform == self.__available_platforms.mac:
            url = constants.CHROMEDRIVER_STORAGE_URL + '/' + release + '/' + constants.FILE_NAME_CHROMEDRIVER_MAC_ZIP

        self.__check_url(url)

        return url

    def download_stable_release(self, output_path=None, extract=False) -> None:
        """ Download the latest stable chromedriver release """

        release = self.__latest_release_version(self.__phases.stable)
        self.download_release(release, output_path, extract)

    def download_beta_release(self, output_path=None, extract=False) -> None:
        """ Download the latest stable chromedriver release """

        release = self.__latest_release_version(self.__phases.beta)
        self.download_release(release, output_path, extract)

    def download_release(self, release, output_path=None, extract=False) -> None:
        """ Download a chromedriver release """

        self.__check_release(release)
        url = self.release_url(release)

        def download(platform_arch):
            if output_path is None:
                output_path_no_file_name = constants.DIR_DOWNLOADS + '/' + release + '/' + platform_arch
            else:
                output_path_no_file_name = output_path

            try:
                output_path_with_file_name, file_name = retriever.download(url=url,
                                                                           output_path=output_path_no_file_name)
            except (OSError, HTTPError, RequestException) as err:
                raise DownloadError(err)

            if extract:
                with zipfile.ZipFile(output_path_with_file_name, 'r') as zip_ref:
                    zip_ref.extractall(path=output_path_no_file_name)

        if self.__current_set_platform == self.__available_platforms.win:
            download(self.__available_platforms.win_arch)
        elif self.__current_set_platform == self.__available_platforms.linux:
            download(self.__available_platforms.linux_arch)
        elif self.__current_set_platform == self.__available_platforms.mac:
            download(self.__available_platforms.mac_arch)

    def __check_url(self, url) -> None:
        """ Check if url is valid """

        if requests.head(url).status_code != 200:
            raise ReleaseUrlError('error: Invalid url')

    def __check_release(self, release) -> None:
        """ Check if release format is valid """

        split_release = release.split('.')

        for number in split_release:
            if not number.isnumeric():
                raise UnknownReleaseError('error: Invalid release format')

    def __check_platform(self, platform) -> str:
        """ Check if platform is valid """

        if platform not in self.__available_platforms.list:
            raise UnknownPlatformError('error: platform not recognized, choose a platform from: '
                                       + str(self.__available_platforms.list))
        return platform
