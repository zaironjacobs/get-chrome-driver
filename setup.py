from setuptools import setup
from setuptools import find_packages

name = "get-chrome-driver"
version = "1.5.1"

with open("README.md", "r") as fh:
    long_description = fh.read()

requires = [
    "beautifulsoup4==4.13.5",
    "requests==2.32.5",
    "urllib3==2.5.0",
    "typer==0.17.4",
]

setup(
    name=name,
    version=version,
    author="Zairon Jacobs",
    author_email="zaironjacobs@gmail.com",
    description="A tool to download and install ChromeDriver.",
    long_description=long_description,
    url="https://github.com/zaironjacobs/get-chrome-driver",
    download_url=f"https://github.com/zaironjacobs/get-chrome-driver/archive/v{version}.tar.gz",
    keywords=["chrome", "chromedriver", "download", "install", "web", "driver", "tool"],
    packages=find_packages(),
    entry_points={
        "console_scripts": [f"{name}=get_chrome_driver.app:app"],
    },
    install_requires=requires,
    license="MIT",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.11",
        "Natural Language :: English",
    ],
    python_requires=">=3",
)
