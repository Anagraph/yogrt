import os

from yogrt.yogrt import get_template_folder, write_template, yogrt_init, yogrt_run


def test_get_template_folder():
    p = get_template_folder()
    assert "/".join(p.split("/")[-2:]) == "yogrt/templates"


def test_write_template():
    write_template("../yogrt/templates/profile_template.yaml", "./test_profile.yaml")
    assert os.path.exists("test_profile.yaml")
    os.remove("test_profile.yaml")


def test_yogrt_init():
    yogrt_init()
    assert os.path.exists("profile.yaml")
    assert os.path.exists("sources.yaml")
    assert os.path.exists("secrets.yaml")
    os.remove("profile.yaml")
    os.remove("sources.yaml")
    os.remove("secrets.yaml")


def test_yogrt_run():
    yogrt_run("templates/profile_template.yaml", "templates/sources_template.yaml",
              "templates/secrets_template.yaml")


def test_yogrt_run():
    yogrt_run("templates/profile_template.yaml", "templates/aws_sources_template.yaml",
              "/home/zacharydeziel/Documents/yogrt/yogrt/templates/test_secrets.yaml")


def test_yogrt_run_no_aws():
    yogrt_run("templates/profile_template.yaml", "templates/sources_template.yaml",
              "templates/no_aws_secrets_template.yaml")
