descriptor = '  {:<30} {}'
message_help_required_version = descriptor.format('', 'required: add a version')
message_help_optional_extract = descriptor.format('', 'optional: use --extract to extract the zip file')

args_options = [
    ['--beta-version', 'print the beta version'],
    ['--stable-version', 'print the stable version'],
    ['--latest-urls', 'print the beta and stable version urls for all platforms'],
    ['--version-url', 'print the version url' + '\n'
     + message_help_required_version],
    ['--beta-url', 'print the beta version url'],
    ['--stable-url', 'print the stable version url'],
    ['--auto-download', 'download a ChromeDriver version for the installed Chrome Version' + '\n'
     + message_help_optional_extract],
    ['--download-beta', 'download the beta version' + '\n'
     + message_help_optional_extract],
    ['--download-stable', 'download the stable version' + '\n'
     + message_help_optional_extract],
    ['--download-version', 'download a specific version' + '\n'
     + message_help_required_version + '\n'
     + message_help_optional_extract],
    ['--extract', 'extract the compressed driver file'],
    ['--version', 'program version'],
    ['--help', 'show help']
]


def print_help():
    print('usage: ' + 'get-chrome-driver' + ' [options]')
    print('')
    print('options: ')
    for i, argument in enumerate(args_options):
        print(descriptor.format(argument[0], argument[1]))
    print('')
    print('The downloaded driver can be found at: ')
    print('<current directory>/<chromedriver>/<version>/<bin>/<chromedriver>')
