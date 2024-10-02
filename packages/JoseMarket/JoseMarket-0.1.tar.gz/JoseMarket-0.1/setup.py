# setup.py

from setuptools import setup, find_packages

setup(
    name='JoseMarket',
    version='0.1',
    packages=find_packages(),
    description='A simple market module',
    author='Jose Eduardo',
    author_email='josedumoura@gmail.com',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
