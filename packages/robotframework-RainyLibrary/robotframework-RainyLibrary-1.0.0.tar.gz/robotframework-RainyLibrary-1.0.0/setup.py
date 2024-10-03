import re
import os
from distutils.command.register import register as register_orig
from distutils.command.upload import upload as upload_orig
from setuptools import setup,find_packages

# Read version from file without loading the module
with open('src/RainyLibrary/version.py', 'r') as version_file:
    version_match = re.search(r"^VERSION ?= ?['\"]([^'\"]*)['\"]", version_file.read(), re.M)
if version_match:
    VERSION=version_match.group(1)
else:
    VERSION='0.1'

requirements = [
    'robotframework==5.0',
    'robotframework-browsermobproxylibrary==0.1.3',
    'robotframework-browser==12.2.0',
    'robotframework-debuglibrary==2.2.2',
    'robotframework-databaselibrary==1.2.4',
    'robotframework-datadriver==1.6.0',
    'robotframework-datetime-tz==1.0.6',
    'robotframework-faker==5.0.0',
    'robotframework-seleniumlibrary==5.1.3',
    'robotframework-seleniumtestability==1.1.0',
    'robotframework-pdf2textlibrary==1.0.1',
    'robotframework-pabot==2.5.3',
    'robotframework-requests==0.9.4',
    'robotframework-sshlibrary==3.8.0',
    'robotframework-robocop==2.0.2',
    'robotframework-jsonlibrary==0.3.1',
    'robotframework-imaplibrary2==0.4.0',
    'robotframework-excellib==2.0.1',
    'robotframework-appiumlibrary==1.6.3',
    'robotframework-csvlibrary==0.0.5',
    'RESTinstance==1.3.0',
    'jsonpath2==0.4.4',
    'pyzxing==1.0.2',
    'PyMySQL==1.0.2',
    'PyYAML==5.3.1',
    'DateTime==4.3',
    'openpyxl==3.0.9',
    'certifi==2022.9.24',
    'cx-Oracle==8.3.0',
    'opencv-python==4.5.5.62'
]

test_requirements = [
    # TODO: put package test requirements here
]


CLASSIFIERS = """
Programming Language :: Python
Programming Language :: Python :: 2
Programming Language :: Python :: 3
License :: OSI Approved :: MIT License
Operating System :: OS Independent
Framework :: Robot Framework
Framework :: Robot Framework :: Library
"""[1:-1]


with open("README.md", "r") as fh:
    long_description = fh.read()


setup(
    name='robotframework-RainyLibrary',
    version=VERSION,
    description="rainy common library for robot framework",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="watchagorn pattummee",
    author_email='wpchagorn24@gmail.com',
    url='https://gitlab.com/wpchagorn24/robotframework-rainylibrary',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    include_package_data=True,
    install_requires=requirements,
    zip_safe=False,
    keywords='RainyWebCommon, RainyCommon, RainyAppCommon,RainyLibrary',
    classifiers=CLASSIFIERS.splitlines(),
    test_suite='tests',
    tests_require=test_requirements
)