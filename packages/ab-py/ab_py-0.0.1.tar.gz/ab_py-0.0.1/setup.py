import os.path
import pathlib
from os.path import exists
from setuptools import setup, find_packages

CURRENT_DIR = pathlib.Path(__file__).parent
long_description = ""
readme_md_file = os.path.join(CURRENT_DIR, "README.md")
if exists(readme_md_file):
    long_description = pathlib.Path(readme_md_file).read_text()

def get_dependencies():
    return ["requests==2.31.0", "setuptools", "peewee", "mysql-connector-python"]

setup(
    name='ab_py',
    version='0.0.1',
    description='This is the sdk support for account',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Kawsar Ahmad',
    author_email='nmkwsr@gmail.com',
    url='https://github.com/exsited/exsited-python',
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=get_dependencies(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',

    ],
)
