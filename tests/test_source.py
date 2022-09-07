import os.path
import shutil

from yogrt.source import Source


def test_source_download_zip():
    source = Source(geometry_type="polygon", table_name="ldc",
                    download_url="https://www.oeb.ca/documents/opendata/open-data-electricity-map-20220131.zip",
                    unzip_filename="Electric_220131.kmz", is_zip=True)
    source.download("./test_tmp")
    assert os.path.exists("./test_tmp/Electric_220131.kmz")
    shutil.rmtree('./test_tmp')
    os.mkdir('./test_tmp')


def test_source_download_not_zip():
    source = Source(geometry_type="polygon", table_name="ldc",
                    download_url="https://datahub.io/core/geo-countries/r/countries.geojson")
    source.download("./test_tmp")
    assert os.path.exists("./test_tmp/countries.geojson")
    shutil.rmtree('./test_tmp')
    os.mkdir('./test_tmp')


def test_source_import_to_db():
    source = Source(geometry_type="polygon", table_name="ldc",
                    download_url="https://datahub.io/core/geo-countries/r/countries.geojson")
    source.download("./test_tmp")
    # requires the postgres to be spun up with `docker-compose up -d`
    source.import_to_database("localhost", "3434", "postgres", "postgres", "bidone", "public", "4326")
    shutil.rmtree('./test_tmp')
    os.mkdir('./test_tmp')


def test_get_download_cmd_aws():
    source = Source(geometry_type="polygon", table_name="ldc",
                    download_url="s3://countries.geojson")
    cmd = source.get_download_cmd("aws_access_key_id", "aws_secret_access_key", "./test_tmp")
    assert cmd == "AWS_ACCESS_KEY_ID=aws_access_key_id AWS_SECRET_ACCESS_KEY=aws_secret_access_key aws s3 cp s3://countries.geojson ./test_tmp"


def test_get_download_cmd_https():
    source = Source(geometry_type="polygon", table_name="ldc",
                    download_url="https://datahub.io/core/geo-countries/r/countries.geojson")
    cmd = source.get_download_cmd("aws_access_key_id", "aws_secret_access_key", "./test_tmp")
    assert cmd == "wget https://datahub.io/core/geo-countries/r/countries.geojson -P ./test_tmp -q"
