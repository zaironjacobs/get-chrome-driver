import sys
import argparse
from signal import signal, SIGINT

import colorama

from . import __version__
from . import arguments
from .get_driver import GetChromeDriver
from .platforms import Platforms
from .phase import Phase
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
        self.__phases = Phase()

        self.__msg_download_finished = 'download finished'
        self.__msg_required_add_release = (self.__c_fore.RED + 'required: add a release version'
                                           + self.__c_style.RESET_ALL)
        self.__msg_optional_add_extract = 'optional: add --extract to extract the zip file'
        self.__msg_error_unrecognized_argument = (
                self.__c_fore.RED + 'error: unrecognized argument(s) detected' + self.__c_style.RESET_ALL
                + '\n' + 'tip: use --help to see all available arguments')
        self.__msg_download_error = (self.__c_fore.RED + 'error: an error occurred at downloading'
                                     + self.__c_style.RESET_ALL)
        self.__msg_release_url_error = (self.__c_fore.RED + 'error: could not find release url'
                                        + self.__c_style.RESET_ALL)
        self.__msg_no_stable_found_error = (self.__c_fore.RED + 'not found'
                                            + self.__c_style.RESET_ALL)
        self.__msg_no_beta_available_error = (self.__c_fore.RED + 'not beta version available'
                                              + self.__c_style.RESET_ALL)
        self.__msg_no_beta_release_version_error = (self.__c_fore.RED
                                                    + 'error: could not find a beta release version'
                                                    + self.__c_style.RESET_ALL)
        self.__msg_no_stable_release_version_error = (self.__c_fore.RED
                                                      + 'error: could not find a stable release version'
                                                      + self.__c_style.RESET_ALL)

        self.__parser = argparse.ArgumentParser(add_help=False)
        for i, arg in enumerate(arguments.args_options):
            self.__parser.add_argument(arguments.args_options[i][0], nargs='*')
        self.__args, self.__unknown = self.__parser.parse_known_args()

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
            self.print_phase_version(self.__phases.beta)
            sys.exit(0)

        ##################
        # STABLE VERSION #
        ##################
        self.__arg_stable_version = self.__args.stable_version
        if self.__arg_passed(self.__arg_stable_version):
            self.print_phase_version(self.__phases.stable)
            sys.exit(0)

        ###############
        # LATEST URLS #
        ###############
        self.__arg_latest_urls = self.__args.latest_urls
        if self.__arg_passed(self.__arg_latest_urls):
            self.print_urls()
            sys.exit(0)

        ###############
        # RELEASE URL #
        ###############
        self.__arg_release_url = self.__args.release_url
        if self.__arg_passed(self.__arg_release_url):
            if len(self.__arg_release_url) < 1:
                print(self.__msg_required_add_release)
            else:
                self.print_release_url(self.__arg_release_url[0])
            sys.exit(0)

        ############
        # BETA URL #
        ############
        self.__arg_beta_url = self.__args.beta_url
        if self.__arg_passed(self.__arg_beta_url):
            self.print_phase_url(self.__phases.beta)
            sys.exit(0)

        ##############
        # STABLE URL #
        ##############
        self.__arg_stable_url = self.__args.stable_url
        if self.__arg_passed(self.__arg_stable_url):
            self.print_phase_url(self.__phases.stable)
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
            self.auto_download(extract)
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
            self.download_phase_release(self.__phases.beta, extract)

        ###################
        # DOWNLOAD STABLE #
        ###################
        self.__arg_download_stable = self.__args.download_stable
        if self.__arg_passed(self.__arg_download_stable):
            extract = False
            self.__arg_extract = self.__args.extract
            if self.__arg_passed(self.__arg_extract):
                extract = True
            self.download_phase_release(self.__phases.stable, extract)

        ####################
        # DOWNLOAD RELEASE #
        ####################
        self.__arg_download_release = self.__args.download_release
        if self.__arg_passed(self.__arg_download_release):
            extract = False
            self.__arg_extract = self.__args.extract
            if self.__arg_passed(self.__arg_extract):
                extract = True
            if len(self.__arg_download_release) < 1:
                print(self.__msg_required_add_release)
                print(self.__msg_optional_add_extract)
                sys.exit(0)
            else:
                release = self.__arg_download_release[0]
                self.download_release(release, extract)
            sys.exit(0)

        ###########
        # VERSION #
        ###########
        self.__arg_version = self.__args.version
        if self.__arg_passed(self.__arg_version):
            print('v' + __version__)
            sys.exit(0)

    def __arg_passed(self, arg):
        """ Check if arguments were passed """

        if isinstance(arg, list):
            return True
        return False

    def print_urls(self):
        """ Print the stable nd beta url release for all platforms """

        get_driver_win = GetChromeDriver(self.__platforms.win)
        get_driver_linux = GetChromeDriver(self.__platforms.linux)
        get_driver_mac = GetChromeDriver(self.__platforms.mac)
        drivers = {'Windows': get_driver_win, 'Linux': get_driver_linux, 'macOS': get_driver_mac}

        for index, (key, value) in enumerate(drivers.items()):
            print('Latest beta and stable release for ' + key + ': ')
            try:
                print('stable : ' + value.stable_release_url())
            except GetChromeDriverError:
                print(self.__msg_no_stable_found_error)
            try:
                print('beta   : ' + value.beta_release_url())
            except GetChromeDriverError:
                print(self.__msg_no_beta_available_error)

            if index < len(drivers) - 1:
                print('')

    def print_phase_version(self, phase):
        """ Print stable version or beta version """

        get_driver = GetChromeDriver()

        if phase == self.__phases.beta:
            try:
                print(get_driver.beta_release_version())
            except GetChromeDriverError:
                print(self.__msg_no_beta_release_version_error)
        else:
            try:
                print(get_driver.stable_release_version())
            except GetChromeDriverError:
                print(self.__msg_no_stable_release_version_error)

    def print_phase_url(self, phase):
        """ Print stable url or beta url """

        get_driver = GetChromeDriver()
        if phase == self.__phases.beta:
            try:
                print(get_driver.beta_release_url())
            except GetChromeDriverError:
                print(self.__msg_release_url_error)
        else:
            try:
                print(get_driver.stable_release_url())
            except GetChromeDriverError:
                print(self.__msg_release_url_error)

    def print_release_url(self, release):
        """ Print the url for a given version """

        get_driver = GetChromeDriver()

        try:
            print(get_driver.release_url(release))
        except GetChromeDriverError:
            print(self.__msg_release_url_error)

    def auto_download(self, extract):
        """ Auto download ChromeDriver """

        get_driver = GetChromeDriver()

        try:
            get_driver.auto_download(extract=extract)
            print(self.__msg_download_finished)
        except GetChromeDriverError:
            print(self.__msg_download_error)

    def download_phase_release(self, phase, extract):
        """ Download the release for the stable version or beta version """

        get_driver = GetChromeDriver()

        if phase == self.__phases.beta:
            try:
                get_driver.download_beta_release(extract=extract)
                print(self.__msg_download_finished)
            except GetChromeDriverError:
                print(self.__msg_download_error)
                print(self.__msg_no_beta_release_version_error)
        else:
            try:
                get_driver.download_stable_release(extract=extract)
                print(self.__msg_download_finished)
            except GetChromeDriverError:
                print(self.__msg_download_error)

    def download_release(self, release, extract):
        """ Download the release of a given version """

        get_driver = GetChromeDriver()

        try:
            get_driver.download_release(release, extract=extract)
            print(self.__msg_download_finished)
        except GetChromeDriverError:
            print(self.__msg_download_error)