import os
import requests
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
from urllib.parse import urlparse
from requests.exceptions import RequestException
from requests.exceptions import HTTPError


def download(url, output_path='', file_name=''):
    """
    Download a file from url
    If output_path is '', the file will be downloaded directly into the current directory
    If file_name is '', the file name from the url will be used
    """

    session = __retry_session(retries=3,
                              backoff_factor=0.1,
                              status_forcelist=[429, 500, 502, 503, 504],
                              method_whitelist=['GET'])
    try:
        res = session.get(url=url)
    except RequestException as err:
        raise RequestException(err)
    else:
        if res.status_code != 200:
            raise HTTPError('Invalid URL')

        if file_name == '' or None:
            # Get the file name from the url
            file_name = get_file_name_from_url(url)

        if output_path == '' or None:
            # The full path will be the file name if no output path was given
            full_output_path = file_name
        else:
            # The full path will be the given output path with the file name at the end
            __create_dir(output_path)
            full_output_path = output_path + '/' + file_name

        with open(full_output_path, 'wb') as file:
            # Download the file in chunks
            for chunk in res.iter_content(chunk_size=1048576):
                if chunk:
                    file.write(chunk)
        return full_output_path, file_name
    finally:
        session.close()


def __retry_session(retries, backoff_factor, status_forcelist, method_whitelist):
    """ Retry session """

    retry = Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist,
        allowed_methods=method_whitelist)

    adapter = HTTPAdapter(max_retries=retry)
    session = requests.Session()
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session


def get_file_name_from_url(url):
    """ Get file name from url """

    path = urlparse(url).path
    return path.split('/')[-1]


def __create_dir(directory):
    """ Create a directory """

    try:
        os.makedirs(directory, exist_ok=True)
    except OSError as err:
        raise OSError(err)
