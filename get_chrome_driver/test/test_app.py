import os
import platform as pl
import shutil
import struct
import subprocess
from os import path

import requests
import pytest
from dotenv import load_dotenv

from get_chrome_driver import GetChromeDriver
from get_chrome_driver import __version__
from get_chrome_driver.enums import Platform

load_dotenv()

name = "get-chrome-driver"

STABLE_VERSION: str | None = os.getenv("STABLE_VERSION")
RANDOM_VERSION: str | None = os.getenv("RANDOM_VERSION")

# If STABLE_VERSION is not defined in .env, then find it using the JSON API endpoint
if not STABLE_VERSION:
    res_last_known_good_versions = requests.get(
        "https://googlechromelabs.github.io/chrome-for-testing/last-known-good-versions.json"
    )
    STABLE_VERSION: str = res_last_known_good_versions.json()["channels"]["Stable"][
        "version"
    ]
if not RANDOM_VERSION:
    RANDOM_VERSION = "116.0.5797.0"

arch = struct.calcsize("P") * 8


def is_version_in_new_api(version: str) -> bool:
    """Is version in new API"""

    if (
        int(version.split(".")[0]) < 113
        or version == "113.0.5672.24"
        or version == "113.0.5672.63"
        or version == "114.0.5735.16"
        or version == "114.0.5735.90"
    ):
        return False
    else:
        return True


def get_filenames_zip(version: str) -> tuple:
    """Get filenames zip"""

    if is_version_in_new_api(version):
        if pl.system() == "Windows":
            filename_zipped_32 = "chromedriver-win32.zip"
            filename_zipped_64 = "chromedriver-win64.zip"
        elif pl.system() == "Linux":
            filename_zipped_32 = "chromedriver-linux32.zip"
            filename_zipped_64 = "chromedriver-linux64.zip"
        elif pl.system() == "Darwin":
            filename_zipped_32 = "chromedriver-mac32.zip"
            filename_zipped_64 = "chromedriver-mac64.zip"
        else:
            raise Exception("Could not identify platform.")
    else:
        if pl.system() == "Windows":
            filename_zipped_32 = "chromedriver_win32.zip"
            filename_zipped_64 = "chromedriver_win64.zip"
        elif pl.system() == "Linux":
            filename_zipped_32 = "chromedriver_linux32.zip"
            filename_zipped_64 = "chromedriver_linux64.zip"
        elif pl.system() == "Darwin":
            filename_zipped_32 = "chromedriver_mac32.zip"
            filename_zipped_64 = "chromedriver_mac64.zip"
        else:
            raise Exception("Could not identify platform.")

    return filename_zipped_32, filename_zipped_64


# Filename
if pl.system() == "Windows":
    filename = "chromedriver.exe"
else:
    filename = "chromedriver"

# Platform name
if pl.system() == "Windows":
    platform_name_32 = Platform.win32.value
    platform_name_64 = Platform.win64.value
elif pl.system() == "Linux":
    platform_name_32 = Platform.linux32.value
    platform_name_64 = Platform.linux64.value
elif pl.system() == "Darwin":
    platform_name_32 = Platform.mac32.value
    platform_name_64 = Platform.mac_x64.value
else:
    raise Exception("Could not identify platform.")

# Filenames zipped
stable_filename_zipped_32, stable_filename_zipped_64 = get_filenames_zip(STABLE_VERSION)
random_filename_zipped_32, random_filename_zipped_64 = get_filenames_zip(RANDOM_VERSION)

# Generate stable version url
if is_version_in_new_api(STABLE_VERSION):
    # New storage
    stable_version_url_32 = f"https://storage.googleapis.com/chrome-for-testing-public/{STABLE_VERSION}/{platform_name_32}/{stable_filename_zipped_32}"
    stable_version_url_64 = f"https://storage.googleapis.com/chrome-for-testing-public/{STABLE_VERSION}/{platform_name_64}/{stable_filename_zipped_64}"
else:
    # Old storage
    stable_version_url_32 = f"https://chromedriver.storage.googleapis.com/{STABLE_VERSION}/{stable_filename_zipped_32}"
    stable_version_url_64 = f"https://chromedriver.storage.googleapis.com/{STABLE_VERSION}/{stable_filename_zipped_64}"

# Generate random version url
if is_version_in_new_api(RANDOM_VERSION):
    # New storage
    random_version_url_32 = f"https://storage.googleapis.com/chrome-for-testing-public/{RANDOM_VERSION}/{platform_name_32}/{random_filename_zipped_32}"
    random_version_url_64 = f"https://storage.googleapis.com/chrome-for-testing-public/{RANDOM_VERSION}/{platform_name_64}/{random_filename_zipped_64}"
else:
    # Old storage
    random_version_url_32 = f"https://chromedriver.storage.googleapis.com/{RANDOM_VERSION}/{random_filename_zipped_32}"
    random_version_url_64 = f"https://chromedriver.storage.googleapis.com/{RANDOM_VERSION}/{random_filename_zipped_64}"

# Change to the current test directory
os.chdir(os.path.dirname(__file__))


