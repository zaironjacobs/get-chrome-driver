Get ChromeDriver
=================
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/get-chrome-driver?color=blue)](https://pypi.python.org/pypi/get-chrome-driver)
[![PyPI](https://img.shields.io/pypi/v/get-chrome-driver?color=blue)](https://pypi.python.org/pypi/get-chrome-driver)
[![PyPI - Status](https://img.shields.io/pypi/status/get-chrome-driver)](https://pypi.python.org/pypi/get-chrome-driver)
[![PyPI - License](https://img.shields.io/pypi/l/get-chrome-driver)](https://pypi.python.org/pypi/get-chrome-driver)

A tool to download ChromeDriver. You can choose to download the beta release (if one is currently available), the stable
release or a specific release. You can use this tool as a package import or as a command-line application.

## Install

To install:

```console
$ pip install get-chrome-driver
```

To upgrade:

```console
$ pip install get-chrome-driver --upgrade
```

## Usage

#### Package import

```Python
from get_chrome_driver import GetChromeDriver

# Platforms to choose from: 'win', 'linux' or 'mac'
get_driver = GetChromeDriver(platform='win')

# Print the stable release version
print(get_driver.stable_release_version())

# Print the stable release download link
print(get_driver.stable_release_url())

# Print the download link of a specific release
print(get_driver.release_url('84.0.4147.30'))

# Download the stable driver release
# Optional: use output_path='' to specify where to download the driver
# Optional: use extract=True to extract the zip file
get_driver.download_stable_release(output_path='webdriver', extract=True)

# Download a specific driver release
# Optional: use output_path='' to specify where to download the driver
# Optional: use extract=True to extract the zip file
get_driver.download_release('84.0.4147.30', extract=True)
```

#### Command-line

Print the stable release url of all platforms:

```console
$ get-chrome-driver --latest-urls
```

Print the stable release version:

```console
$ get-chrome-driver --stable-version
```

Print the stable release url of a specific platform:

```console
$ get-chrome-driver --stable-url linux
```

Download the stable release of a specific platform:

```console
$ get-chrome-driver --download-stable win
```

Download a specific release for a specific platform and extract the zip file:

```console
$ get-chrome-driver --download-release mac 84.0.4147.30 --extract
```

#### Downloaded drivers will be downloaded by default at:

*`<current directory>/<chrome_driver_downloads>/<release version>/<platform>/<chromedriver.zip>`*

*Note: Beta release related options and functions will only work if one is currently available.*

### Options

```
--help                      Show help.

--beta-version              Print the beta release version.

--stable-version            Print the stable release version.

--latest-urls               Print the beta and stable release urls for all platforms.

--release-url               Print the url of a release for a platform.

--beta-url                  Print the beta release url for a platform.

--stable-url                Print the stable release url for a platform.

--download-beta             Download the beta release for a platform.

--download-stable           Download the stable release for a platform.

--download-release          Download a release.

--extract                   Option to extract the zip file.

--version                   Program version.
```
