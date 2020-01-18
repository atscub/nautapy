from setuptools import setup, find_packages
from os import path
from io import open


def get_about():
    scope = {}
    with open("nautapy/__about__.py") as fp:
        exec(fp.read(), scope)
    return scope


def get_requirements(env="base.txt"):
    with open("requirements/{}".format(env)) as fd:
        requirements = []
        for line in fd.readlines():
            if line.startswith("-r"):
                _, _env = line.split(" ", 2)
                requirements += get_requirements(_env.strip())
            else:
                requirements.append(line.strip())
        return requirements


def get_readme():
    """
        Get the long description from the README file
        :return:
        """
    with open(path.join(here, "README.md"), encoding="utf-8") as f:
        return f.read()


here = path.abspath(path.dirname(__file__))
about = get_about()

setup(
    name=about["__name__"],
    version=about["__version__"],
    description=about["__description__"],
    long_description=get_readme(),
    long_description_content_type="text/markdown",
    url=about["__url__"],
    author=about["__author__"],
    author_email=about["__email__"],
    classifiers=[
        "Topic :: Internet",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python"
    ],
    keywords="nauta portal cautivo",
    packages=find_packages(),
    install_requires=get_requirements(),
    entry_points={
        "console_scripts": [about["__cli__"] + "=nautapy.cli:main"],
    }
)
