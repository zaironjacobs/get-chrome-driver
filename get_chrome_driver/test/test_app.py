import pytest
import os
import shutil
import subprocess
import platform as pl
from os import path

from bs4 import BeautifulSoup
import requests
from decouple import config

from .. import GetChromeDriver
from .. import constants
from .. import __version__
from ..platforms import Platforms

name = 'get-chrome-driver'

platforms = Platforms()

stable_version = config('STABLE_VERSION')
random_version = config('RANDOM_VERSION')

if pl.system() == 'Windows':
    file_name_zipped = 'chromedriver_win32.zip'
    file_name = 'chromedriver.exe'
    stable_version_url = 'https://chromedriver.storage.googleapis.com/' + stable_version + '/' + file_name_zipped
    random_version_url = 'https://chromedriver.storage.googleapis.com/' + random_version + '/' + file_name_zipped
elif pl.system() == 'Linux':
    file_name_zipped = 'chromedriver_linux64.zip'
    file_name = 'chromedriver'
    stable_version_url = 'https://chromedriver.storage.googleapis.com/' + stable_version + '/' + file_name_zipped
    random_version_url = 'https://chromedriver.storage.googleapis.com/' + random_version + '/' + file_name_zipped
elif pl.system() == 'Darwin':
    file_name_zipped = 'chromedriver_mac64.zip'
    file_name = 'chromedriver'
    stable_version_url = 'https://chromedriver.storage.googleapis.com/' + stable_version + '/' + file_name_zipped
    random_version_url = 'https://chromedriver.storage.googleapis.com/' + random_version + '/' + file_name_zipped

# Change to the current test directory
os.chdir(os.path.dirname(__file__))


