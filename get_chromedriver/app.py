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
        self.__msg_required_choose_platform = (self.__c_fore.RED + 'required: choose one of the following platforms: '
                                               + str(self.__platforms.list) + self.__c_style.RESET_ALL)
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
            self.print_latest_urls()
            sys.exit(0)

        ###############
        # RELEASE URL #
        ###############
        self.__arg_release_url = self.__args.release_url
        if self.__arg_passed(self.__arg_release_url):
            custom_required_message = (self.__msg_required_choose_platform
                                       + '\n' + self.__msg_required_add_release)
            if not self.__arg_release_url:
                print(custom_required_message)
                sys.exit(0)
            if len(self.__arg_release_url) != 2:
                print(custom_required_message)
                sys.exit(0)

            platform = self.__arg_release_url[0]
            release = self.__arg_release_url[1]
            if self.__platforms.win == platform:
                # noinspection PyBroadException
                try:
                    self.print_release_url(self.__platforms.win, release)
                except Exception:
                    print(self.__msg_release_url_error)
            elif self.__platforms.linux == platform:
                # noinspection PyBroadException
                try:
                    self.print_release_url(self.__platforms.linux, release)
                except Exception:
                    print(self.__msg_release_url_error)
            elif self.__platforms.mac == platform:
                # noinspection PyBroadException
                try:
                    self.print_release_url(self.__platforms.mac, release)
                except Exception:
                    print(self.__msg_release_url_error)
            else:
                print(custom_required_message)
            sys.exit(0)

        ############
        # BETA URL #
        ############
        self.__arg_beta_url = self.__args.beta_url
        if self.__arg_passed(self.__arg_beta_url):
            if not self.__arg_beta_url:
                print(self.__msg_required_choose_platform)
                sys.exit(0)
            if len(self.__arg_beta_url) != 1:
                print(self.__msg_required_choose_platform)
                sys.exit(0)

            platform = self.__arg_beta_url[0]
            if self.__platforms.win == platform:
                # noinspection PyBroadException
                try:
                    self.print_phase_url(self.__platforms.win, self.__phases.beta)
                except Exception:
                    print(self.__msg_release_url_error)
            elif self.__platforms.linux == platform:
                # noinspection PyBroadException
                try:
                    self.print_phase_url(self.__platforms.linux, self.__phases.beta)
                except Exception:
                    print(self.__msg_release_url_error)
            elif self.__platforms.mac == platform:
                # noinspection PyBroadException
                try:
                    self.print_phase_url(self.__platforms.mac, self.__phases.beta)
                except Exception:
                    print(self.__msg_release_url_error)
            else:
                print(self.__msg_required_choose_platform)
            sys.exit(0)

        ##############
        # STABLE URL #
        ##############
        self.__arg_stable_url = self.__args.stable_url
        if self.__arg_passed(self.__arg_stable_url):
            if not self.__arg_stable_url:
                print(self.__msg_required_choose_platform)
                sys.exit(0)
            if len(self.__arg_stable_url) != 1:
                print(self.__msg_required_choose_platform)
                sys.exit(0)

            self.__platform = self.__arg_stable_url[0]
            if self.__platforms.win == self.__platform:
                # noinspection PyBroadException
                try:
                    self.print_phase_url(self.__platforms.win, self.__phases.stable)
                except Exception:
                    print(self.__msg_release_url_error)
            elif self.__platforms.linux == self.__platform:
                # noinspection PyBroadException
                try:
                    self.print_phase_url(self.__platforms.linux, self.__phases.stable)
                except Exception:
                    print(self.__msg_release_url_error)
            elif self.__platforms.mac == self.__platform:
                # noinspection PyBroadException
                try:
                    self.print_phase_url(self.__platforms.mac, self.__phases.stable)
                except Exception:
                    print(self.__msg_release_url_error)
            else:
                print(self.__msg_required_choose_platform)
            sys.exit(0)

        #################
        # DOWNLOAD BETA #
        #################
        self.__arg_download_beta = self.__args.download_beta
        if self.__arg_passed(self.__arg_download_beta):
            if not self.__arg_download_beta:
                print(self.__msg_required_choose_platform)
                print(self.__msg_optional_add_extract)
                sys.exit(0)
            extract = False
            self.__arg_extract = self.__args.extract
            if self.__arg_passed(self.__arg_extract):
                extract = True
            platform = self.__arg_download_beta[0]
            if platform in self.__platforms.list:
                # noinspection PyBroadException
                try:
                    if not self.download_latest_phase_release(platform, self.__phases.beta, extract):
                        print(self.__msg_download_error)
                        print(self.__c_fore.RED
                              + 'there might be no beta release at the moment'
                              + self.__c_style.RESET_ALL)
                    else:
                        print(self.__msg_download_finished)
                except GetChromeDriverError:
                    print(self.__msg_download_error)
            else:
                print(self.__msg_required_choose_platform)
                print(self.__msg_optional_add_extract)
            sys.exit(0)

        ###################
        # DOWNLOAD STABLE #
        ###################
        self.__arg_download_stable = self.__args.download_stable
        if self.__arg_passed(self.__arg_download_stable):
            if not self.__arg_download_stable:
                print(self.__msg_required_choose_platform)
                print(self.__msg_optional_add_extract)
                sys.exit(0)
            extract = False
            self.__arg_extract = self.__args.extract
            if self.__arg_passed(self.__arg_extract):
                extract = True
            platform = self.__arg_download_stable[0]
            if platform in self.__platforms.list:
                # noinspection PyBroadException
                try:
                    if not self.download_latest_phase_release(platform, self.__phases.stable, extract):
                        print(self.__msg_download_error)
                    else:
                        print(self.__msg_download_finished)
                except GetChromeDriverError:
                    print(self.__msg_download_error)
            else:
                print(self.__msg_required_choose_platform)
                print(self.__msg_optional_add_extract)
            sys.exit(0)

        ####################
        # DOWNLOAD RELEASE #
        ####################
        self.__arg_download_release = self.__args.download_release
        if self.__arg_passed(self.__arg_download_release):
            custom_required_message = (self.__msg_required_choose_platform
                                       + '\n' + self.__msg_required_add_release)
            if not self.__arg_download_release:
                print(custom_required_message)
                print(self.__msg_optional_add_extract)
                sys.exit(0)
            if len(self.__arg_download_release) != 2:
                print(custom_required_message)
                print(self.__msg_optional_add_extract)
                sys.exit(0)
            extract = False
            self.__arg_extract = self.__args.extract
            if self.__arg_passed(self.__arg_extract):
                extract = True
            if len(self.__arg_download_release) != 2:
                print(custom_required_message)
                print(self.__msg_optional_add_extract)
                sys.exit(0)
            else:
                platform = self.__arg_download_release[0]
                if platform in self.__platforms.list:
                    release = self.__arg_download_release[1]
                    # noinspection PyBroadException
                    try:
                        self.download_release(platform, release, extract)
                        print(self.__msg_download_finished)
                    except GetChromeDriverError:
                        print(self.__msg_download_error)
                else:
                    print(custom_required_message)
                    print(self.__msg_optional_add_extract)
            sys.exit(0)

        ###########
        # VERSION #
        ###########
        self.__arg_version = self.__args.version
        if self.__arg_passed(self.__arg_version):
            print('v' + __version__)
            sys.exit(0)

    def __arg_passed(self, arg):
        if isinstance(arg, list):
            return True
        return False

    def print_latest_urls(self):
        latest_stable = 'Latest stable release for '

        get_driver = GetChromeDriver(self.__platforms.win)
        print(latest_stable + 'Windows:')
        print(get_driver.latest_stable_release_url())

        print('')

        get_driver = GetChromeDriver(self.__platforms.linux)
        print(latest_stable + 'Linux:')
        print(get_driver.latest_stable_release_url())

        print('')

        get_driver = GetChromeDriver(self.__platforms.mac)
        print(latest_stable + 'Mac:')
        print(get_driver.latest_stable_release_url())

    def print_phase_version(self, phase):
        if phase == self.__phases.beta:
            get_driver = GetChromeDriver(self.__platforms.win)
            beta = get_driver.latest_beta_release_version()
            if beta is None:
                print(self.__c_fore.RED + 'error: could not find a beta release version' + self.__c_style.RESET_ALL)
            else:
                print(beta)
        elif phase == self.__phases.stable:
            get_driver = GetChromeDriver(self.__platforms.win)
            stable = get_driver.latest_stable_release_version()
            if stable is None:
                print(self.__c_fore.RED + 'error: could not find a stable release version' + self.__c_style.RESET_ALL)
            else:
                print(stable)

    def print_phase_url(self, platform, phase):
        get_driver = GetChromeDriver(platform)
        if phase == self.__phases.beta:
            print(get_driver.latest_beta_release_url())
        elif phase == self.__phases.stable:
            print(get_driver.latest_stable_release_url())

    def print_release_url(self, platform, release):
        get_driver = GetChromeDriver(platform)
        print(get_driver.release_url(release))

    def download_latest_phase_release(self, platform, phase, extract):
        if phase == self.__phases.beta:
            get_driver = GetChromeDriver(platform)
            if get_driver.download_latest_beta_release(extract=extract):
                return True
        elif phase == self.__phases.stable:
            get_driver = GetChromeDriver(platform)
            if get_driver.download_latest_stable_release(extract=extract):
                return True

        return False

    def download_release(self, platform, release, extract):
        get_driver = GetChromeDriver(platform)
        get_driver.download_release(release, extract=extract)

