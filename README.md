# Get ChromeDriver

[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/get-chrome-driver?color=blue)](https://pypi.python.org/pypi/get-chrome-driver)
[![PyPI](https://img.shields.io/pypi/v/get-chrome-driver?color=blue)](https://pypi.python.org/pypi/get-chrome-driver)
[![PyPI - License](https://img.shields.io/pypi/l/get-chrome-driver)](https://pypi.python.org/pypi/get-chrome-driver)

[![tests](https://github.com/zaironjacobs/get-chrome-driver/actions/workflows/test.yml/badge.svg)](https://github.com/zaironjacobs/get-chrome-driver/actions/workflows/test.yml)

A tool to download and install ChromeDriver. Automatically download a ChromeDriver version for the current installed
Chrome version. Or you can choose to download the beta version (if one is currently available), the stable version or
another specific version. You can use this tool as a package import or as a command-line application.

## Install

To install:

```console
pip install get-chrome-driver
```

To upgrade:

```console
pip install get-chrome-driver --upgrade
```

## Usage

#### Install and use ChromeDriver with Selenium

```Python
import time
from get_chrome_driver import GetChromeDriver
from selenium import webdriver

# Install the driver:
# Downloads ChromeDriver for the installed Chrome version on the machine
# Adds the downloaded ChromeDriver to path
get_driver = GetChromeDriver()
get_driver.install()

# Use the installed ChromeDriver with Selenium
driver = webdriver.Chrome()
driver.get("https://google.com")
time.sleep(3)
driver.quit()
```

#### For downloading only

```Python
from get_chrome_driver import GetChromeDriver

get_driver = GetChromeDriver()

# Print the stable version
print(get_driver.stable_version())

# Print the stable version download link
print(get_driver.stable_version_url())

# Print the download link of a specific version
print(get_driver.version_url('84.0.4147.30'))

# Auto download ChromeDriver for the installed Chrome version
# Optional: use output_path= to specify where to download the driver
# Optional: use extract=True to extract the file
get_driver.auto_download(extract=True)

# Download the stable driver version
# Optional: use output_path= to specify where to download the driver
# Optional: use extract=True to extract the zip file
get_driver.download_stable_version(extract=True)

# Download a specific driver version
# Optional: use output_path= to specify where to download the driver
# Optional: use extract=True to extract the file
get_driver.download_version('84.0.4147.30', extract=True)
```

#### Command-line

Print the stable version url of all platforms:

```console
get-chrome-driver --latest-urls
```

Print the stable version:

```console
get-chrome-driver --stable-version
```

Print the stable version url:

```console
get-chrome-driver --stable-url
```

Auto download ChromeDriver for the current installed Chrome version and extract the file:

```console
get-chrome-driver --auto-download --extract
```

Download the stable version and extract the file:

```console
get-chrome-driver --download-stable --extract
```

Download a specific version and extract the file:

```console
get-chrome-driver --download-version 84.0.4147.30 --extract
```

#### The downloaded driver can be found at:

*`<current directory>/<chromedriver>/<version>/<bin>/<chromedriver>`*

*Note: Beta version related options and functions will only work if one is currently available.*

### Options

```
--help                      Show help.

--beta-version              Print the beta version.

--stable-version            Print the stable version.

--latest-urls               Print the beta and stable version urls for all platforms.

--version-url               Print the url of a version.

--beta-url                  Print the beta version url.

--stable-url                Print the stable version url.

--auto-download             Download a ChromeDriver version for the installed Chrome Version.

--chromium                  Auto download will look for the installed Chromium version instead of Chrome.

--download-beta             Download the beta version.

--download-stable           Download the stable version.

--download-version          Download a specific version.

--extract                   Extract the compressed driver file.

--driver-filename           Print the driver filename.

--version                   App version.
```
