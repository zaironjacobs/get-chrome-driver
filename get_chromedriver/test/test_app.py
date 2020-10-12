import pytest
import os
import shutil
import subprocess
import re
from os import path

from get_chromedriver import constants
from app_info import __app_name__
from app_info import __app_version__
from get_chromedriver.platforms import Platforms

beta_release = '86.0.4240.22'
stable_release = '85.0.4183.87'
random_release = '80.0.3987.106'
random_release_win_url = 'https://chromedriver.storage.googleapis.com/80.0.3987.106/chromedriver_win32.zip'
random_release_linux_url = 'https://chromedriver.storage.googleapis.com/80.0.3987.106/chromedriver_linux64.zip'
random_release_mac_url = 'https://chromedriver.storage.googleapis.com/80.0.3987.106/chromedriver_mac64.zip'
beta_release_win_url = 'https://chromedriver.storage.googleapis.com/86.0.4240.22/chromedriver_win32.zip'
beta_release_linux_url = 'https://chromedriver.storage.googleapis.com/86.0.4240.22/chromedriver_linux64.zip'
beta_release_mac_url = 'https://chromedriver.storage.googleapis.com/86.0.4240.22/chromedriver_mac64.zip'
stable_release_win_url = 'https://chromedriver.storage.googleapis.com/85.0.4183.87/chromedriver_win32.zip'
stable_release_linux_url = 'https://chromedriver.storage.googleapis.com/85.0.4183.87/chromedriver_linux64.zip'
stable_release_mac_url = 'https://chromedriver.storage.googleapis.com/85.0.4183.87/chromedriver_mac64.zip'

available_platforms = Platforms()

# Change to the current test directory
os.chdir(os.path.dirname(__file__))


