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

from . import downloader, constants
from .enums import Platform, Phase
from .exceptions import GetChromeDriverError, UnknownPlatformError, VersionUrlError, UnknownVersionError, \
    DownloadError, VersionError


class GetChromeDriver:

    def __init__(self, platform: Platform | None = None):
        if not platform:
            if pl.system() == 'Windows':
                self.__platform = self.__check_platform(Platform.win)
            elif pl.system() == 'Linux':
                self.__platform = self.__check_platform(Platform.linux)
            elif pl.system() == 'Darwin':
                self.__platform = self.__check_platform(Platform.mac)
        else:
            self.__platform = self.__check_platform(platform)

    def stable_version(self) -> str:
        """ Return the latest stable version """

        return self.__latest_version_by_phase(Phase.stable)

    def beta_version(self) -> str:
        """ Return the latest beta version """

        return self.__latest_version_by_phase(Phase.beta)

    def __latest_version_by_phase(self, phase: Phase) -> str:
        """
        Return the latest stable or latest beta version

        :param phase: Stable or beta
        """

        response = requests.get(constants.url_chromium)
        if not response.ok:
            raise GetChromeDriverError(f'Could not get {constants.url_chromium}')

        soup = BeautifulSoup(response.content, 'html.parser')
        ul = soup.select_one(constants.css_selector_versions)
        for li in ul:
            li_text = li.text.replace(u'\u00A0', ' ')
            if Phase.stable == phase:
                version_str = constants.latest_stable_version_str
            else:
                version_str = constants.latest_beta_version_str

            if li_text[:len(version_str)].lower() == version_str.lower():
                try:
                    version = li.a['href'].split('path=')[-1:][0][:-1]
                except TypeError:
                    raise UnknownVersionError('Could not find version')
                else:
                    self.__check_if_version_format_is_valid(version)
                    return version
        else:
            raise UnknownVersionError('Could not find version')

    def stable_version_url(self) -> str:
        """ Return the latest stable version url """

        return self.version_url(self.__latest_version_by_phase(Phase.stable))

    def beta_version_url(self) -> str:
        """ Return the latest beta version url """

        return self.version_url(self.__latest_version_by_phase(Phase.beta))

    def version_url(self, version: str) -> str:
        """
        Return the version download url

        :param version: Chromedriver version
        """

        self.__check_if_version_format_is_valid(version)
        arch = struct.calcsize('P') * 8
        arch_64 = 64
        chromedriver = 'chromedriver'
        zip_ext = '.zip'

        if self.__platform == Platform.win:
            # 64bit
            if arch == arch_64:
                try:
                    url = f'{constants.url_chromedriver_storage}/{version}/{chromedriver}_{Platform.win64}{zip_ext}'
                    self.__check_if_url_is_valid(url)
                    return url
                except VersionUrlError:
                    # No 64 bit, get 32 bit
                    pass
            # 32bit
            url = f'{constants.url_chromedriver_storage}/{version}/{chromedriver}_{Platform.win32}{zip_ext}'
            self.__check_if_url_is_valid(url)
            return url

        elif self.__platform == Platform.linux:
            # 64bit
            if arch == arch_64:
                try:
                    url = f'{constants.url_chromedriver_storage}/{version}/{chromedriver}_{Platform.linux64}{zip_ext}'
                    self.__check_if_url_is_valid(url)
                    return url
                except VersionUrlError:
                    # No 64 bit, get 32 bit
                    pass
            # 32bit
            url = f'{constants.url_chromedriver_storage}/{version}/{chromedriver}_{Platform.linux32}{zip_ext}'
            self.__check_if_url_is_valid(url)
            return url

        elif self.__platform == Platform.mac:
            # 64bit
            if arch == arch_64:
                try:
                    url = f'{constants.url_chromedriver_storage}/{version}/{chromedriver}_{Platform.mac64}{zip_ext}'
                    self.__check_if_url_is_valid(url)
                    return url
                except VersionUrlError:
                    # No 64 bit, get 32 bit
                    pass
            # 32bit
            url = f'{constants.url_chromedriver_storage}/{version}/{chromedriver}_{Platform.mac32}{zip_ext}'
            self.__check_if_url_is_valid(url)
            return url

    def download_stable_version(self, output_path: str | None = None, extract: bool = False):
        """
        Download the latest stable chromedriver version

        :param output_path: Path to download the driver to
        :param extract: Extract the downloaded driver or not
        """

        version = self.__latest_version_by_phase(Phase.stable)
        self.download_version(version=version, output_path=output_path, extract=extract)

    def download_beta_version(self, output_path: str | None = None, extract: bool = False):
        """
        Download the latest beta chromedriver version

        :param output_path: Path to download the driver to
        :param extract: Extract the downloaded driver or not
        """

        version = self.__latest_version_by_phase(Phase.beta)
        self.download_version(version=version, output_path=output_path, extract=extract)

    def download_version(self, version, output_path: str | None = None, extract: bool = False) -> str:
        """
        Download a chromedriver version

        :param version: Chromedriver version
        :param output_path: Path to download the driver to
        :param extract: Extract the downloaded driver or not
        """

        self.__check_if_version_format_is_valid(version)
        if not output_path:
            # on path is None,
            # ChromeDriver will be downloaded at e.g. chromedriver/88.0.4324.96/bin/chromedriver.exe
            output_path = self._output_path(version)

        # If path == webdriver/bin (or any other dir name)
        # ChromeDriver will be downloaded at webdriver/bin/chromedriver.exe

        def download(download_url: str, download_output_path: str) -> str:
            try:
                file_path, file_name = downloader.download(url=download_url, output_path=download_output_path)
            except (OSError, HTTPError, RequestException) as err:
                raise DownloadError(err)
            if extract:
                with zipfile.ZipFile(file_path, 'r') as zip_ref:
                    zip_ref.extractall(path=download_output_path)
                os.remove(file_path)
                if self.__platform == Platform.linux or self.__platform == Platform.mac:
                    os.chmod(f'{download_output_path}/chromedriver', 0o755)
            return download_output_path

        # Download the driver file and return the path of the driver file
        url = self.version_url(version)
        return download(download_url=url, download_output_path=output_path)

    def __check_if_url_is_valid(self, url: str):
        """
        Check if url is valid

        :param url: The driver download url
        """

        if requests.head(url).status_code != 200:
            raise VersionUrlError('Invalid url')

    def __check_if_version_format_is_valid(self, version: str):
        """
        Check if version format is valid

        :param version: Chromedriver version
        """

        split_version = version.split('.')
        for number in split_version:
            if not number.isnumeric():
                raise UnknownVersionError('Invalid version format')

    def __check_platform(self, platform: Platform) -> str:
        """
        Check if platform is valid

        :param platform: OS
        """

        platforms_list = [platform for platform in Platform]

        if platform not in platforms_list:
            raise UnknownPlatformError(f'Unknown platform, choose a platform from: {str(platforms_list)}')
        return platform

    def matching_version(self) -> str:
        """ Return a matching ChromeDriver version """

        all_chromedriver_versions = self.__get_all_chromedriver_versions()
        installed_chrome_version = self.__get_installed_chrome_version()
        for chromedriver_version in reversed(all_chromedriver_versions):
            if '.'.join(installed_chrome_version.split('.')[:-1]) == '.'.join(chromedriver_version.split('.')[:-1]):
                return chromedriver_version

    def auto_download(self, output_path: str | None = None, extract: bool = False) -> str:
        """
        Download ChromeDriver for the installed Chrome version on machine

        :param output_path: Path to download the driver to
        :param extract: Extract the downloaded driver or not
        """

        version = self.matching_version()
        if version == '' or version is None:
            raise VersionError('Unable to find a ChromeDriver version for the installed Chrome version')
        return self.download_version(version, output_path, extract)

    def install(self):
        """ Install ChromeDriver for the installed Chrome version on machine """

        output_path = self.auto_download(extract=True)
        path = os.path.join(os.path.abspath(os.getcwd()), output_path)
        os.environ['PATH'] += os.pathsep + os.pathsep.join([path])

    def __get_all_chromedriver_versions(self) -> list:
        """ Return a list with all ChromeDriver versions """

        key_texts = []
        versions = []

        with urlopen(constants.url_chromedriver_storage) as xml_file:
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

        if self.__platform == Platform.win:
            process = subprocess.Popen(
                ['reg', 'query', 'HKEY_CURRENT_USER\\SOFTWARE\\Google\\Chrome\\BLBeacon', '/v', 'version'],
                stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL)
            return process.communicate()[0].decode('UTF-8').split()[-1]

        elif self.__platform == Platform.linux:
            process = subprocess.Popen(
                ['google-chrome', '--version'],
                stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL)
            return process.communicate()[0].decode('UTF-8').split()[-1]

        elif self.__platform == Platform.mac:
            process = subprocess.Popen(
                ['/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', '--version'],
                stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL)
            return process.communicate()[0].decode('UTF-8').split()[-1]

    def _output_path(self, version: str) -> str:
        """
        Return the output path

        :param version: Chromedriver version
        """

        return f'chromedriver/{version}/bin'
