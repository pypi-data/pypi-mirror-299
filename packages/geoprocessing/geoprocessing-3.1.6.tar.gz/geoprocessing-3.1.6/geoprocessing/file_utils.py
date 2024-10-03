import os
import requests
from urllib.parse import urlparse


def download(url: str, fileName: str):
    req = requests.get(url)
    file = open(fileName, 'wb')
    for chunk in req.iter_content(100000):
        file.write(chunk)
    file.close()


def download_url(folder: str, url: str):
    url_parsed = urlparse(url)
    filename = os.path.basename(url_parsed.path)
    dest = f"{folder}/{filename}"
    if os.path.isfile(dest):
        return
    download(url, dest)
    return dest


def download_shapefile(dest: str, base_url: str):
    def download_files(filename: str):
        download_url(dest, f"{base_url}/{filename}.shp")
        download_url(dest, f"{base_url}/{filename}.dbf")
        download_url(dest, f"{base_url}/{filename}.shx")
    return download_files


def mkdirs(dest: str):
    if not os.path.isdir(dest):
        os.makedirs(dest)


def has_ext(ext: str) -> bool:
    def compare(file: str): return os.path.splitext(file)[1] == ext
    return compare
