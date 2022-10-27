import os
import shutil
import subprocess
import zipfile
from abc import ABC
from urllib.parse import urlparse

import boto3
from botocore.exceptions import ClientError
import requests
from rich import print


def is_http(url):
    if url[0:4] == "http":
        return True
    return False


def is_aws_s3(url):
    if url[0:5] == "s3://":
        return True
    return False


def is_local(url):
    return os.path.exists(url)


def get_source(geometry_type, table_name, download_url, is_zip, unzip_filename):
    if is_zip:
        return ZipSource(geometry_type, table_name, download_url, unzip_filename)
    else:
        return UnzipSource(geometry_type, table_name, download_url)


def http_download_file(url, destination_path):
    r = requests.get(url, allow_redirects=True)
    with open(destination_path, "wb+") as f:
        f.write(r.content)


def copy_local_file(source_path, destination_path):
    shutil.copy(source_path, destination_path)


def aws_download_file(destination, file_name, bucket, aws_access_key_id, aws_secret_access_key):
    try:
        resource = boto3.resource('s3', aws_access_key_id=aws_access_key_id,
                                  aws_secret_access_key=aws_secret_access_key)
        my_bucket = resource.Bucket(bucket)
        my_bucket.download_file(file_name, destination)
    except ClientError as e:
        raise ValueError("AWS S3 download failed: {}".format(e))


def is_shp_zip(zip_path):
    zip_data = zipfile.ZipFile(zip_path)
    zip_infos = zip_data.infolist()

    num_shp = 0
    for f in zip_infos:
        if f.filename.split('.')[-1] == 'shp':
            num_shp += 1

    if num_shp != 1:
        return False

    return True


def unzip_file(zip_path, destination_filename, destination_folder):
    zip_data = zipfile.ZipFile(zip_path)
    zip_infos = zip_data.infolist()

    if len(zip_infos) > 1 and not is_shp_zip(zip_path):
        raise ValueError("Zip file contains more than one file")

    zip_infos[0].filename = destination_filename
    zip_data.extract(zip_infos[0])
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(destination_folder)


class Source(ABC):
    def __init__(self, geometry_type, table_name, download_url):
        self.type = geometry_type
        self.table_name = table_name
        self.download_url = download_url
        self.downloaded_path = None

    def __repr__(self):
        return f"Source(type={self.type}, table_name={self.table_name}, download_url={self.download_url})"

    def download(self, destination_folder, aws_access_key_id=None, aws_secret_access_key=None, force_download=False, ):
        path = urlparse(self.download_url).path
        ext = os.path.splitext(path)[1]
        self.downloaded_path = os.path.join(destination_folder, self.table_name + ext)

        if is_http(self.download_url):
            http_download_file(self.download_url, self.downloaded_path)
        elif is_aws_s3(self.download_url):
            p = urlparse(self.download_url, allow_fragments=False)
            bucket = p.netloc
            file_path = p.path[1:]  # contains '/' if not indexing from [1:]
            aws_download_file(self.downloaded_path, file_path, bucket, aws_access_key_id, aws_secret_access_key)
        elif is_local(self.download_url):
            copy_local_file(self.download_url, self.downloaded_path)
        else:
            raise ValueError(f"Did you provide a valid http or s3 url for the source: {self.table_name}?")

    def import_to_database(self, host, port, database, user, password, schema, target_projection):
        cmd = f"""ogr2ogr -progress -t_srs "EPSG:{target_projection}" -f "PostgreSQL" PG:"host='{host}' port='{port}' dbname='{database}' user='{user}' password='{password}'" -lco SCHEMA={schema} -nlt PROMOTE_TO_MULTI -nln {self.table_name} {self.downloaded_path} -overwrite"""
        print(self.__repr__())
        print(cmd)
        p = subprocess.Popen(cmd, shell=True)
        p.wait()


class UnzipSource(Source):
    pass


class ZipSource(Source):
    def __init__(self, geometry_type, table_name, download_url, unzip_filename):
        super().__init__(geometry_type, table_name, download_url)
        self.unzip_filename = unzip_filename

    def download(self, destination_folder, aws_access_key_id=None, aws_secret_access_key=None, force_download=False):
        super().download(destination_folder, aws_access_key_id, aws_secret_access_key, force_download)

        final_unzip = os.path.join(destination_folder, self.unzip_filename)
        if force_download or not os.path.exists(final_unzip):
            unzip_file(self.downloaded_path, self.unzip_filename, destination_folder)

        self.downloaded_path = final_unzip
