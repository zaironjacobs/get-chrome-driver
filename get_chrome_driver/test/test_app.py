import pytest
import os
import shutil
import subprocess
import platform as pl
from os import path

from bs4 import BeautifulSoup
import requests
from decouple import config

from .. import constants
from .. import __version__
from ..platforms import Platforms

name = 'get-chrome-driver'

platforms = Platforms()

stable_release = config('STABLE_RELEASE')
random_release = config('RANDOM_RELEASE')

file_name_zipped = ''
stable_release_url = ''
random_release_url = ''
if pl.system() == 'Windows':
    file_name_zipped = 'chromedriver_win32.zip'
    file_name = 'chromedriver.exe'
    stable_release_url = 'https://chromedriver.storage.googleapis.com/' + stable_release + '/chromedriver_win32.zip'
    random_release_url = 'https://chromedriver.storage.googleapis.com/' + random_release + '/chromedriver_win32.zip'
elif pl.system() == 'Linux':
    file_name_zipped = 'chromedriver_linux64.zip'
    file_name = 'chromedriver'
    stable_release_url = 'https://chromedriver.storage.googleapis.com/' + stable_release + '/chromedriver_linux64.zip'
    random_release_url = 'https://chromedriver.storage.googleapis.com/' + random_release + '/chromedriver_linux64.zip'
elif pl.system() == 'Darwin':
    file_name_zipped = 'chromedriver_mac64.zip'
    file_name = 'chromedriver'
    stable_release_url = 'https://chromedriver.storage.googleapis.com/' + stable_release + '/chromedriver_mac64.zip'
    random_release_url = 'https://chromedriver.storage.googleapis.com/' + random_release + '/chromedriver_mac64.zip'

# Change to the current test directory
os.chdir(os.path.dirname(__file__))


class TestApp:

    ###################################
    # LI TEXT "LATEST STABLE RELEASE" #
    ###################################
    def test_text_match_latest_stable(self):
        match_found = False

        result = requests.get(constants.CHROMEDRIVER_CHROMIUM_URL)
        soup = BeautifulSoup(result.content, 'html.parser')
        ul = soup.select_one(constants.UL_RELEASES_SELECTOR)
        for li in ul:
            text = li.text.replace(u'\u00A0', ' ')
            if text[:len(constants.LATEST_STABLE_RELEASE_STR)].lower() == constants.LATEST_STABLE_RELEASE_STR.lower():
                match_found = True
                break

        assert match_found is True

    #################################
    # LI TEXT "LATEST BETA RELEASE" #
    #################################
    def test_text_match_latest_beta(self):
        match_found = False

        result = requests.get(constants.CHROMEDRIVER_CHROMIUM_URL)
        soup = BeautifulSoup(result.content, 'html.parser')
        ul = soup.select_one(constants.UL_RELEASES_SELECTOR)
        for li in ul:
            text = li.text.replace(u'\u00A0', ' ')
            if text[:len(constants.LATEST_BETA_RELEASE_STR)].lower() == constants.LATEST_BETA_RELEASE_STR.lower():
                match_found = True
                break

        assert match_found is True

    ##################
    # STABLE VERSION #
    ##################
    def test_stable_release_version(self):
        out = subprocess.run(args=[name, '--stable-version'],
                             universal_newlines=True,
                             stdout=subprocess.PIPE)
        actual = out.stdout.split()[0]
        assert stable_release == str(actual)

    ######################
    # RANDOM RELEASE URL #
    ######################
    def test_random_win_release_url(self):
        url = random_release_url
        out = subprocess.run(args=[name, '--release-url', random_release],
                             universal_newlines=True,
                             stdout=subprocess.PIPE)
        actual = out.stdout.split()[0]
        assert url, str(actual)

    ######################
    # STABLE RELEASE URL #
    ######################
    def test_stable_release_url(self):
        url = stable_release_url
        out = subprocess.run(args=[name, '--stable-url'],
                             universal_newlines=True,
                             stdout=subprocess.PIPE)
        actual = out.stdout.split()[0]
        assert url == str(actual)

    ########################################
    # DOWNLOAD STABLE RELEASE - NO EXTRACT #
    ########################################
    def test_download_stable_release_no_extract(self):
        release = stable_release
        subprocess.run(args=[name, '--download-stable'], stdout=subprocess.PIPE)
        file_path = (constants.DIR_DOWNLOAD + '/' + release + '/'
                     + 'bin' + '/' + file_name_zipped)
        result = path.exists(file_path)
        assert result

    #######################################
    # DOWNLOAD STABLE RELEASE - EXTRACTED #
    #######################################
    def test_download_stable_win_release_extract(self):
        release = stable_release
        subprocess.run(args=[name, '--download-stable', '--extract'], stdout=subprocess.PIPE)
        file_path_extracted = (constants.DIR_DOWNLOAD + '/' + release + '/'
                               + 'bin' + '/' + file_name)
        result = path.exists(file_path_extracted)
        assert result

    ########################################
    # DOWNLOAD RANDOM RELEASE - NO EXTRACT #
    ########################################
    def test_download_random_win_release_no_extract(self):
        release = random_release
        subprocess.run(args=[name, '--download-release', release], stdout=subprocess.PIPE)
        file_path = (constants.DIR_DOWNLOAD + '/' + release + '/'
                     + 'bin' + '/' + file_name_zipped)
        result = path.exists(file_path)
        assert result

    #######################################
    # DOWNLOAD RANDOM RELEASE - EXTRACTED #
    #######################################
    def test_download_random_win_release_extract(self):
        release = random_release
        subprocess.run(args=[name, '--download-release', release, '--extract'],
                       stdout=subprocess.PIPE)
        file_path_extracted = (constants.DIR_DOWNLOAD + '/' + release + '/'
                               + 'bin' + '/' + file_name)
        result = path.exists(file_path_extracted)
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
    @pytest.fixture(scope='session', autouse=True)
    def cleanup(self):
        yield
        try:
            shutil.rmtree('chromedriver')
        except FileNotFoundError:
            pass
