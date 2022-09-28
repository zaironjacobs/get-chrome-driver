from setuptools import setup
from setuptools import find_packages

name = 'get-chrome-driver'
version = '1.3.5'

with open('README.md', 'r') as fh:
    long_description = fh.read()

with open('requirements.txt') as f:
    requires = f.read().splitlines()

setup(
    name=name,
    version=version,
    author='Zairon Jacobs',
    author_email='zaironjacobs@gmail.com',
    description='A tool to download and install ChromeDriver.',
    long_description=long_description,
    url='https://github.com/zaironjacobs/get-chrome-driver',
    download_url=f'https://github.com/zaironjacobs/get-chrome-driver/archive/v{version}.tar.gz',
    keywords=['chrome', 'chromedriver', 'download', 'install', 'web', 'driver', 'tool'],
    packages=find_packages(),
    entry_points={
        'console_scripts': [f'{name}=get_chrome_driver.app:app'],
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
    python_requires='>=3',
)
