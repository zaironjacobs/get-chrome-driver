from setuptools import setup
from setuptools import find_packages
from get_chromedriver.version import __version__
from get_chromedriver.console_name import __console_name__

with open('README.md', 'r') as fh:
    long_description = fh.read()

requires = [
    'bs4>=0.0.1',
    'requests>=2.24.0',
    'colorama>=0.4.3',
    'pytest>=6.1.0'
]

setup(
    name=__console_name__,
    version=__version__,
    author='Zairon Jacobs',
    author_email='zaironjacobs@gmail.com',
    description='A tool to download ChromeDriver.',
    long_description=long_description,
    url='https://github.com/zaironjacobs/get-chromedriver',
    download_url='https://github.com/zaironjacobs/get-chromedriver/archive/v' + __version__ + '.tar.gz',
    keywords=['chrome', 'chromedriver', 'download', 'web', 'driver', 'tool', 'get'],
    packages=find_packages(),
    entry_points={
        'console_scripts': [__console_name__ + '=get_chromedriver.app:main'],
    },
    install_requires=requires,
    license='MIT',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.8',
        'Natural Language :: English'
    ],
    python_requires='>=3.8',
)
