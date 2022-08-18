import os.path
import shutil

from src.source import Source


def test_source_download_zip():
    source = Source(geometry_type="polygon", table_name="ldc",
                    download_url="https://www.oeb.ca/documents/opendata/open-data-electricity-map-20220131.zip",
                    is_zip=True)
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
