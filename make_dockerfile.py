import os
from os.path import join
from datetime import datetime

from jinja2 import Environment, FileSystemLoader

here = os.path.abspath(os.path.dirname(__file__))


def modification_date(filename):
    mtime = os.path.getmtime(filename)
    return datetime.fromtimestamp(mtime)


def make_file(template, filepath, **kwargs):
    if not os.path.exists(filepath):
        hastomake = True
    else:
        if modification_date(filepath) < modification_date(template):
            hastomake = True
        else:
            hastomake = False

    if hastomake:
        print(template, "->", filepath)
        env = Environment(loader=FileSystemLoader(here))
        template_j2 = env.get_template(template)
        with open(filepath, "w") as f:
            f.write(template_j2.render(**kwargs))


def clean():
    for filepath in files:
        if os.path.exists(filepath):
            os.remove(filepath)


if __name__ == "__main__":
    template = "template.Dockerfile"

    with open(join(here, "apt_requirements.txt")) as fp:
        apt_requirements = [pkg for pkg in fp.readlines() if pkg]

    files = {
        join(here, "Dockerfile"): dict(
            pip="pip3", image="python:3.7", apt_requirements=apt_requirements
        )
    }

    for filepath, kwargs in files.items():
        make_file(template, filepath, **kwargs)
