import sys
import argparse
from signal import signal, SIGINT

import colorama

from get_chromedriver.version import __version__
from get_chromedriver import arguments
from get_chromedriver.get_driver import GetChromeDriver
from get_chromedriver.platforms import Platforms
from get_chromedriver.phase import Phase

platforms = Platforms()
phases = Phase()


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
        c_fore = colorama.Fore
        c_style = colorama.Style
        colorama.init()

        msg_download_finished = 'download finished'
        msg_required_choose_platform = (c_fore.RED + 'required: choose one of the following platforms: '
                                        + str(platforms.list) + c_style.RESET_ALL)
        msg_required_add_release = c_fore.RED + 'required: add a release version' + c_style.RESET_ALL
        msg_optional_add_extract = 'optional: add --extract to extract the zip file'
        msg_error_unrecognized_argument = (
                c_fore.RED + 'error: unrecognized argument(s) detected' + c_style.RESET_ALL
                + '\n' + 'tip: use --help to see all available arguments')
        msg_download_error = c_fore.RED + 'error: an error occurred at downloading' + c_style.RESET_ALL
        msg_release_url_error = c_fore.RED + 'error: could not find release url' + c_style.RESET_ALL

        parser = argparse.ArgumentParser(add_help=False)
        for i, arg in enumerate(arguments.args_options):
            parser.add_argument(arguments.args_options[i][0], nargs='*')
        args, unknown = parser.parse_known_args()

        if unknown:
            print(msg_error_unrecognized_argument)
            sys.exit(0)

        if len(sys.argv) == 1:
            arguments.print_help()
            sys.exit(0)

        args_help = args.help
        if isinstance(args_help, list):
            arguments.print_help()
            sys.exit(0)

        args_beta_version = args.beta_version
        if isinstance(args_beta_version, list):
            self.print_phase_version(phases.beta)
            sys.exit(0)

        args_stable_version = args.stable_version
        if isinstance(args_stable_version, list):
            self.print_phase_version(phases.stable)
            sys.exit(0)

        args_latest_urls = args.latest_urls
        if isinstance(args_latest_urls, list):
            self.print_url_phases_release()
            sys.exit(0)

        args_release_url = args.release_url
        if isinstance(args_release_url, list):
            custom_required_message = (msg_required_choose_platform
                                       + '\n' + msg_required_add_release)
            if not args_release_url:
                print(custom_required_message)
                sys.exit(0)
            if len(args_release_url) != 2:
                print(custom_required_message)
                sys.exit(0)

            platform = args_release_url[0]
            release = args_release_url[1]
            if platforms.win == platform:
                # noinspection PyBroadException
                try:
                    self.print_release_url(platforms.win, release)
                except Exception:
                    print(msg_release_url_error)
            elif platforms.linux == platform:
                # noinspection PyBroadException
                try:
                    self.print_release_url(platforms.linux, release)
                except Exception:
                    print(msg_release_url_error)
            elif platforms.mac == platform:
                # noinspection PyBroadException
                try:
                    self.print_release_url(platforms.mac, release)
                except Exception:
                    print(msg_release_url_error)
            else:
                print(custom_required_message)
            sys.exit(0)

        args_beta_url = args.beta_url
        if isinstance(args_beta_url, list):
            if not args_beta_url:
                print(msg_required_choose_platform)
                sys.exit(0)
            if len(args_beta_url) != 1:
                print(msg_required_choose_platform)
                sys.exit(0)

            platform = args_beta_url[0]
            if platforms.win == platform:
                # noinspection PyBroadException
                try:
                    self.print_phase_url(platforms.win, phases.beta)
                except Exception:
                    print(msg_release_url_error)
            elif platforms.linux == platform:
                # noinspection PyBroadException
                try:
                    self.print_phase_url(platforms.linux, phases.beta)
                except Exception:
                    print(msg_release_url_error)
            elif platforms.mac == platform:
                # noinspection PyBroadException
                try:
                    self.print_phase_url(platforms.mac, phases.beta)
                except Exception:
                    print(msg_release_url_error)
            else:
                print(msg_required_choose_platform)
            sys.exit(0)

        args_stable_url = args.stable_url
        if isinstance(args_stable_url, list):
            if not args_stable_url:
                print(msg_required_choose_platform)
                sys.exit(0)
            if len(args_stable_url) != 1:
                print(msg_required_choose_platform)
                sys.exit(0)

            platform = args_stable_url[0]
            if platforms.win == platform:
                # noinspection PyBroadException
                try:
                    self.print_phase_url(platforms.win, phases.stable)
                except Exception:
                    print(msg_release_url_error)
            elif platforms.linux == platform:
                # noinspection PyBroadException
                try:
                    self.print_phase_url(platforms.linux, phases.stable)
                except Exception:
                    print(msg_release_url_error)
            elif platforms.mac == platform:
                # noinspection PyBroadException
                try:
                    self.print_phase_url(platforms.mac, phases.stable)
                except Exception:
                    print(msg_release_url_error)
            else:
                print(msg_required_choose_platform)
            sys.exit(0)

        args_download_beta = args.download_beta
        if isinstance(args_download_beta, list):
            if not args_download_beta:
                print(msg_required_choose_platform)
                print(msg_optional_add_extract)
                sys.exit(0)
            extract = False
            args_extract = args.extract
            if isinstance(args_extract, list):
                extract = True
            platform = args_download_beta[0]
            if platform in platforms.list:
                # noinspection PyBroadException
                try:
                    self.download_latest_phase_release(platform, phases.beta, extract)
                    print(msg_download_finished)
                except Exception:
                    print(msg_download_error)
            else:
                print(msg_required_choose_platform)
                print(msg_optional_add_extract)
            sys.exit(0)

        args_download_stable = args.download_stable
        if isinstance(args_download_stable, list):
            if not args_download_stable:
                print(msg_required_choose_platform)
                print(msg_optional_add_extract)
                sys.exit(0)
            extract = False
            args_extract = args.extract
            if isinstance(args_extract, list):
                extract = True
            platform = args_download_stable[0]
            if platform in platforms.list:
                # noinspection PyBroadException
                try:
                    self.download_latest_phase_release(platform, phases.stable, extract)
                    print(msg_download_finished)
                except Exception:
                    print(msg_download_error)
            else:
                print(msg_required_choose_platform)
                print(msg_optional_add_extract)
            sys.exit(0)

        args_download_release = args.download_release
        if isinstance(args_download_release, list):
            custom_required_message = (msg_required_choose_platform
                                       + '\n' + msg_required_add_release)
            if not args_download_release:
                print(custom_required_message)
                print(msg_optional_add_extract)
                sys.exit(0)
            if len(args_download_release) != 2:
                print(custom_required_message)
                print(msg_optional_add_extract)
                sys.exit(0)
            extract = False
            args_extract = args.extract
            if isinstance(args_extract, list):
                extract = True
            if len(args_download_release) != 2:
                print(custom_required_message)
                print(msg_optional_add_extract)
                sys.exit(0)
            else:
                platform = args_download_release[0]
                if platform in platforms.list:
                    release = args_download_release[1]
                    # noinspection PyBroadException
                    try:
                        self.download_release(platform, release, extract)
                        print(msg_download_finished)
                    except Exception:
                        print(msg_download_error)
                else:
                    print(custom_required_message)
                    print(msg_optional_add_extract)
            sys.exit(0)

        args_version = args.version
        if isinstance(args_version, list):
            print('v' + __version__)
            sys.exit(0)

    def print_url_phases_release(self):
        latest_beta = 'Latest beta release for '
        latest_stable = 'Latest stable release for '

        get_driver = GetChromeDriver(platforms.win)
        print(latest_beta + 'Windows:')
        print(get_driver.latest_beta_release_url())

        print('')

        get_driver = GetChromeDriver(platforms.linux)
        print(latest_beta + 'Linux:')
        print(get_driver.latest_beta_release_url())

        print('')

        get_driver = GetChromeDriver(platforms.mac)
        print(latest_beta + 'Mac:')
        print(get_driver.latest_beta_release_url())

        print('')

        get_driver = GetChromeDriver(platforms.win)
        print(latest_stable + 'Windows:')
        print(get_driver.latest_stable_release_url())

        print('')

        get_driver = GetChromeDriver(platforms.linux)
        print(latest_stable + 'Linux:')
        print(get_driver.latest_stable_release_url())

        print('')

        get_driver = GetChromeDriver(platforms.mac)
        print(latest_stable + 'Mac:')
        print(get_driver.latest_stable_release_url())

    def print_phase_version(self, phase):
        if phase == phases.beta:
            get_driver = GetChromeDriver(platforms.win)
            print(get_driver.latest_beta_release_version())
        elif phase == phases.stable:
            get_driver = GetChromeDriver(platforms.win)
            print(get_driver.latest_stable_release_version())

    def print_phase_url(self, platform, phase):
        get_driver = GetChromeDriver(platform)
        if phase == phases.beta:
            print(get_driver.latest_beta_release_url())
        elif phase == phases.stable:
            print(get_driver.latest_stable_release_url())

    def print_release_url(self, platform, release):
        get_driver = GetChromeDriver(platform)
        print(get_driver.release_url(release))

    def download_latest_phase_release(self, platform, phase, extract):
        if phase == phases.beta:
            get_driver = GetChromeDriver(platform)
            get_driver.download_latest_beta_release(extract=extract)
        elif phase == phases.stable:
            get_driver = GetChromeDriver(platform)
            get_driver.download_latest_stable_release(extract=extract)

    def download_release(self, platform, release, extract):
        get_driver = GetChromeDriver(platform)
        get_driver.download_release(release, extract=extract)


if __name__ == '__main__':
    main()
