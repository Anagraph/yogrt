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


def yogrt_run(profile, sources):
    pass