class TestApp:

    ################
    # BETA VERSION #
    ################
    def test_latest_beta_release_version(self):
        out = subprocess.run(args=[__app_name__, '--beta-version'],
                             universal_newlines=True,
                             stdout=subprocess.PIPE)
        actual = out.stdout.split()[0]
        assert beta_release == str(actual)

    ##################
    # STABLE VERSION #
    ##################
    def test_latest_stable_release_version(self):
        out = subprocess.run(args=[__app_name__, '--stable-version'],
                             universal_newlines=True,
                             stdout=subprocess.PIPE)
        actual = out.stdout.split()[0]
        assert stable_release == str(actual)

    ############################
    # ALL LATEST RELEASE URLS #
    ############################
    def test_latest_release_urls(self):
        # Update on new beta and stable release
        with open('for_test_latest_release_urls', 'r') as file:
            latest_release_urls = file.read()
        latest_release_urls = latest_release_urls + '\n'

        out = subprocess.run(args=[__app_name__, '--latest-urls'],
                             universal_newlines=True,
                             stdout=subprocess.PIPE)
        actual = out.stdout
        ansi_escape = re.compile(r'\x1B\[[0-?]*[ -/]*[@-~]')
        actual = ansi_escape.sub('', actual)
        assert latest_release_urls == str(actual)

    ######################
    # RANDOM RELEASE URL #
    ######################
    def test_random_win_release_url(self):
        url = random_release_win_url
        out = subprocess.run(args=[__app_name__, '--release-url', 'win', random_release],
                             universal_newlines=True,
                             stdout=subprocess.PIPE)
        actual = out.stdout.split()[0]
        assert url, str(actual)

    def test_random_linux_release_url(self):
        url = random_release_linux_url
        out = subprocess.run(args=[__app_name__, '--release-url', 'linux', random_release],
                             universal_newlines=True,
                             stdout=subprocess.PIPE)
        actual = out.stdout.split()[0]
        assert url == str(actual)

    def test_random_mac_release_url(self):
        url = random_release_mac_url
        out = subprocess.run(args=[__app_name__, '--release-url', 'mac', random_release],
                             universal_newlines=True,
                             stdout=subprocess.PIPE)
        actual = out.stdout.split()[0]
        assert url == str(actual)

    ####################
    # BETA RELEASE URL #
    ####################
    def test_beta_win_release_url(self):
        url = beta_release_win_url
        out = subprocess.run(args=[__app_name__, '--beta-url', 'win'],
                             universal_newlines=True,
                             stdout=subprocess.PIPE)
        actual = out.stdout.split()[0]
        assert url == str(actual)

    def test_beta_linux_release_url(self):
        url = beta_release_linux_url
        out = subprocess.run(args=[__app_name__, '--beta-url', 'linux'],
                             universal_newlines=True,
                             stdout=subprocess.PIPE)
        actual = out.stdout.split()[0]
        assert url == str(actual)

    def test_beta_mac_release_url(self):
        url = beta_release_mac_url
        out = subprocess.run(args=[__app_name__, '--beta-url', 'mac'],
                             universal_newlines=True,
                             stdout=subprocess.PIPE)
        actual = out.stdout.split()[0]
        assert url == str(actual)

    ######################
    # STABLE RELEASE URL #
    ######################
    def test_stable_win_release_url(self):
        url = stable_release_win_url
        out = subprocess.run(args=[__app_name__, '--stable-url', 'win'],
                             universal_newlines=True,
                             stdout=subprocess.PIPE)
        actual = out.stdout.split()[0]
        assert url == str(actual)

    def test_stable_linux_release_url(self):
        url = stable_release_linux_url
        out = subprocess.run(args=[__app_name__, '--stable-url', 'linux'],
                             universal_newlines=True,
                             stdout=subprocess.PIPE)
        actual = out.stdout.split()[0]
        assert url == str(actual)

    def test_stable_mac_release_url(self):
        url = stable_release_mac_url
        out = subprocess.run(args=[__app_name__, '--stable-url', 'mac'],
                             universal_newlines=True,
                             stdout=subprocess.PIPE)
        actual = out.stdout.split()[0]
        assert url == str(actual)

    ######################################
    # DOWNLOAD BETA RELEASE - NO EXTRACT #
    ######################################
    def test_download_latest_win_beta_release_no_extract(self):
        release = beta_release
        subprocess.run(args=[__app_name__, '--download-beta', 'win'], stdout=subprocess.PIPE)
        file_path = (constants.DIR_DOWNLOADS + '/' + release + '/'
                     + available_platforms.win_arch + '/' + constants.FILE_NAME_CHROMEDRIVER_WIN_ZIP)
        result = path.exists(file_path)
        assert result

    def test_download_latest_linux_beta_release_no_extract(self):
        release = beta_release
        subprocess.run(args=[__app_name__, '--download-beta', 'linux'], stdout=subprocess.PIPE)
        file_path = (constants.DIR_DOWNLOADS + '/' + release + '/'
                     + available_platforms.linux_arch + '/' + constants.FILE_NAME_CHROMEDRIVER_LINUX_ZIP)
        result = path.exists(file_path)
        assert result

    def test_download_latest_mac_beta_release_no_extract(self):
        release = beta_release
        subprocess.run(args=[__app_name__, '--download-beta', 'mac'], stdout=subprocess.PIPE)
        file_path = (constants.DIR_DOWNLOADS + '/' + release + '/'
                     + available_platforms.mac_arch + '/' + constants.FILE_NAME_CHROMEDRIVER_MAC_ZIP)
        result = path.exists(file_path)
        assert result

    #####################################
    # DOWNLOAD BETA RELEASE - EXTRACTED #
    #####################################
    def test_download_latest_win_beta_release_extract(self):
        release = beta_release
        subprocess.run(args=[__app_name__, '--download-beta', 'win', '--extract'], stdout=subprocess.PIPE)
        file_path_extracted = (constants.DIR_DOWNLOADS + '/' + release + '/'
                               + available_platforms.win_arch + '/' + constants.FILE_NAME_CHROMEDRIVER_EXE)
        result = path.exists(file_path_extracted)
        assert result

    def test_download_latest_linux_beta_release_extract(self):
        release = beta_release
        subprocess.run(args=[__app_name__, '--download-beta', 'linux', '--extract'], stdout=subprocess.PIPE)
        file_path_extracted = (constants.DIR_DOWNLOADS + '/' + release + '/'
                               + available_platforms.linux_arch + '/' + constants.FILE_NAME_CHROMEDRIVER)
        result = path.exists(file_path_extracted)
        assert result

    def test_download_latest_mac_beta_release_extract(self):
        release = beta_release
        subprocess.run(args=[__app_name__, '--download-beta', 'mac', '--extract'], stdout=subprocess.PIPE)
        file_path_extracted = (constants.DIR_DOWNLOADS + '/' + release + '/'
                               + available_platforms.mac_arch + '/' + constants.FILE_NAME_CHROMEDRIVER)
        result = path.exists(file_path_extracted)
        assert result

    ########################################
    # DOWNLOAD STABLE RELEASE - NO EXTRACT #
    ########################################
    def test_download_latest_win_stable_release_no_extract(self):
        release = stable_release
        subprocess.run(args=[__app_name__, '--download-stable', 'win'], stdout=subprocess.PIPE)
        file_path = (constants.DIR_DOWNLOADS + '/' + release + '/'
                     + available_platforms.win_arch + '/' + constants.FILE_NAME_CHROMEDRIVER_WIN_ZIP)
        result = path.exists(file_path)
        assert result

    def test_download_latest_linux_stable_release_no_extract(self):
        release = stable_release
        subprocess.run(args=[__app_name__, '--download-stable', 'linux'], stdout=subprocess.PIPE)
        file_path = (constants.DIR_DOWNLOADS + '/' + release + '/'
                     + available_platforms.linux_arch + '/' + constants.FILE_NAME_CHROMEDRIVER_LINUX_ZIP)
        result = path.exists(file_path)
        assert result

    def test_download_latest_mac_stable_release_no_extract(self):
        release = stable_release
        subprocess.run(args=[__app_name__, '--download-stable', 'mac'], stdout=subprocess.PIPE)
        file_path = (constants.DIR_DOWNLOADS + '/' + release + '/'
                     + available_platforms.mac_arch + '/' + constants.FILE_NAME_CHROMEDRIVER_MAC_ZIP)
        result = path.exists(file_path)
        assert result

    #######################################
    # DOWNLOAD STABLE RELEASE - EXTRACTED #
    #######################################
    def test_download_latest_win_stable_release_extract(self):
        release = stable_release
        subprocess.run(args=[__app_name__, '--download-stable', 'win', '--extract'], stdout=subprocess.PIPE)
        file_path_extracted = (constants.DIR_DOWNLOADS + '/' + release + '/'
                               + available_platforms.win_arch + '/' + constants.FILE_NAME_CHROMEDRIVER_EXE)
        result = path.exists(file_path_extracted)
        assert result

    ########################################
    # DOWNLOAD RANDOM RELEASE - NO EXTRACT #
    ########################################
    def test_download_win_release_no_extract(self):
        release = random_release
        subprocess.run(args=[__app_name__, '--download-release', 'win', release], stdout=subprocess.PIPE)
        file_path = (constants.DIR_DOWNLOADS + '/' + release + '/'
                     + available_platforms.win_arch + '/' + constants.FILE_NAME_CHROMEDRIVER_WIN_ZIP)
        result = path.exists(file_path)
        assert result

    def test_download_linux_release_no_extract(self):
        release = random_release
        subprocess.run(args=[__app_name__, '--download-release', 'linux', release], stdout=subprocess.PIPE)
        file_path = (constants.DIR_DOWNLOADS + '/' + release + '/'
                     + available_platforms.linux_arch + '/' + constants.FILE_NAME_CHROMEDRIVER_LINUX_ZIP)
        result = path.exists(file_path)
        assert result

    def test_download_mac_release_no_extract(self):
        release = random_release
        subprocess.run(args=[__app_name__, '--download-release', 'mac', release], stdout=subprocess.PIPE)
        file_path = (constants.DIR_DOWNLOADS + '/' + release + '/'
                     + available_platforms.mac_arch + '/' + constants.FILE_NAME_CHROMEDRIVER_MAC_ZIP)
        result = path.exists(file_path)
        assert result

    #######################################
    # DOWNLOAD RANDOM RELEASE - EXTRACTED #
    #######################################
    def test_download_win_release_extract(self):
        release = random_release
        subprocess.run(args=[__app_name__, '--download-release', 'win', release, '--extract'],
                       stdout=subprocess.PIPE)
        file_path_extract = (constants.DIR_DOWNLOADS + '/' + release + '/'
                             + available_platforms.win_arch + '/' + constants.FILE_NAME_CHROMEDRIVER_EXE)
        result = path.exists(file_path_extract)
        assert result

    def test_download_linux_release_extract(self):
        release = random_release
        subprocess.run(args=[__app_name__, '--download-release', 'linux', release, '--extract'],
                       stdout=subprocess.PIPE)
        file_path_extract = (constants.DIR_DOWNLOADS + '/' + release + '/'
                             + available_platforms.linux_arch + '/' + constants.FILE_NAME_CHROMEDRIVER)
        result = path.exists(file_path_extract)
        assert result

    def test_download_mac_release_extract(self):
        release = random_release
        subprocess.run(args=[__app_name__, '--download-release', 'mac', release, '--extract'],
                       stdout=subprocess.PIPE)
        file_path_extract = (constants.DIR_DOWNLOADS + '/' + release + '/'
                             + available_platforms.mac_arch + '/' + constants.FILE_NAME_CHROMEDRIVER)
        result = path.exists(file_path_extract)
        assert result

    ###########
    # VERSION #
    ###########
    def test_version(self):
        out = subprocess.run(args=[__app_name__, '--version'],
                             universal_newlines=True,
                             stdout=subprocess.PIPE)
        actual = out.stdout.split()[0]
        assert 'v' + __app_version__ == str(actual)

    ###########
    # CLEANUP #
    ###########
    @pytest.fixture(scope='session', autouse=True)
    def cleanup(self):
        yield
        try:
            shutil.rmtree(constants.DIR_DOWNLOADS)
        except FileNotFoundError:
            pass
