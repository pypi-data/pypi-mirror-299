from setuptools import setup, find_packages

from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='SimpleDSL',
    version='1.0.1',
    description='A domain-specific language for simple understanding',
    author='Joel Douglass Licklider',
    author_email='joellicklider@gmail.com',
    url='https://github.com/joellicklider878/SimpleDSL',
    packages=find_packages(),
    install_requires=[
        'antlr4-python3-runtime==4.9.2',
    ],
    entry_points={
        'console_scripts': [
            'simpledsl=yourpackage.main:main',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.9'
 )