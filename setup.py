import os
from setuptools import setup, find_packages

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

setup(
    name='python-cuckoo',
    description="Cuckoo Filter implemenation for Python 3.x",
    keywordds='cuckoofilter bloomfilter',
    version="1.0.0",
    license='MIT',
    packages=find_packages(),
    install_requires=[
        'mmh3',
    ],
    tests_require=[
        'pytest',
    ],
    author='Maxime Beauchemin',
    author_email='maximebeauchemin@gmail.com',
    maintainer='Leechael Yim',
    maintainer_email='yanleech@gmail.com',
    url='https://github.com/Leechael/python-cuckoo',
    download_url='https://github.com/Leechael/python-cuckoo/tarball/1.0.0',
    classifiers=[
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)
