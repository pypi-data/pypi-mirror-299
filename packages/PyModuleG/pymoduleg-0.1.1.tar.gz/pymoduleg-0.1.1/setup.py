from setuptools import setup, find_packages
import pathlib

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# Read the README file
README = (HERE / "README.md").read_text(encoding='utf-8')

setup(
    name='PyModuleG',
    version='0.1.1',
    author='Amit Kumar Jha',
    author_email='jha.8@iitj.ac.in',
    description='Automatically generate Python modules from a script based on specified imports and function names.',
    long_description=README,
    long_description_content_type='text/markdown',  # Specifies that README is in Markdown
    url='https://github.com/AIM-IT4/PyModule',
    packages=find_packages(),
    install_requires=[
        'astunparse',
    ],
    entry_points={
        'console_scripts': [
            'automodule=pymodule:main',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
