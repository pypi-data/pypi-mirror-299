import os
import subprocess
import sys
from setuptools import setup, find_packages
from setuptools.command.install import install
from setuptools.command.develop import develop
from setuptools.command.egg_info import egg_info

def download_models():
    from stepcutis.download_models import download
    download()

class PostInstallCommand(install):
    def run(self):
        install.run(self)
        self.execute(download_models, (), msg="Downloading model files...")

class PostDevelopCommand(develop):
    def run(self):
        develop.run(self)
        self.execute(download_models, (), msg="Downloading model files...")

class PostEggInfoCommand(egg_info):
    def run(self):
        egg_info.run(self)
        self.execute(download_models, (), msg="Downloading model files...")

# Read requirements from requirements.txt
try:
    with open('requirements.txt') as f:
        requirements = f.read().splitlines()
except FileNotFoundError:
    print("Warning: requirements.txt not found. Proceeding without explicit requirements.")
    requirements = []

# Try to read long description from README.md, use a default if not found
try:
    with open('README.md', 'r', encoding='utf-8') as f:
        long_description = f.read()
except FileNotFoundError:
    long_description = "stepcutis - A document analysis program"

setup(
    name='stepcutis',
    version='0.1.0',
    author='Your Name',
    author_email='eaucoi9@lsu.edu',
    description='A document analysis program',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/2OsZI4ISYd/stepcutis',
    packages=find_packages(),
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'stepcutis=stepcutis.start:main',
        ],
    },
    cmdclass={
        'install': PostInstallCommand,
        'develop': PostDevelopCommand,
        'egg_info': PostEggInfoCommand,
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.10',
    ],
    python_requires='>=3.10',
    include_package_data=True,
)