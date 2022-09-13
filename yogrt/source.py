import os
import shutil
import subprocess
import logging
from abc import ABC

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

    return True


def copy_local_file(source_path, destination_path):
    shutil.copy(source_path, destination_path)

    return True


def aws_download_file(destination_folder, file_name, bucket, aws_access_key_id, aws_secret_access_key):
    """Upload a file to an S3 bucket

    :param destination_folder: The folder to download the file to
    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :return: True if file was uploaded, else False
    """

    s3_client = boto3.client('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)
    try:
        with open(os.path.join(destination_folder, file_name), "w+") as f:
            s3_client.download_fileobj(bucket, file_name, f)
    except ClientError as e:
        logging.error(e)
        return False

    return True


class Source(ABC):
    def __init__(self, geometry_type, table_name, download_url):
        self.type = geometry_type
        self.table_name = table_name
        self.download_url = download_url
        self.downloaded_path = None

    def __repr__(self):
        return f"Source(type={self.type}, table_name={self.table_name}, download_url={self.download_url})"

    def download(self, destination_folder, aws_access_key_id=None, aws_secret_access_key=None, force_download=False):
        if is_http(self.download_url):
            http_download_file(self.download_url, os.path.join(destination_folder, self.table_name))
        elif is_aws_s3(self.download_url):
            aws_download_file(destination_folder, self.table_name, self.download_url[5:], aws_access_key_id,
                              aws_secret_access_key)
        elif is_local(self.download_url):
            copy_local_file(self.download_url, os.path.join(destination_folder, self.table_name))
        else:
            raise ValueError(f"Did you provide a valid http or s3 url for the source: {self.table_name}?")

        self.downloaded_path = os.path.join(destination_folder, os.path.basename(self.download_url))

    def import_to_database(self, host, port, database, user, password, schema, target_projection):
        cmd = f"""ogr2ogr -progress -t_srs "EPSG:{target_projection}" -f "PostgreSQL" PG:"host='{host}' port='{port}' dbname='{database}' user='{user}' password='{password}'" -lco SCHEMA={schema} -nlt PROMOTE_TO_MULTI -nln {self.table_name} {self.downloaded_path} -overwrite"""
        print(self.__repr__())
        print(cmd)
        p = subprocess.Popen(cmd, shell=True)
        p.wait()


class UnzipSource(Source):
    pass


class ZipSource(Source):
    def __init__(self, geometry_type, table_name, download_url, unzip_filename=None):
        super().__init__(geometry_type, table_name, download_url)
        self.unzip_filename = unzip_filename

    def download(self, destination_folder, aws_access_key_id=None, aws_secret_access_key=None, force_download=False):
        super().download(destination_folder, aws_access_key_id, aws_secret_access_key, force_download)

        final_unzip = os.path.join(destination_folder, self.unzip_filename)
        if force_download or not os.path.exists(final_unzip):
            cmd = f"unzip -o {self.downloaded_path} -d {destination_folder}"
            print(cmd)
            p = subprocess.Popen(cmd, shell=True)
            p.wait()
        self.downloaded_path = final_unzip
