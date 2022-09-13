import os.path
import shutil

import yaml

from yogrt.source import ZipSource, UnzipSource, is_local, is_aws_s3, is_http, aws_download_file


def test_source_download_zip():
    source = ZipSource(geometry_type="polygon", table_name="ldc",
                       download_url="https://www.oeb.ca/documents/opendata/open-data-electricity-map-20220131.zip",
                       unzip_filename="Electric_220131.kmz")
    source.download("./test_tmp")
    assert os.path.exists("./test_tmp/Electric_220131.kmz")
    shutil.rmtree('./test_tmp')
    os.mkdir('./test_tmp')


def test_source_download_not_zip():
    source = UnzipSource(geometry_type="polygon", table_name="countries_1",
                         download_url="https://datahub.io/core/geo-countries/r/countries.geojson")
    source.download("./test_tmp")
    # table named is used to name the downloaded file now
    assert os.path.exists("./test_tmp/countries_1.geojson")
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


def test_aws_download_file():
    secrets_def = yaml.full_load(open("/home/zacharydeziel/Documents/yogrt/yogrt/templates/test_secrets.yaml", "r"))
    aws_download_file(destination="./test_tmp/chief_three_peaks_loop.geojson", file_name="chief_three_peaks_loop.json",
                      bucket="squamish-data", aws_secret_access_key=secrets_def["default"]["s3_secret_access_key"],
                      aws_access_key_id=secrets_def["default"]["s3_access_key_id"])
    assert os.path.exists("./test_tmp/chief_three_peaks_loop.geojson")