class TestApp:
    def test_stable_version(self):
        out = subprocess.run(
            args=[name, "--stable-version"],
            universal_newlines=True,
            stdout=subprocess.PIPE,
        )
        actual = out.stdout.split()[0]

        assert STABLE_VERSION == actual

    def test_random_version_url(self):
        out = subprocess.run(
            args=[name, "--version-url", RANDOM_VERSION],
            universal_newlines=True,
            stdout=subprocess.PIPE,
        )
        actual = out.stdout.split()[0]
        match = actual == random_version_url_32 or actual == random_version_url_64

        assert match

    def test_stable_version_url(self):
        out = subprocess.run(
            args=[name, "--stable-url"], universal_newlines=True, stdout=subprocess.PIPE
        )
        actual = out.stdout.split()[0]
        match = actual == stable_version_url_32 or actual == stable_version_url_64

        assert match

    def test_auto_download_no_extract(self):
        get_driver = GetChromeDriver()
        version = get_driver.matching_version()
        subprocess.run(args=[name, "--auto-download"], stdout=subprocess.PIPE)
        filename_zipped_32, filename_zipped_64 = get_filenames_zip(version)
        file_path_32 = f"{get_driver._output_path(version)}/{filename_zipped_32}"
        file_path_64 = f"{get_driver._output_path(version)}/{filename_zipped_64}"
        match = path.exists(file_path_32) or path.exists(file_path_64)

        assert match

    def test_auto_download_extract(self):
        get_driver = GetChromeDriver()
        version = get_driver.matching_version()
        subprocess.run(
            args=[name, "--auto-download", "--extract"], stdout=subprocess.PIPE
        )
        file_path_extracted = f"{get_driver._output_path(version)}/{filename}"
        result = path.exists(file_path_extracted)

        assert result

    def test_auto_download_extract_custom_path(self):
        get_driver = GetChromeDriver()
        get_driver.auto_download(output_path="webdriver/bin/chromedriver", extract=True)
        result = path.exists(f"webdriver/bin/chromedriver/{filename}")

        assert result

    def test_download_stable_version_no_extract(self):
        get_driver = GetChromeDriver()
        version = STABLE_VERSION
        subprocess.run(args=[name, "--download-stable"], stdout=subprocess.PIPE)
        file_path_32 = f"{get_driver._output_path(version)}/{stable_filename_zipped_32}"
        file_path_64 = f"{get_driver._output_path(version)}/{stable_filename_zipped_64}"
        match = path.exists(file_path_32) or path.exists(file_path_64)

        assert match

    def test_download_stable_version_extract(self):
        get_driver = GetChromeDriver()
        version = STABLE_VERSION
        subprocess.run(
            args=[name, "--download-stable", "--extract"], stdout=subprocess.PIPE
        )
        file_path_extracted = f"{get_driver._output_path(version)}/{filename}"
        result = path.exists(file_path_extracted)

        assert result

    def test_download_stable_version_extract_custom_path(self):
        get_driver = GetChromeDriver()
        get_driver.download_stable_version(
            output_path="webdriver/bin/chromedriver", extract=True
        )
        result = path.exists(f"webdriver/bin/chromedriver/{filename}")

        assert result

    def test_download_random_version_no_extract(self):
        get_driver = GetChromeDriver()
        version = RANDOM_VERSION
        subprocess.run(
            args=[name, "--download-version", version], stdout=subprocess.PIPE
        )
        file_path_32 = f"{get_driver._output_path(version)}/{random_filename_zipped_32}"
        file_path_64 = f"{get_driver._output_path(version)}/{random_filename_zipped_64}"
        result = path.exists(file_path_32) or path.exists(file_path_64)

        assert result

    def test_download_random_version_extract(self):
        get_driver = GetChromeDriver()
        version = RANDOM_VERSION
        subprocess.run(
            args=[name, "--download-version", version, "--extract"],
            stdout=subprocess.PIPE,
        )
        file_path_extracted = f"{get_driver._output_path(version)}/{filename}"
        result = path.exists(file_path_extracted)

        assert result

    def test_download_random_version_extract_custom_path(self):
        get_driver = GetChromeDriver()
        version = RANDOM_VERSION
        get_driver.download_version(
            version, output_path="webdriver/bin/chromedriver", extract=True
        )
        result = path.exists(f"webdriver/bin/chromedriver/{filename}")

        assert result

    def test_install(self):
        get_driver = GetChromeDriver()
        output_path = get_driver.install()

        found = False
        if os.path.isfile(f"{output_path}/{filename}"):
            found = True

        assert found

    def test_install_custom_path(self):
        get_driver = GetChromeDriver()
        output_path = get_driver.install("my_dir_1/my_dir_2")

        found = False
        if os.path.isfile(f"{output_path}/{filename}"):
            found = True

        assert found

    def test_version(self):
        out = subprocess.run(
            args=[name, "--version"], universal_newlines=True, stdout=subprocess.PIPE
        )
        actual = out.stdout.split()[0]

        assert f"v{__version__}" == str(actual)

    @pytest.fixture(scope="function", autouse=True)
    def cleanup(self):
        yield
        try:
            shutil.rmtree("webdriver")
        except (FileNotFoundError, PermissionError):
            pass
        try:
            shutil.rmtree("chromedriver")
        except (FileNotFoundError, PermissionError):
            pass
        try:
            shutil.rmtree("my_dir_1")
        except (FileNotFoundError, PermissionError):
            pass
