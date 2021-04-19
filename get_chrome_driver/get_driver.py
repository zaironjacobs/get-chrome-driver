import os
import requests
import zipfile
import platform as pl
import xml.etree.ElementTree as ElTree
import subprocess
import struct
from urllib.request import urlopen
from bs4 import BeautifulSoup

from requests.exceptions import RequestException
from requests.exceptions import HTTPError

from . import constants
from . import retriever
from .platforms import Platforms
from .phases import Phases
from .exceptions import GetChromeDriverError
from .exceptions import UnknownPlatformError
from .exceptions import VersionUrlError
from .exceptions import UnknownVersionError
from .exceptions import DownloadError
from .exceptions import VersionError


class GetChromeDriver:

    def __init__(self, platform=None) -> None:
        self.__platforms = Platforms()

        if not platform:
            if pl.system() == 'Windows':
                self.__platform = self.__check_platform(self.__platforms.win)
            elif pl.system() == 'Linux':
                self.__platform = self.__check_platform(self.__platforms.linux)
            elif pl.system() == 'Darwin':
                self.__platform = self.__check_platform(self.__platforms.mac)
        else:
            self.__platform = self.__check_platform(platform)

        self.__phases = Phases()

    def stable_version(self) -> str:
        """ Return the latest stable version """

        return self.__latest_version_by_phase('stable')

    def beta_version(self) -> str:
        """ Return the latest beta version """

        return self.__latest_version_by_phase('beta')

    def __latest_version_by_phase(self, phase) -> str:
        """ Return the latest stable or latest beta version """

        res = requests.get(constants.CHROMEDRIVER_CHROMIUM_URL)

        if res.status_code != 200:
            raise GetChromeDriverError('error: could not connect to ' + constants.CHROMEDRIVER_CHROMIUM_URL)

        soup = BeautifulSoup(res.content, 'html.parser')
        ul = soup.select_one(constants.CSS_VERSIONS_SELECTOR_UL)
        for li in ul:
            li_text = li.text.replace(u'\u00A0', ' ')
            if self.__phases.stable == phase:
                version_str = constants.LATEST_STABLE_VERSION_STR
            else:
                version_str = constants.LATEST_BETA_VERSION_STR

            if li_text[:len(version_str)].lower() == version_str.lower():
                try:
                    version = li.a['href'].split('path=')[-1:][0][:-1]
                except TypeError:
                    raise UnknownVersionError('error: could not find version')
                else:
                    self.__check_version(version)
                    return version

    def stable_version_url(self) -> str:
        """ Return the latest stable version url """

        return self.version_url(self.__latest_version_by_phase(self.__phases.stable))

    def beta_version_url(self) -> str:
        """ Return the latest beta version url """

        return self.version_url(self.__latest_version_by_phase(self.__phases.beta))

    def version_url(self, version) -> str:
        """ Return the version download url """

        self.__check_version(version)

        arch = struct.calcsize('P') * 8
        arch_64 = 64

        if self.__platform == self.__platforms.win:
            # 64bit
            if arch == arch_64:
                try:
                    url = (constants.CHROMEDRIVER_STORAGE_URL + '/' + version + '/' + constants.CHROMEDRIVER + '_'
                           + self.__platforms.win_64 + constants.ZIP_TYPE)
                    self.__check_url(url)
                    return url
                except VersionUrlError:
                    pass
            # 32bit
            url = (constants.CHROMEDRIVER_STORAGE_URL + '/' + version + '/' + constants.CHROMEDRIVER + '_'
                   + self.__platforms.win_32 + constants.ZIP_TYPE)
            self.__check_url(url)
            return url

        elif self.__platform == self.__platforms.linux:
            # 64bit
            if arch == arch_64:
                try:
                    url = (constants.CHROMEDRIVER_STORAGE_URL + '/' + version + '/' + constants.CHROMEDRIVER + '_'
                           + self.__platforms.linux_64 + constants.ZIP_TYPE)
                    self.__check_url(url)
                    return url
                except VersionUrlError:
                    pass
            # 32bit
            url = (constants.CHROMEDRIVER_STORAGE_URL + '/' + version + '/' + constants.CHROMEDRIVER + '_'
                   + self.__platforms.linux_32 + constants.ZIP_TYPE)
            self.__check_url(url)
            return url

        elif self.__platform == self.__platforms.mac:
            # 64bit
            if arch == arch_64:
                try:
                    url = (constants.CHROMEDRIVER_STORAGE_URL + '/' + version + '/' + constants.CHROMEDRIVER + '_'
                           + self.__platforms.mac_64 + constants.ZIP_TYPE)
                    self.__check_url(url)
                    return url
                except VersionUrlError:
                    pass
            # 32bit
            url = (constants.CHROMEDRIVER_STORAGE_URL + '/' + version + '/' + constants.CHROMEDRIVER + '_'
                   + self.__platforms.mac_32 + constants.ZIP_TYPE)
            self.__check_url(url)
            return url

    def download_stable_version(self, output_path=None, extract=False) -> None:
        """ Download the latest stable chromedriver version """

        version = self.__latest_version_by_phase(self.__phases.stable)
        self.download_version(version, output_path, extract)

    def download_beta_version(self, output_path=None, extract=False) -> None:
        """ Download the latest beta chromedriver version """

        version = self.__latest_version_by_phase(self.__phases.beta)
        self.download_version(version, output_path, extract)

    def download_version(self, version, output_path=None, extract=False) -> str:
        """ Download a chromedriver version """

        self.__check_version(version)

        if len(str(output_path)) == 0:
            # on path == '',
            # ChromeDriver will be downloaded in the current dir
            output_path = ''
        elif not output_path:
            # on path == None,
            # ChromeDriver will be downloaded at e.g. chromedriver/88.0.4324.96/bin/chromedriver.exe
            output_path = self._default_output_path(version)

        # on path == webdriver/bin (or any other dir name),
        # ChromeDriver will be downloaded at webdriver/bin/chromedriver.exe

        def download(download_url, download_path) -> str:
            try:
                output_path_with_file_name, file_name = retriever.download(url=download_url, output_path=download_path)
            except (OSError, HTTPError, RequestException) as err:
                raise DownloadError(err)
            if extract:
                with zipfile.ZipFile(output_path_with_file_name, 'r') as zip_ref:
                    zip_ref.extractall(path=download_path)
                os.remove(output_path_with_file_name)
                if self.__platform == self.__platforms.linux or self.__platform == self.__platforms.mac:
                    os.chmod(download_path + '/' + constants.CHROMEDRIVER, 0o755)
            return download_path

        # Download the driver file and return the relative dir path of the driver file
        url = self.version_url(version)
        return download(url, output_path)

    def __check_url(self, url) -> None:
        """ Check if url is valid """

        if requests.head(url).status_code != 200:
            raise VersionUrlError('error: Invalid url')

    def __check_version(self, version) -> None:
        """ Check if version format is valid """

        split_version = version.split('.')
        for number in split_version:
            if not number.isnumeric():
                raise UnknownVersionError('error: Invalid version format')

    def __check_platform(self, platform) -> str:
        """ Check if platform is valid """

        if platform not in self.__platforms.list:
            raise UnknownPlatformError('error: platform not recognized, choose a platform from: '
                                       + str(self.__platforms.list))
        return platform

    def matching_version(self):
        """ Return a matching ChromeDriver version """

        all_chromedriver_versions = self.__get_all_chromedriver_versions()
        installed_chrome_version = self.__get_installed_chrome_version()

        chromedriver_version_to_download = ''
        for chromedriver_version in reversed(all_chromedriver_versions):
            if '.'.join(installed_chrome_version.split('.')[:-1]) == '.'.join(chromedriver_version.split('.')[:-1]):
                chromedriver_version_to_download = chromedriver_version
                break
        return chromedriver_version_to_download

    def auto_download(self, output_path=None, extract=False) -> str:
        """ Download ChromeDriver for the installed Chrome version on machine """

        version = self.matching_version()
        if version == '' or version is None:
            raise VersionError('error: unable to find a ChromeDriver version for the installed Chrome version')

        return self.download_version(version, output_path, extract)

    def install(self) -> None:
        """ Install ChromeDriver for the installed Chrome version on machine """

        output_path = self.auto_download(extract=True)
        path = os.path.join(os.path.abspath(os.getcwd()), output_path)
        os.environ['PATH'] += os.pathsep + os.pathsep.join([path])

    def __get_all_chromedriver_versions(self) -> list:
        """ Return a list with all ChromeDriver versions """

        key_texts = []
        versions = []

        url = constants.CHROMEDRIVER_STORAGE_URL

        with urlopen(url) as xml_file:
            tree = ElTree.parse(xml_file)
            root = tree.getroot()

            for root_item in root:
                # Remove namespace
                root_item.tag = root_item.tag.split('}', 1)[1]

            for content in root.findall('Contents'):

                for content_item in content:
                    # Remove namespace
                    content_item.tag = content_item.tag.split('}', 1)[1]

                    key_texts.append(content.find('Key').text)

        for text in key_texts:

            version = ''
            for char in text:
                if char.isnumeric() or char == '.':
                    version += char
                else:
                    break

            if len(version) < 1:
                continue

            versions.append(version)

        return list(dict.fromkeys(versions))

    def __get_installed_chrome_version(self) -> str:
        """ Return the installed Chrome version on the machine """

        if self.__platform == self.__platforms.win:
            process = subprocess.Popen(
                ['reg', 'query', 'HKEY_CURRENT_USER\\SOFTWARE\\Google\\Chrome\\BLBeacon', '/v', 'version'],
                stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL)
            return process.communicate()[0].decode('UTF-8').split()[-1]

        elif self.__platform == self.__platforms.linux:
            process = subprocess.Popen(
                ['google-chrome', '--version'],
                stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL)
            return process.communicate()[0].decode('UTF-8').split()[-1]

        elif self.__platform == self.__platforms.mac:
            process = subprocess.Popen(
                ['/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', '--version'],
                stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL)
            return process.communicate()[0].decode('UTF-8').split()[-1]

    def _default_output_path(self, version) -> str:
        """ Return the default output path """

        return constants.CHROMEDRIVER + '/' + version + '/' + 'bin'
