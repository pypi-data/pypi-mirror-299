# my_package/setup.py
from setuptools import setup, find_packages

setup(
    name='pyutiltool',
    version='3.5',
    packages=find_packages(),
    description='Simple Python Utils Package',
    author='Alan Paul',
    author_email='testy9128@protonmail.com',
    install_requires=[
        'requests',  
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
