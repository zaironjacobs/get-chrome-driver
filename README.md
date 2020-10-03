Get ChromeDriver
=================
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/get-chromedriver?color=blue)](https://pypi.python.org/pypi/get-chromedriver)
[![PyPI](https://img.shields.io/pypi/v/get-chromedriver?color=blue)](https://pypi.python.org/pypi/get-chromedriver)
[![PyPI - Status](https://img.shields.io/pypi/status/get-chromedriver)](https://pypi.python.org/pypi/get-chromedriver)
[![PyPI - License](https://img.shields.io/pypi/l/get-chromedriver)](https://pypi.python.org/pypi/get-chromedriver)

A tool to download ChromeDriver. You can choose to download the latest beta release, the latest stable release 
or a specific release. You can use this tool as a package import or as a command-line application.

## Install
To install:
```console
$ pip install get-chromedriver
```

To upgrade:
```console
$ pip install get-chromedriver --upgrade
```

## Usage

#### Package import


```Python
from get_chromedriver import GetChromeDriver

# Platforms to choose from: 'win', 'linux' or 'mac'
get_driver = GetChromeDriver(platform='win')

# Print the version of the latest stable release
print(get_driver.latest_stable_release_version())

# Print the version of the latest beta release
print(get_driver.latest_beta_release_version())

# Print the url of the latest stable release
print(get_driver.latest_stable_release_url())

# Print the url of the latest beta release
print(get_driver.latest_beta_release_url())

# Print the url of a specific release
print(get_driver.release_url('84.0.4147.30'))

# Download the latest stable driver release
# Optional: "extract" (boolean) can be passed as an argument to extract the zip file
get_driver.download_latest_stable_release(extract=True)

# Download the latest beta driver release
# Optional: use output_path='' to specify where to download the driver
# Optional: use extract=True to extract the zip file
get_driver.download_latest_beta_release(output_path='webdriver')

# Optional: use output_path='' to specify where to download the driver
# Optional: use extract=True to extract the zip file
get_driver.download_release('84.0.4147.30', extract=True)
```

#### Command-line
Print the beta and stable release urls of all available platforms:
```console
$ get-chromedriver --latest-urls
```

Print the beta and stable release version:
```console
$ get-chromedriver --beta-version
$ get-chromedriver --stable-version
```

Print the beta and stable release urls for a specific platform:
```console
$ get-chromedriver --beta-url linux
$ get-chromedriver --stable-url linux
```

Download the beta and stable chromedriver release for a specific platform:
```console
$ get-chromedriver --download-beta win
$ get-chromedriver --download-stable win
```

Download a specific chromedriver release for a specific platform and extract the zip file:
```console
$ get-chromedriver --download-release mac 84.0.4147.30 --extract
```

#### Downloaded drivers can be found at:

*`<current directory>/<get-chromedriver_downloads>/<release version>/<platform>/<chromedriver.zip>`*

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

--downlaod-stable           Download the stable release for a platform.

--downlaod-release          Download a release.

--extract                   Option to extract the zip file.

--version                   Program version.
```