import yaml

from source import Source


def write_template(template_path, destination_path):
    with open(template_path, "r") as f:
        profile_template = f.read()
        with open(destination_path, "w+") as profile_file:
            profile_file.write(profile_template)

    return


def yogrt_init(profile_path="./profile.yaml", sources_path="./sources.yaml", secrets_path="./secrets.yaml",
               profile_template="templates/profile_template.yaml",
               sources_template="templates/sources_template.yaml",
               secrets_template="templates/sources_template.yaml"):
    write_template(profile_template, profile_path)
    write_template(sources_template, sources_path)
    write_template(secrets_template, secrets_path)

    return


def yogrt_run(profile_path, sources_path, secrets_path):
    profile_def = yaml.full_load(open(profile_path, "r"))
    sources_def = yaml.full_load(open(sources_path, "r"))
    secrets_def = yaml.full_load(open(secrets_path, "r"))

    sources = []
    for source in sources_def:
        if "is_zip" not in sources_def[source]:
            sources_def[source]["is_zip"] = False
        if "unzip_filename" not in sources_def[source]:
            sources_def[source]["unzip_filename"] = None

        sources.append(Source(geometry_type=sources_def[source]['type'],
                              table_name=sources_def[source]['table_name'],
                              download_url=sources_def[source]['download_url'],
                              is_zip=sources_def[source]['is_zip'],
                              unzip_filename=sources_def[source]['unzip_filename']))

    for source in sources:
        print(source.type)
        source.download(destination_folder=profile_def['default']['destination_folder'])
        source.import_to_database(host=secrets_def['default']['host'],
                                  port=secrets_def['default']['port'],
                                  database=secrets_def['default']['dbname'],
                                  user=secrets_def['default']['user'],
                                  password=secrets_def['default']['password'],
                                  schema=secrets_def['default']['schema'],
                                  geom_type=source.type,
                                  target_projection=profile_def['default']['target_projection'])
