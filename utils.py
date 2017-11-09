import urllib
from urllib import request
import os
import hashlib
import pandas as pd


def get_data(url):
    """Download file from URL to filename
    If filename is present, then skip download.
    """
    url_hash = hashlib.sha224(url.encode()).hexdigest()
    filename = url_hash[:7] + '.csv'
    try:
        if os.path.exists(filename):
            print('File already present')
        else:
            print('Downloading', filename)
            request.urlretrieve(url, filename)
    except urllib.error.HTTPError:
        print('Invalid URL')
        return None


def remove_data(url):
    """Remove data in filename
    from directory
    """
    url_hash = hashlib.sha224(url.encode()).hexdigest()
    filename = url_hash[:7] + '.csv'
    if os.path.exists(filename):
        os.remove(filename)
        print('Removed', filename)
    else:
        print('File is not present')
