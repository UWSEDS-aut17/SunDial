import urllib
from urllib import request
import os
import hashlib
import pandas as pd
import zipfile



def get_data(url,ext):
    """Download file from URL to filename
    If filename is present, then skip download.
    ext is string for datatype (e.g. 'csv', 'xml')
    """
    url_hash = hashlib.sha224(url.encode()).hexdigest()
    filename = url_hash[:7] + '.' + ext
    try:
        if os.path.exists(filename):
            print('File already present')
            return filename
        else:
            print('Downloading', filename)
            request.urlretrieve(url, filename)
            #For data that is downloaded as zip files, need to
            #Extract the zip, then return name from extracted file
            #Haven't included zip capabilities in remove_data yet 
            #(remove_data) just removes zip file not extracted files
            if ext == 'zip':
                print('Extracting zip')
                zip_ref = zipfile.ZipFile(filename, 'r')
                zip_ref.extractall()              
                for name in zip_ref.namelist():
                    localFilePath = zip_ref.extract(name, '/tmp/')
                    extracted_fn = zip_ref.extract(name, '/tmp/')               

                zip_ref.close()
                return extracted_fn[5:]
            else:
                return filename
    except urllib.error.HTTPError:
        print('Invalid URL')
        return None


def remove_data(url,ext):
    """Remove data in filename
    from directory
    """
    url_hash = hashlib.sha224(url.encode()).hexdigest()
    filename = url_hash[:7] + '.' + ext
    if os.path.exists(filename):
        os.remove(filename)
        print('Removed', filename)
    else:
        print('File is not present')
