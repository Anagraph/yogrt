from yogrt.yogrt import get_template_folder


def test_get_template_folder():
    p = get_template_folder()
    assert "/".join(p.split("/")[-2:]) == "yogrt/templates"
