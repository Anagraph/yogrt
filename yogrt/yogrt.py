import yaml
import os

from yogrt.source import get_source


def write_template(template_path, destination_path):
    with open(template_path, "r") as f:
        profile_template = f.read()
        with open(destination_path, "w+") as profile_file:
            profile_file.write(profile_template)

    return


def get_template_folder():
    return os.path.join(os.path.dirname(__file__), 'templates')


def yogrt_init(profile_path="./profile.yaml", sources_path="./sources.yaml", secrets_path="./secrets.yaml",
               profile_template=os.path.join(get_template_folder(), "profile_template.yaml"),
               sources_template=os.path.join(get_template_folder(), "sources_template.yaml"),
               secrets_template=os.path.join(get_template_folder(), "secrets_template.yaml")):
    write_template(profile_template, profile_path)
    write_template(sources_template, sources_path)
    write_template(secrets_template, secrets_path)

    return


def yogrt_run(profile_path, sources_path, secrets_path, force_download=False):
    profile_def = yaml.full_load(open(profile_path, "r"))
    sources_def = yaml.full_load(open(sources_path, "r"))
    secrets_def = yaml.full_load(open(secrets_path, "r"))

    sources = []
    for source in sources_def:
        if "is_zip" not in sources_def[source]:
            sources_def[source]["is_zip"] = False
        if "unzip_filename" not in sources_def[source]:
            sources_def[source]["unzip_filename"] = None

        sources.append(get_source(geometry_type=sources_def[source]['type'],
                                  table_name=sources_def[source]['table_name'],
                                  download_url=sources_def[source]['download_url'],
                                  is_zip=sources_def[source]['is_zip'],
                                  unzip_filename=sources_def[source]['unzip_filename']))

    for source in sources:
        # the only parameter that can be excluded from the profile.yaml is the aws s3 credentials
        # same decision should be made for other vendors
        if 's3_access_key_id' in secrets_def['default']:
            s3_access_key = secrets_def['default']['s3_access_key_id']
        else:
            s3_access_key = None
        if 's3_secret_access_key' in secrets_def['default']:
            s3_secret = secrets_def['default']['s3_secret_access_key']
        else:
            s3_secret = None

        source.download(destination_folder=profile_def['default']['destination_folder'], force_download=force_download,
                        aws_access_key_id=s3_access_key,
                        aws_secret_access_key=s3_secret)
        source.import_to_database(host=secrets_def['default']['host'],
                                  port=secrets_def['default']['port'],
                                  database=secrets_def['default']['dbname'],
                                  user=secrets_def['default']['user'],
                                  password=secrets_def['default']['password'],
                                  schema=secrets_def['default']['schema'],
                                  target_projection=profile_def['default']['target_projection'])

        return
