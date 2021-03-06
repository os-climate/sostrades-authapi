'''
Copyright 2022 Airbus SAS

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
'''
# coding: utf-8

from setuptools import setup, find_packages
from datetime import date
import os


def __path(filename):
    ''''Build a full absolute path using the given filename

        :params filename : filename to ass to the path of this module
        :returns: full builded path
    '''
    return os.path.join(os.path.dirname(__file__), filename)


with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()


# Manage module version using date
today = date.today()

# formating the date as yy.mm.dd
version = today.strftime('%y.%m.%d')

# check if the version.info file is existing (add a suffix to the version
# in case of multiple release in a day)
# it is intended that the version.info file contain only one line with the
# suffix information

suffix = ''
if os.path.exists(__path('version.info')):
    suffix = open(__path('version.info')).read().strip()

if len(suffix) > 0:
    version = f'{version}.{suffix}'

setup(
    name='sostrades_authapi',
    version=version,
    description='Repository of SoS Trades authentication api',
    long_description=readme,
    author='Airbus SAS',
    url='https://idas661.eu.airbus.corp/sostrades/sostrades_authapi.git',
    license=license,
    packages=find_packages(exclude=('tests', 'docs')),
    include_package_data=True,
    python_requires='==3.7',
    install_requires=[
        'python-dotenv==0.12.0',
        'Flask==1.1.1',
        'Flask-Cors==3.0.8',
        'itsdangerous==1.1.0',
        'passlib==1.7.2',
        'requests-toolbelt==0.9.1',
        'python3-saml==1.9.0'
    ]
)
