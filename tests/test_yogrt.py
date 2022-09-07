import os

from yogrt.yogrt import get_template_folder, write_template


def test_get_template_folder():
    p = get_template_folder()
    assert "/".join(p.split("/")[-2:]) == "yogrt/templates"


def test_write_template():
    write_template("../yogrt/templates/profile_template.yaml", "./test_profile.yaml")
    assert os.path.exists("test_profile.yaml")
    os.remove("test_profile.yaml")