class TestApp:

    ###################################
    # LI TEXT "LATEST STABLE VERSION" #
    ###################################
    def test_text_match_latest_stable(self):
        match_found = False

        result = requests.get(constants.CHROMEDRIVER_CHROMIUM_URL)
        soup = BeautifulSoup(result.content, 'html.parser')
        ul = soup.select_one(constants.CSS_VERSIONS_SELECTOR_UL)
        for li in ul:
            text = li.text.replace(u'\u00A0', ' ')
            if text[:len(constants.LATEST_STABLE_VERSION_STR)].lower() == constants.LATEST_STABLE_VERSION_STR.lower():
                match_found = True
                break

        assert match_found is True

    #################################
    # LI TEXT "LATEST BETA VERSION" #
    #################################
    def test_text_match_latest_beta(self):
        match_found = False

        result = requests.get(constants.CHROMEDRIVER_CHROMIUM_URL)
        soup = BeautifulSoup(result.content, 'html.parser')
        ul = soup.select_one(constants.CSS_VERSIONS_SELECTOR_UL)
        for li in ul:
            text = li.text.replace(u'\u00A0', ' ')
            if text[:len(constants.LATEST_BETA_VERSION_STR)].lower() == constants.LATEST_BETA_VERSION_STR.lower():
                match_found = True
                break

        assert match_found is True

    ##################
    # STABLE VERSION #
    ##################
    def test_stable_version(self):
        out = subprocess.run(args=[name, '--stable-version'],
                             universal_newlines=True,
                             stdout=subprocess.PIPE)
        actual = out.stdout.split()[0]
        assert stable_version == str(actual)

    ######################
    # RANDOM VERSION URL #
    ######################
    def test_random_version_url(self):
        url = random_version_url
        out = subprocess.run(args=[name, '--version-url', random_version],
                             universal_newlines=True,
                             stdout=subprocess.PIPE)
        actual = out.stdout.split()[0]
        assert url, str(actual)

    ######################
    # STABLE VERSION URL #
    ######################
    def test_stable_version_url(self):
        url = stable_version_url
        out = subprocess.run(args=[name, '--stable-url'],
                             universal_newlines=True,
                             stdout=subprocess.PIPE)
        actual = out.stdout.split()[0]
        assert url == str(actual)

    ##############################
    # AUTO DOWNLOAD - NO EXTRACT #
    ##############################
    def test_auto_download_no_extract(self):
        get_driver = GetChromeDriver()
        version = get_driver.matching_version()
        subprocess.run(args=[name, '--auto-download'], stdout=subprocess.PIPE)
        file_path = get_driver._default_output_path(version) + '/' + file_name_zipped
        result = path.exists(file_path)
        assert result

    ###########################
    # AUTO DOWNLOAD - EXTRACT #
    ###########################
    def test_auto_download_extract(self):
        get_driver = GetChromeDriver()
        version = get_driver.matching_version()
        subprocess.run(args=[name, '--auto-download', '--extract'], stdout=subprocess.PIPE)
        file_path_extracted = get_driver._default_output_path(version) + '/' + file_name
        result = path.exists(file_path_extracted)
        assert result

    ################################################
    # AUTO DOWNLOAD - EXTRACT AND WITH CUSTOM PATH #
    ################################################
    def test_auto_download_extract_custom_path(self):
        get_driver = GetChromeDriver()
        get_driver.auto_download(output_path='webdriver/bin/chromedriver', extract=True)
        result = path.exists('webdriver/bin/chromedriver/' + file_name)
        assert result

    ########################################
    # DOWNLOAD STABLE VERSION - NO EXTRACT #
    ########################################
    def test_download_stable_version_no_extract(self):
        get_driver = GetChromeDriver()
        version = stable_version
        subprocess.run(args=[name, '--download-stable'], stdout=subprocess.PIPE)
        file_path = get_driver._default_output_path(version) + '/' + file_name_zipped
        result = path.exists(file_path)
        assert result

    #####################################
    # DOWNLOAD STABLE VERSION - EXTRACT #
    #####################################
    def test_download_stable_version_extract(self):
        get_driver = GetChromeDriver()
        version = stable_version
        subprocess.run(args=[name, '--download-stable', '--extract'], stdout=subprocess.PIPE)
        file_path_extracted = get_driver._default_output_path(version) + '/' + file_name
        result = path.exists(file_path_extracted)
        assert result

    ##########################################################
    # STABLE VERSION DOWNLOAD - EXTRACT AND WITH CUSTOM PATH #
    ##########################################################
    def test_download_stable_version_extract_custom_path(self):
        get_driver = GetChromeDriver()
        get_driver.download_stable_version(output_path='webdriver/bin/chromedriver', extract=True)
        result = path.exists('webdriver/bin/chromedriver/' + file_name)
        assert result

    ########################################
    # DOWNLOAD RANDOM VERSION - NO EXTRACT #
    ########################################
    def test_download_random_version_no_extract(self):
        get_driver = GetChromeDriver()
        version = random_version
        subprocess.run(args=[name, '--download-version', version], stdout=subprocess.PIPE)
        file_path = get_driver._default_output_path(version) + '/' + file_name_zipped
        result = path.exists(file_path)
        assert result

    #####################################
    # DOWNLOAD RANDOM VERSION - EXTRACT #
    #####################################
    def test_download_random_version_extract(self):
        get_driver = GetChromeDriver()
        version = random_version
        subprocess.run(args=[name, '--download-version', version, '--extract'],
                       stdout=subprocess.PIPE)
        file_path_extracted = get_driver._default_output_path(version) + '/' + file_name
        result = path.exists(file_path_extracted)
        assert result

    ##########################################################
    # RANDOM VERSION DOWNLOAD - EXTRACT AND WITH CUSTOM PATH #
    ##########################################################
    def test_download_random_version_extract_custom_path(self):
        get_driver = GetChromeDriver()
        version = random_version
        get_driver.download_version(version, output_path='webdriver/bin/chromedriver', extract=True)
        result = path.exists('webdriver/bin/chromedriver/' + file_name)
        assert result

    ###########
    # VERSION #
    ###########
    def test_version(self):
        out = subprocess.run(args=[name, '--version'],
                             universal_newlines=True,
                             stdout=subprocess.PIPE)
        actual = out.stdout.split()[0]
        assert 'v' + __version__ == str(actual)

    ###########
    # CLEANUP #
    ###########
    @pytest.fixture(scope='function', autouse=True)
    def cleanup(self):
        yield
        try:
            shutil.rmtree(constants.CHROMEDRIVER)
        except (FileNotFoundError, PermissionError):
            pass
        try:
            shutil.rmtree(constants.WEBDRIVER)
        except (FileNotFoundError, PermissionError):
            pass
