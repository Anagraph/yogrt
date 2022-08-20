import yaml

from source import Source


def yogrt_init(profile_path="./profile.yaml", sources_path="./sources.yaml",
               profile_template="templates/profile_template.yaml",
               sources_template="templates/sources_template.yaml"):
    with open(profile_template, "r") as f:
        profile_template = f.read()
        with open(profile_path, "w+") as profile_file:
            profile_file.write(profile_template)

    with open(sources_template, "r") as f:
        sources_template = f.read()
        with open(sources_path, "w+") as sources_file:
            sources_file.write(sources_template)

    return


def yogrt_run(profile_path, sources_path):
    profile_def = yaml.full_load(open(profile_path, "r"))
    sources_def = yaml.full_load(open(sources_path, "r"))
    sources = []
    for source in sources_def:
        if "unzip_filename" not in sources_def[source]:
            sources_def[source]["unzip_filename"] = None
        sources.append(Source(geometry_type=sources_def[source]['type'],
                              table_name=sources_def[source]['table_name'],
                              download_url=sources_def[source]['download_url'],
                              is_zip=sources_def[source]['is_zip'],
                              unzip_filename=sources_def[source]['unzip_filename']))

    for source in sources:
        source.download(destination_folder=profile_def['default']['destination_folder'])
        source.import_to_database(host=profile_def['default']['host'],
                                  port=profile_def['default']['port'],
                                  database=profile_def['default']['dbname'],
                                  user=profile_def['default']['user'],
                                  password=profile_def['default']['password'],
                                  schema=profile_def['default']['schema'])


def get_connection(profile):
    stream = open(profile)
    config = yaml.full_load(stream)

    print(config)
