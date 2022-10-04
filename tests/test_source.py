import os.path
import shutil

import pytest
import yaml

from yogrt.source import ZipSource, UnzipSource, is_local, is_aws_s3, is_http


def test_source_download_zip():
    source = ZipSource(geometry_type="polygon", table_name="ldc",
                       download_url="https://www.oeb.ca/documents/opendata/open-data-electricity-map-20220131.zip",
                       unzip_filename="Electric_220131.kmz")
    source.download("./test_tmp")
    assert os.path.exists("./test_tmp/Electric_220131.kmz")
    shutil.rmtree('./test_tmp')
    os.mkdir('./test_tmp')


def test_source_download_not_zip():
    source = UnzipSource(geometry_type="polygon", table_name="ldc",
                         download_url="https://datahub.io/core/geo-countries/r/countries.geojson")
    source.download("./test_tmp")
    assert os.path.exists("./test_tmp/countries.geojson")
    shutil.rmtree('./test_tmp')
    os.mkdir('./test_tmp')


def test_source_import_to_db():
    source = UnzipSource(geometry_type="polygon", table_name="ldc",
                         download_url="https://datahub.io/core/geo-countries/r/countries.geojson")
    source.download("./test_tmp")
    # requires the postgres to be spun up with `docker-compose up -d`
    source.import_to_database("localhost", "3434", "postgres", "postgres", "bidone", "public", "4326")
    shutil.rmtree('./test_tmp')
    os.mkdir('./test_tmp')


def test_get_download_cmd_aws():
    source = UnzipSource(geometry_type="polygon", table_name="ldc",
                         download_url="s3://countries.geojson")
    cmd = source.get_download_cmd("aws_access_key_id", "aws_secret_access_key", "./test_tmp")
    assert cmd == "AWS_ACCESS_KEY_ID=aws_access_key_id AWS_SECRET_ACCESS_KEY=aws_secret_access_key aws s3 cp s3://countries.geojson ./test_tmp"


def test_get_download_cmd_https():
    source = UnzipSource(geometry_type="polygon", table_name="ldc",
                         download_url="https://datahub.io/core/geo-countries/r/countries.geojson")
    cmd = source.get_download_cmd("aws_access_key_id", "aws_secret_access_key", "./test_tmp")
    assert cmd == "wget https://datahub.io/core/geo-countries/r/countries.geojson -P ./test_tmp -q"


def test_get_download_cmd_local():
    source = UnzipSource(geometry_type="polygon", table_name="ldc", download_url="countries.geojson")
    open("countries.geojson", "w").close()
    cmd = source.get_download_cmd("aws_access_key_id", "aws_secret_access_key", "./test_tmp")
    assert cmd == "cp countries.geojson ./test_tmp"
    os.remove("countries.geojson")


def test_get_download_cmd_value_error():
    source = UnzipSource(geometry_type="polygon", table_name="ldc", download_url="countries.geojson")
    with pytest.raises(ValueError):
        source.get_download_cmd("aws_access_key_id", "aws_secret_access_key", "./test_tmp")


def test_is_aws_s3():
    assert is_aws_s3("s3://countries.geojson")
    assert not is_aws_s3("https://datahub.io/core/geo-countries/r/countries.geojson")


def test_is_local():
    open("./test_tmp/countries.geojson", "w").close()
    assert is_local("./test_tmp/countries.geojson")
    assert not is_local("https://datahub.io/core/geo-countries/r/countries.geojson")
    shutil.rmtree('./test_tmp')
    os.mkdir('./test_tmp')


def test_is_http():
    assert is_http("https://datahub.io/core/geo-countries/r/countries.geojson")
    assert not is_http("s3://countries.geojson")


def test_repr():
    source = UnzipSource(geometry_type="polygon", table_name="ldc", download_url="countries.geojson")
    assert source.__repr__() == f"Source(type=polygon, table_name=ldc, download_url=countries.geojson)"


def test_shp_s3_source():
    source = ZipSource(geometry_type="polygon", table_name="countries",
                       download_url="s3://anagraph-public-bucket/countries.zip", unzip_filename="countries.shp")
    source.download("./test_tmp", os.environ["AWS_S3_ACCESS_KEY_ID"], os.environ["AWS_S3_SECRET_ACCESS_KEY"])
    print(source.downloaded_path)
