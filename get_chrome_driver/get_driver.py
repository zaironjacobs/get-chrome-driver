import os
import platform as pl
import shutil
import struct
import subprocess
import xml.etree.ElementTree as ElTree
import zipfile
from urllib.request import urlopen

import requests
from requests.exceptions import HTTPError
from requests.exceptions import RequestException

from get_chrome_driver import downloader, constants
from get_chrome_driver.enums import Platform, Phase, OsPlatform
from get_chrome_driver.exceptions import (
    GetChromeDriverError,
    UnknownPlatformError,
    UnknownVersionError,
    DownloadError,
    VersionError,
    VersionUrlError,
)


class GetChromeDriver:
    def __init__(self, os_platform: OsPlatform = None):
        self.__os_platforms_list = [os_platform for os_platform in OsPlatform]

        if not os_platform:
            if pl.system() == "Windows":
                self.__os_platform = OsPlatform.win
            elif pl.system() == "Linux":
                self.__os_platform = OsPlatform.linux
            elif pl.system() == "Darwin":
                self.__os_platform = OsPlatform.mac
        else:
            if self.__check_if_os_platform_is_valid(os_platform):
                self.__os_platform = os_platform
        if not self.__os_platform:
            raise UnknownPlatformError("Unknown OS platform.")

        self.__arch = struct.calcsize("P") * 8
        self.__chromedriver_str = "chromedriver"
        self.__zip_ext = ".zip"

    def driver_filename(self) -> str:
        """
        Driver filename.
        """

        if self.__os_platform == OsPlatform.win:
            return "chromedriver.exe"
        elif self.__os_platform == OsPlatform.linux:
            return "chromedriver"
        elif self.__os_platform == OsPlatform.mac:
            return "chromedriver"

        raise UnknownPlatformError("Unknown OS platform.")

    def stable_version(self) -> str:
        """
        Return the latest stable version.
        """

        return self.__latest_version_by_phase(Phase.stable)

    def beta_version(self) -> str:
        """
        Return the latest beta version.
        """

        return self.__latest_version_by_phase(Phase.beta)

    def __latest_version_by_phase(self, phase: Phase) -> str:
        """
        Return the latest stable or latest beta version.

        :param phase: Stable or beta.
        """

        response = requests.get(constants.LAST_KNOWN_GOOD_VERSIONS_URL)
        if not response.ok:
            raise GetChromeDriverError(
                f"Could not fetch from {constants.LAST_KNOWN_GOOD_VERSIONS_URL}."
            )

        try:
            if phase == Phase.stable:
                return response.json()["channels"]["Stable"]["version"]
            if phase == Phase.beta:
                return response.json()["channels"]["Beta"]["version"]
        except KeyError:
            raise UnknownVersionError("Could not find version.")

        raise UnknownVersionError("Could not find version.")

    def stable_version_url(self) -> str:
        """
        Return the latest stable version URL.
        """

        return self.version_url(self.__latest_version_by_phase(Phase.stable))

    def beta_version_url(self) -> str:
        """
        Return the latest beta version URL.
        """

        return self.version_url(self.__latest_version_by_phase(Phase.beta))

    def __version_url_for_platform(
        self,
        new_api_known_good_versions: list,
        version: str,
        platform_64: str,
        platform_32: str = None,
        is_mac: bool = False,
    ) -> str:
        """
        Return the version download URL for a platform.

        :param new_api_known_good_versions: The latest known good driver versions from the new api.
        :param version: Chromedriver version.
        :param platform_64: 64bit platform.
        :param platform_32: 32bit platform.
        """

        # New api
        for driver_version in new_api_known_good_versions:
            if driver_version.get("version") == version:
                drivers = driver_version.get("downloads").get("chromedriver")

                # 64
                if self.__arch == 64:
                    for driver in drivers or []:
                        if is_mac:
                            if pl.processor() == "arm":
                                _platform_64 = Platform.mac_arm64.value
                            else:
                                _platform_64 = Platform.mac_x64.value
                        else:
                            _platform_64 = platform_64

                        if driver.get("platform") == _platform_64:
                            url = driver.get("url")
                            if url and self.__check_if_url_is_valid(url):
                                return url

                # 32
                if platform_32 and not is_mac:
                    for driver in drivers or []:
                        if driver.get("platform") == platform_32:
                            url = driver.get("url")
                            if url and self.__check_if_url_is_valid(url):
                                return url

        # Old chromedriver storage
        # 64
        if self.__arch == 64:
            url = f"{constants.CHROMEDRIVER_STORAGE_URL}/{version}/{self.__chromedriver_str}_{platform_64}{self.__zip_ext}"
            if self.__check_if_url_is_valid(url):
                return url

        # 32
        if platform_32:
            url = f"{constants.CHROMEDRIVER_STORAGE_URL}/{version}/{self.__chromedriver_str}_{platform_32}{self.__zip_ext}"
            if self.__check_if_url_is_valid(url):
                return url

        raise VersionUrlError(f"Could not find download URL for version {version}.")

    def version_url(self, version: str) -> str:
        """
        Return the version download URL.

        :param version: Chromedriver version.
        """

        if not self.__check_if_version_format_is_valid(version):
            raise UnknownVersionError("Invalid version format.")

        # Get driver URLs from the new api
        response = requests.get(constants.KNOWN_GOOD_VERSIONS_WITH_DOWNLOADS_URL)
        if not response.ok:
            raise GetChromeDriverError(
                f"Could not get {constants.KNOWN_GOOD_VERSIONS_WITH_DOWNLOADS_URL}."
            )
        new_api_known_good_versions = response.json()["versions"]

        if self.__os_platform == OsPlatform.win:
            url = self.__version_url_for_platform(
                new_api_known_good_versions=new_api_known_good_versions,
                version=version,
                platform_32=Platform.win32.value,
                platform_64=Platform.win64.value,
            )

            return url

        elif self.__os_platform == OsPlatform.linux:
            url = self.__version_url_for_platform(
                new_api_known_good_versions=new_api_known_good_versions,
                version=version,
                platform_32=Platform.linux32.value,
                platform_64=Platform.linux64.value,
            )

            return url

        elif self.__os_platform == OsPlatform.mac:
            url = self.__version_url_for_platform(
                new_api_known_good_versions=new_api_known_good_versions,
                version=version,
                platform_64=Platform.mac64.value,
                is_mac=True,
            )

            return url

        raise VersionUrlError("Could not find version URL.")

    def download_stable_version(
        self, output_path: str = None, extract: bool = False
    ) -> str:
        """
        Download the latest stable chromedriver version.

        :param output_path: Path to download the driver to.
        :param extract: Extract the downloaded driver or not.
        """

        version = self.__latest_version_by_phase(Phase.stable)
        output_path = self.download_version(
            version=version, output_path=output_path, extract=extract
        )

        return output_path

    def download_beta_version(
        self, output_path: str = None, extract: bool = False
    ) -> str:
        """
        Download the latest beta chromedriver version.

        :param output_path: Path to download the driver to.
        :param extract: Extract the downloaded driver or not.
        """

        version = self.__latest_version_by_phase(Phase.beta)
        output_path = self.download_version(
            version=version, output_path=output_path, extract=extract
        )

        return output_path

    def download_version(
        self, version, output_path: str = None, extract: bool = False
    ) -> str:
        """
        Download a chromedriver version.

        :param version: Chromedriver version.
        :param output_path: Path to download the driver to.
        :param extract: Extract the downloaded driver or not.
        """

        if not self.__check_if_version_format_is_valid(version):
            raise UnknownVersionError("Invalid version format.")

        if not output_path:
            # On path is None, the driver will be downloaded at e.g. chromedriver/88.0.4324.96/bin/chromedriver.exe
            output_path = self._output_path(version)

        # e.g. if path == 'webdriver/bin', the driver will be downloaded at 'webdriver/bin/chromedriver.exe'
        def download(download_url: str):
            # Download
            try:
                file_path, file_name = downloader.download(
                    url=download_url, output_path=output_path
                )
            except (OSError, HTTPError, RequestException) as err:
                raise DownloadError(err)

            # Extract
            if extract:
                with zipfile.ZipFile(file_path, "r") as zip_ref:
                    zip_ref.extractall(path=output_path)

                # Remove downloaded zip file
                os.remove(file_path)

                # Move driver to output dir
                self.__move_driver_file_to_output_dir(
                    os_platform=self.__os_platform, output_path=output_path
                )

                if (
                    self.__os_platform == OsPlatform.linux
                    or self.__os_platform == OsPlatform.mac
                ):
                    os.chmod(f"{output_path}/chromedriver", 0o755)

        url = self.version_url(version)
        download(download_url=url)

        return output_path

    def __move_driver_file_to_output_dir(
        self, os_platform: OsPlatform, output_path: str
    ):
        """Move driver file to output dir if extracted driver file is contained inside a dir"""

        old_driver_file_path_32 = None
        old_driver_file_parent_dir_32 = None

        if os_platform == OsPlatform.win:
            driver_file_ext = ".exe"
            old_driver_file_path_64 = os.path.join(
                output_path,
                f"{self.__chromedriver_str}-win64",
                f"{self.__chromedriver_str}{driver_file_ext}",
            )
            old_driver_file_parent_dir_64 = os.path.join(
                output_path, f"{self.__chromedriver_str}-win64"
            )
            old_driver_file_path_32 = os.path.join(
                output_path,
                f"{self.__chromedriver_str}-win32",
                f"{self.__chromedriver_str}{driver_file_ext}",
            )
            old_driver_file_parent_dir_32 = os.path.join(
                output_path, f"{self.__chromedriver_str}-win32"
            )
        elif os_platform == OsPlatform.linux:
            driver_file_ext = ""
            old_driver_file_path_64 = os.path.join(
                output_path,
                f"{self.__chromedriver_str}-linux64",
                f"{self.__chromedriver_str}{driver_file_ext}",
            )
            old_driver_file_parent_dir_64 = os.path.join(
                output_path, f"{self.__chromedriver_str}-linux64"
            )
        elif os_platform == OsPlatform.mac:
            driver_file_ext = ""
            if pl.processor() == "arm":
                filename = f"{self.__chromedriver_str}-mac-arm64"
            else:
                filename = f"{self.__chromedriver_str}-mac-x64"
            old_driver_file_path_64 = os.path.join(
                output_path,
                filename,
                f"{self.__chromedriver_str}{driver_file_ext}",
            )
            old_driver_file_parent_dir_64 = os.path.join(output_path, filename)
        else:
            raise GetChromeDriverError("Could not determine OS.")

        # The correct driver file path inside output dir
        new_driver_file_path = os.path.join(
            f"{output_path}", f"{self.__chromedriver_str}{driver_file_ext}"
        )

        # If driver file was not found directly inside output dir
        if not os.path.isfile(
            os.path.join(output_path, f"{self.__chromedriver_str}{driver_file_ext}")
        ):
            # If driver file was found inside <output dir>/chromedriver-<platform-arch>
            if os.path.isfile(old_driver_file_path_64):
                # Move the driver to output dir
                shutil.move(old_driver_file_path_64, new_driver_file_path)

            # Arch 32, only check for Windows
            elif os_platform == OsPlatform.win:
                # If driver file was found inside <output dir>/chromedriver-<platform-arch>
                if os.path.isfile(old_driver_file_path_32):
                    # Move the driver to output dir
                    shutil.move(old_driver_file_path_32, new_driver_file_path)

        # Cleanup
        if old_driver_file_parent_dir_32:
            shutil.rmtree(old_driver_file_parent_dir_32, ignore_errors=True)
        if old_driver_file_path_64:
            shutil.rmtree(old_driver_file_parent_dir_64, ignore_errors=True)

    def __check_if_url_is_valid(self, url: str) -> bool:
        """
        Check if URL is valid.

        :param url: The driver download URL.
        """

        if requests.head(url).status_code != 200:
            return False

        return True

    def __check_if_version_format_is_valid(self, version: str) -> bool:
        """
        Check if version format is valid.

        :param version: Chromedriver version.
        """

        split_version = version.split(".")
        for number in split_version:
            if not number.isnumeric():
                return False

        return True

    def __check_if_os_platform_is_valid(self, os_platform: OsPlatform) -> bool:
        """
        Check if platform is valid.

        :param os_platform: OS.
        """

        if os_platform not in self.__os_platforms_list:
            return False

        return True

    def matching_version(self, chromium: bool = False) -> str:
        """
        Return a matching ChromeDriver version.
        """

        all_chromedriver_versions = self.__get_all_chromedriver_versions()
        installed_chrome_version = self.__get_installed_chrome_version(
            chromium=chromium
        )

        for chromedriver_version in reversed(all_chromedriver_versions):
            if ".".join(installed_chrome_version.split(".")[:-1]) == ".".join(
                chromedriver_version.split(".")[:-1]
            ):
                return chromedriver_version

        raise UnknownVersionError("Could not find matching version.")

    def auto_download(
        self, output_path: str = None, extract: bool = False, chromium: bool = False
    ) -> str:
        """
        Download ChromeDriver for the installed Chrome version on machine.

        :param output_path: Path to download the driver to.
        :param extract: Extract the downloaded driver or not.
        :param chromium: Look for the installed Chromium version instead of Chrome.
        """

        version = self.matching_version(chromium=chromium)
        if not version:
            name = "Chrome" if not chromium else "Chromium"
            raise VersionError(
                f"Unable to find a ChromeDriver version for the installed {name} version."
            )

        output_path = self.download_version(version, output_path, extract)

        return output_path

    def install(self, output_path: str = None) -> str:
        """Install ChromeDriver for the installed Chrome version on machine"""

        if output_path:
            self.auto_download(output_path=output_path, extract=True)
        else:
            output_path = self.auto_download(extract=True)

        os.environ["PATH"] += os.pathsep + output_path

        if not os.path.isabs(output_path):
            output_path = os.path.join(os.path.abspath(os.getcwd()), output_path)

        output_path = output_path.replace(os.sep, "/")

        return output_path

    @staticmethod
    def __get_all_chromedriver_versions() -> list:
        """Return a list with all ChromeDriver versions"""

        # Get versions from old storage
        key_texts = []
        old_storage_versions = []

        with urlopen(constants.CHROMEDRIVER_STORAGE_URL) as xml_file:
            tree = ElTree.parse(xml_file)
            root = tree.getroot()

            for root_item in root:
                # Remove namespace
                root_item.tag = root_item.tag.split("}", 1)[1]

            for content in root.findall("Contents"):
                for content_item in content:
                    # Remove namespace
                    content_item.tag = content_item.tag.split("}", 1)[1]

                    key_texts.append(content.find("Key").text)

        for text in key_texts:
            version = ""
            for char in text:
                if char.isnumeric() or char == ".":
                    version += char
                else:
                    break

            if len(version) < 1:
                continue

            old_storage_versions.append(version)

        old_storage_versions = list(dict.fromkeys(old_storage_versions))

        # Get versions from new storage
        new_storage_versions = []
        response = requests.get(constants.KNOWN_GOOD_VERSIONS_WITH_DOWNLOADS_URL)
        if response.ok:
            for version in response.json()["versions"]:
                new_storage_versions.append(version["version"])

        new_storage_versions = list(dict.fromkeys(new_storage_versions))

        unique_versions = list(
            dict.fromkeys(old_storage_versions + new_storage_versions)
        )
        sorted_versions = sorted(unique_versions, key=lambda x: int(x.split(".")[0]))

        return sorted_versions

    def __get_installed_chrome_version(self, chromium: bool = False) -> str:
        """
        Return the installed Chrome version on the machine.

        :param chromium: Return the installed Chromium version instead.
        """

        if self.__os_platform == OsPlatform.win:
            if chromium:
                args = [
                    "reg",
                    "query",
                    "HKEY_CURRENT_USER\\SOFTWARE\\Chromium\\BLBeacon",
                    "/v",
                    "version",
                ]
            else:
                args = [
                    "reg",
                    "query",
                    "HKEY_CURRENT_USER\\SOFTWARE\\Google\\Chrome\\BLBeacon",
                    "/v",
                    "version",
                ]
            process = subprocess.Popen(
                args,
                stdout=subprocess.PIPE,
                stderr=subprocess.DEVNULL,
                stdin=subprocess.DEVNULL,
            )
            version = process.communicate()[0].decode("UTF-8").split()[-1]

            return version

        elif self.__os_platform == OsPlatform.linux:
            if chromium:
                process = subprocess.Popen(
                    ["chromium-browser", "--version"],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.DEVNULL,
                    stdin=subprocess.DEVNULL,
                )

                return process.communicate()[0].decode("UTF-8").split()[1]
            else:
                process = subprocess.Popen(
                    args=["google-chrome", "--version"],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.DEVNULL,
                    stdin=subprocess.DEVNULL,
                )

                return process.communicate()[0].decode("UTF-8").split()[-1]

        elif self.__os_platform == OsPlatform.mac:
            if chromium:
                args = [
                    "/Applications/Chromium.app/Contents/MacOS/Chromium",
                    "--version",
                ]
            else:
                args = [
                    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
                    "--version",
                ]
            process = subprocess.Popen(
                args,
                stdout=subprocess.PIPE,
                stderr=subprocess.DEVNULL,
                stdin=subprocess.DEVNULL,
            )

            return process.communicate()[0].decode("UTF-8").split()[-1]

        raise UnknownVersionError("Could not find installed version.")

    def _output_path(self, version: str) -> str:
        """
        Get the output path.

        :param version: Chromedriver version.
        """

        return f"chromedriver/{version}/bin"
