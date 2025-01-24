import os
import requests
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
from urllib.parse import urlparse
from requests.exceptions import RequestException
from requests.exceptions import HTTPError


def download(url: str, output_path: str = None, file_name: str = None):
    """
    Download a file from url.
    If output_path is None, the file will be downloaded directly at the current directory.
    If file_name is None, the file name from the url will be used.
    """

    session = __retry_session(
        retries=3,
        backoff_factor=0.1,
        status_forcelist=[429, 500, 502, 503, 504],
        method_whitelist=["GET"],
    )
    try:
        res = session.get(url=url)
    except RequestException as err:
        raise RequestException(err)
    else:
        if res.status_code != 200:
            raise HTTPError("Invalid URL")

        if file_name == "" or file_name is None:
            # Get the file name from the url
            file_name = __get_file_name_from_url(url)

        if output_path == "" or output_path is None:
            file_path = file_name
        else:
            __makedirs(output_path)
            file_path = output_path + "/" + file_name

        with open(file_path, "wb") as file:
            # Download the file in chunks
            for chunk in res.iter_content(chunk_size=1048576):
                if chunk:
                    file.write(chunk)

        return file_path, file_name
    finally:
        session.close()


def __retry_session(
    retries: int, backoff_factor: float, status_forcelist: any, method_whitelist: any
):
    """
    Retry session.
    """

    retry = Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist,
        allowed_methods=method_whitelist,
    )

    adapter = HTTPAdapter(max_retries=retry)
    session = requests.Session()
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    return session


def __get_file_name_from_url(url: str):
    """
    Get file name from url.
    """

    path = urlparse(url).path

    return path.split("/")[-1]


def __makedirs(path: str):
    """
    Make dirs.
    """

    try:
        if not os.path.exists(path):
            os.makedirs(path, exist_ok=True)
    except OSError as err:
        raise OSError(err)
