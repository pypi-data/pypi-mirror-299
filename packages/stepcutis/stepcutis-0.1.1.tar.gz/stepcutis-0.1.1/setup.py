import os
import sys
from setuptools import setup, find_packages
from setuptools.command.install import install
import subprocess

class PostInstallCommand(install):
    def run(self):
        install.run(self)
        subprocess.check_call([sys.executable, '-m', 'stepcutis.download_models'])

# Read requirements from requirements.txt
with open('requirements.txt') as f:
    requirements = f.read().splitlines()

# Read long description from README.md
with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='stepcutis',
    version='0.1.1',  # Increment this as needed
    author='Emile Aucoin',
    author_email='eaucoi9@lsu.edu',
    description='A document analysis program',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/stepcutis',
    packages=find_packages(),
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'stepcutis=stepcutis.start:main',
        ],
    },
    cmdclass={
        'install': PostInstallCommand,
    },
    package_data={
        'stepcutis': [
            'GOT-OCR2_0/**/*',
            'projectpackages/surya/**/*',
            'projectpackages/CRAFT/**/*',
            'projectpackages/LakeOCR/**/*',
        ],
    },
    include_package_data=True,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.10',
    ],
    python_requires='>=3.10',
)