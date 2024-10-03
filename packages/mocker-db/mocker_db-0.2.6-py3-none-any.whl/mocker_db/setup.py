from setuptools import setup

import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))
path_to_readme = os.path.join(here, "README.md")

long_description = """# Mocker db

MockerDB is a python module that contains mock vector database like solution built around
python dictionary data type. It contains methods necessary to interact with this 'database',
embed, search and persist.

"""

if os.path.exists(path_to_readme):
  with codecs.open(path_to_readme, encoding="utf-8") as fh:
      long_description += fh.read()

setup(
    name="mocker_db",
    packages=["mocker_db"],
    install_requires=['httpx', 'gridlooper>=0.0.1', 'pydantic', 'pyyaml', 'pympler==1.0.1', 'psutil', 'requests', 'click==8.1.7', 'numpy==1.26.0', 'dill==0.3.7', 'attrs>=22.2.0', 'fastapi'],
    classifiers=['Development Status :: 3 - Alpha', 'Intended Audience :: Developers', 'Intended Audience :: Science/Research', 'Programming Language :: Python :: 3', 'Programming Language :: Python :: 3.9', 'Programming Language :: Python :: 3.10', 'Programming Language :: Python :: 3.11', 'License :: OSI Approved :: MIT License', 'Topic :: Scientific/Engineering'],
    long_description=long_description,
    long_description_content_type='text/markdown',
    author="Kyrylo Mordan",
    author_email="parachute.repo@gmail.com",
    description="A mock handler for simulating a vector database.",
    license="mit",
    keywords="['aa-paa-tool']",
    version="0.2.6",
    entry_points = {'console_scripts': ['mockerdb = mocker_db.cli:cli']},

    extras_require = {'hnswlib': ['hnswlib==0.8.0'], 'sentence-transformers': ['sentence-transformers==2.2.2'], 'torch': ['torch'], 'all': ['hnswlib==0.8.0', 'sentence-transformers==2.2.2', 'torch']},
    include_package_data = True,
    package_data = {'mocker_db': ['mkdocs/**/*', '.paa.tracking/version_logs.csv', '.paa.tracking/release_notes.md', '.paa.tracking/lsts_package_versions.yml', '.paa.tracking/notebook.ipynb', '.paa.tracking/package_mapping.json', '.paa.tracking/package_licenses.json', '.paa.tracking/.paa.config', '.paa.tracking/.paa.version']} ,
    )
