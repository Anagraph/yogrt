# YAML OGR Templating (yogrt) 🍦 
## A simple templating tool for importing GIS data to PostGIS 

## Requirements

- Python 3.6+
- [GDAL & OGR](https://gdal.org/)
- [awscli](https://aws.amazon.com/cli/) (optional)
- [poetry](https://python-poetry.org/) (optional)

## Installation

`poetry`:
```bash
poetry add git+ssh://git@github.com/Anagraph/yogrt.git@develop
poetry shell
```

## Example

### Initialize template files

```bash
export YOGRT_TARGET_DIR=./yogrt
mkdir -p $YOGRT_TARGET_DIR
yogrt init --target-directory $YOGRT_TARGET_DIR
```

You will now have the following files within the target directory:
```bash
.
├── profile.yaml
├── secrets.yaml
└── sources.yaml
```

You can modify the target projection of the sources by modifying the `profile.yaml` file.

You must modify the `secrets.yaml` to configure it with your database and optionally your AWS credentials.

The `sources.yaml` file is where you will configure the sources you want to import:
```yaml
countries:
  type: polygon
  download_url: https://datahub.io/core/geo-countries/r/countries.geojson
  table_name: countries

ldc:
  type: polygon
  download_url: https://www.oeb.ca/documents/opendata/open-data-electricity-map-20220131.zip
  table_name: ldc
  is_zip: true
  unzip_filename: "Electric_220131.kmz"
```

### Import datasources

Run with:
```bash
yogrt run --profile=$YOGRT_TARGET_DIR/profile.yaml --sources=$YOGRT_TARGET_DIR/sources.yaml  --secrets=$YOGRT_TARGET_DIR/secrets.yaml
```

## Contributing

## Install for dev

```bash
git clone git@github.com:Anagraph/yogrt.git
git switch -c feature/my-new-feature
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Run tests

```bash
cd tests
pytest .
```

## Additional notes

You can [setup a dev PostgreSQL server](docs/postgresql-docker.md)

