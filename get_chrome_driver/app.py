import sys
import argparse
from signal import signal, SIGINT

import colorama

from . import __version__
from . import arguments
from .get_driver import GetChromeDriver
from .platforms import Platforms
from .phases import Phases
from .exceptions import GetChromeDriverError


def main():
    # noinspection PyUnusedLocal
    def signal_handler(signal_received, frame):
        """ Handles clean Ctrl+C exit """

        sys.stdout.write('\n')
        sys.exit(0)

    signal(SIGINT, signal_handler)
    App()


class App:

    def __init__(self):
        self.__c_fore = colorama.Fore
        self.__c_style = colorama.Style
        colorama.init()

        self.__platforms = Platforms()
        self.__phases = Phases()

        self.__msg_download_finished = 'download finished'
        self.__msg_required_add_version = (self.__c_fore.RED + 'required: add a version'
                                           + self.__c_style.RESET_ALL)
        self.__msg_optional_add_extract = 'optional: add --extract to extract the zip file'
        self.__msg_error_unrecognized_argument = (
                self.__c_fore.RED + 'error: unrecognized argument(s) detected' + self.__c_style.RESET_ALL
                + '\n' + 'tip: use --help to see all available arguments')
        self.__msg_download_error = (self.__c_fore.RED + 'error: an error occurred at downloading'
                                     + self.__c_style.RESET_ALL)
        self.__msg_version_url_error = (self.__c_fore.RED + 'error: could not find version url'
                                        + self.__c_style.RESET_ALL)
        self.__msg_no_stable_found_error = (self.__c_fore.RED + 'not found'
                                            + self.__c_style.RESET_ALL)
        self.__msg_no_beta_available_error = (self.__c_fore.RED + 'not beta version available'
                                              + self.__c_style.RESET_ALL)
        self.__msg_no_beta_version_error = (self.__c_fore.RED
                                            + 'error: could not find a beta version'
                                            + self.__c_style.RESET_ALL)
        self.__msg_no_stable_version_error = (self.__c_fore.RED
                                              + 'error: could not find a stable version'
                                              + self.__c_style.RESET_ALL)

        self.__parser = argparse.ArgumentParser(add_help=False)
        for i, arg in enumerate(arguments.args_options):
            self.__parser.add_argument(arguments.args_options[i][0], nargs='*')
        self.__args, self.__unknown = self.__parser.parse_known_args()

        self.__get_driver = GetChromeDriver()

        if self.__unknown:
            print(self.__msg_error_unrecognized_argument)
            sys.exit(0)

        ###################
        # DEFAULT NO ARGS #
        ###################
        if len(sys.argv) == 1:
            arguments.print_help()
            sys.exit(0)

        ########
        # HELP #
        ########
        self.__arg_help = self.__args.help
        if self.__arg_passed(self.__arg_help):
            arguments.print_help()
            sys.exit(0)

        ################
        # BETA VERSION #
        ################
        self.__arg_beta_version = self.__args.beta_version
        if self.__arg_passed(self.__arg_beta_version):
            self.__print_latest_version(self.__phases.beta)
            sys.exit(0)

        ##################
        # STABLE VERSION #
        ##################
        self.__arg_stable_version = self.__args.stable_version
        if self.__arg_passed(self.__arg_stable_version):
            self.__print_latest_version(self.__phases.stable)
            sys.exit(0)

        ###############
        # LATEST URLS #
        ###############
        self.__arg_latest_urls = self.__args.latest_urls
        if self.__arg_passed(self.__arg_latest_urls):
            self.__print_latest_urls()
            sys.exit(0)

        ###############
        # VERSION URL #
        ###############
        self.__arg_version_url = self.__args.version_url
        if self.__arg_passed(self.__arg_version_url):
            if len(self.__arg_version_url) < 1:
                print(self.__msg_required_add_version)
            else:
                self.__print_version_url(self.__arg_version_url[0])
            sys.exit(0)

        ############
        # BETA URL #
        ############
        self.__arg_beta_url = self.__args.beta_url
        if self.__arg_passed(self.__arg_beta_url):
            self.__print_latest_url(self.__phases.beta)
            sys.exit(0)

        ##############
        # STABLE URL #
        ##############
        self.__arg_stable_url = self.__args.stable_url
        if self.__arg_passed(self.__arg_stable_url):
            self.__print_latest_url(self.__phases.stable)
            sys.exit(0)

        #################
        # AUTO DOWNLOAD #
        #################
        self.__arg_auto_download = self.__args.auto_download
        if self.__arg_passed(self.__arg_auto_download):
            extract = False
            self.__arg_extract = self.__args.extract
            if self.__arg_passed(self.__arg_extract):
                extract = True
            self.__auto_download(extract)
            sys.exit(0)

        #################
        # DOWNLOAD BETA #
        #################
        self.__arg_download_beta = self.__args.download_beta
        if self.__arg_passed(self.__arg_download_beta):
            extract = False
            self.__arg_extract = self.__args.extract
            if self.__arg_passed(self.__arg_extract):
                extract = True
            self.__download_latest_version(self.__phases.beta, extract)
            sys.exit(0)

        ###################
        # DOWNLOAD STABLE #
        ###################
        self.__arg_download_stable = self.__args.download_stable
        if self.__arg_passed(self.__arg_download_stable):
            extract = False
            self.__arg_extract = self.__args.extract
            if self.__arg_passed(self.__arg_extract):
                extract = True
            self.__download_latest_version(self.__phases.stable, extract)
            sys.exit(0)

        ####################
        # DOWNLOAD VERSION #
        ####################
        self.__arg_download_version = self.__args.download_version
        if self.__arg_passed(self.__arg_download_version):
            extract = False
            self.__arg_extract = self.__args.extract
            if self.__arg_passed(self.__arg_extract):
                extract = True
            if len(self.__arg_download_version) < 1:
                print(self.__msg_required_add_version)
                print(self.__msg_optional_add_extract)
                sys.exit(0)
            else:
                version = self.__arg_download_version[0]
                self.__download_version(version, extract)
            sys.exit(0)

        ###########
        # VERSION #
        ###########
        self.__arg_version = self.__args.version
        if self.__arg_passed(self.__arg_version):
            print('v' + __version__)
            sys.exit(0)

    def __arg_passed(self, arg) -> bool:
        """ Check if the argument was passed """

        if isinstance(arg, list):
            return True
        return False

    def __print_latest_urls(self) -> None:
        """ Print the stable and beta url version for all platforms """

        get_driver_win = GetChromeDriver(self.__platforms.win)
        get_driver_linux = GetChromeDriver(self.__platforms.linux)
        get_driver_mac = GetChromeDriver(self.__platforms.mac)
        drivers = {'Windows': get_driver_win, 'Linux': get_driver_linux, 'macOS': get_driver_mac}

        for index, (key, value) in enumerate(drivers.items()):
            print('Latest beta and stable version for ' + key + ': ')
            try:
                print('stable : ' + value.stable_version_url())
            except GetChromeDriverError:
                print(self.__msg_no_stable_found_error)
            try:
                print('beta   : ' + value.beta_version_url())
            except GetChromeDriverError:
                print(self.__msg_no_beta_available_error)

            if index < len(drivers) - 1:
                print('')

    def __print_latest_version(self, phase) -> None:
        """ Print stable version or beta version """

        if phase == self.__phases.beta:
            try:
                print(self.__get_driver.beta_version())
            except GetChromeDriverError:
                print(self.__msg_no_beta_version_error)
        else:
            try:
                print(self.__get_driver.stable_version())
            except GetChromeDriverError:
                print(self.__msg_no_stable_version_error)

    def __print_latest_url(self, phase) -> None:
        """ Print stable url or beta url """

        if phase == self.__phases.beta:
            try:
                print(self.__get_driver.beta_version_url())
            except GetChromeDriverError:
                print(self.__msg_version_url_error)
        else:
            try:
                print(self.__get_driver.stable_version_url())
            except GetChromeDriverError:
                print(self.__msg_version_url_error)

    def __print_version_url(self, version) -> None:
        """ Print the url for a given version """

        try:
            print(self.__get_driver.version_url(version))
        except GetChromeDriverError:
            print(self.__msg_version_url_error)

    def __auto_download(self, extract) -> None:
        """ Auto download ChromeDriver """

        try:
            self.__get_driver.auto_download(extract=extract)
            print(self.__msg_download_finished)
        except GetChromeDriverError:
            print(self.__msg_download_error)

    def __download_latest_version(self, phase, extract) -> None:
        """ Download the version for the stable version or beta version """

        if phase == self.__phases.beta:
            try:
                self.__get_driver.download_beta_version(extract=extract)
                print(self.__msg_download_finished)
            except GetChromeDriverError:
                print(self.__msg_no_beta_version_error)
        else:
            try:
                self.__get_driver.download_stable_version(extract=extract)
                print(self.__msg_download_finished)
            except GetChromeDriverError:
                print(self.__msg_download_error)

    def __download_version(self, version, extract) -> None:
        """ Download the version of a given version """

        try:
            self.__get_driver.download_version(version, extract=extract)
            print(self.__msg_download_finished)
        except GetChromeDriverError:
            print(self.__msg_download_error)
