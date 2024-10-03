from setuptools import setup, find_packages

setup(
    name='PyModuleG',
    version='0.1.0',
    author='Amit Kumar Jha',
    author_email='jha.8@iitj.ac.in',
    description='Automatically generate Python modules from a script based on specified imports and function names.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/AIM-IT4/PyModule',
    packages=find_packages(),
    install_requires=[
        'astunparse',
    ],
    entry_points={
        'console_scripts': [
            'automodule=autogenerator:main',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
