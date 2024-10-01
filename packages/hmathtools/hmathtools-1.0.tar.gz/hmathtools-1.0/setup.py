# setup.py
from setuptools import setup, find_packages

setup(
    name='hmathtools',
    version='1.0',
    packages=find_packages(),
    install_requires=['numpy'],
    author='Harman Singh',
    author_email='the.programming.hacker.hk+1@gmail.com',
    description='A simple package that uses NumPy .',
    long_description=open('README.md').read(),
    url='https://github.com/your_username/my_package',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
)