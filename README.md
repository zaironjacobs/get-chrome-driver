Get ChromeDriver
=================
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/get-chrome-driver?color=blue)](https://pypi.python.org/pypi/get-chrome-driver)
[![PyPI](https://img.shields.io/pypi/v/get-chrome-driver?color=blue)](https://pypi.python.org/pypi/get-chrome-driver)
[![PyPI - Status](https://img.shields.io/pypi/status/get-chrome-driver)](https://pypi.python.org/pypi/get-chrome-driver)
[![PyPI - License](https://img.shields.io/pypi/l/get-chrome-driver)](https://pypi.python.org/pypi/get-chrome-driver)

A tool to download and install ChromeDriver. Automatically download a ChromeDriver version for the current installed
Chrome version. Or you can choose to download the beta release (if one is currently available), the stable release or
another specific release. You can use this tool as a package import or as a command-line application.

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

#### Install and use ChromeDriver with Selenium

```Python
import time
from get_chrome_driver import GetChromeDriver
from selenium import webdriver

# Install the driver:
# Downloads a ChromeDriver version that matches the installed Chrome version on the machine
# Adds the downloaded ChromeDriver to path
get_driver = GetChromeDriver()
get_driver.auto_install()

# Use the installed ChromeDriver with Selenium
chrome_driver = webdriver.Chrome()
chrome_driver.get("https://google.com")
time.sleep(3)
chrome_driver.quit()
```

#### For downloading only

```Python
from get_chrome_driver import GetChromeDriver

get_driver = GetChromeDriver()

# Print the stable release version
print(get_driver.stable_release_version())

# Print the stable release download link
print(get_driver.stable_release_url())

# Print the download link of a specific release
print(get_driver.release_url('84.0.4147.30'))

# Auto download ChromeDriver for the installed Chrome version
# Optional: use output_path= to specify where to download the driver
# Optional: use extract=True to extract the zip file
get_driver.auto_download(extract=True)

# Download the stable driver release
# Optional: use output_path= to specify where to download the driver
# Optional: use extract=True to extract the zip file
get_driver.download_stable_release(extract=True)

# Download a specific driver release
# Optional: use output_path= to specify where to download the driver
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

Print the stable release url:

```console
$ get-chrome-driver --stable-url
```

Auto download ChromeDriver for the current installed Chrome version and extract the file:

```console
$ get-chrome-driver --auto-download --extract
```

Download the stable release and extract the file:

```console
$ get-chrome-driver --download-stable --extract
```

Download a specific release and extract the file:

```console
$ get-chrome-driver --download-release 84.0.4147.30 --extract
```

#### The downloaded driver can be found at:

*`<current directory>/<chromedriver>/<version>/<bin>/<chromedriver>`*

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

--auto-download             Auto download ChromeDriver for the installed Chrome Version

--download-beta             Download the beta release for a platform.

--download-stable           Download the stable release for a platform.

--download-release          Download a release.

--extract                   Option to extract the zip file.

--version                   Program version.
```
