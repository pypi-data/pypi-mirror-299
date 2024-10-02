from setuptools import setup, find_packages
setup(
name='rlpp',
version='0.1.0',
author='Uriel Garcilazo Cruz',
author_email='garcilazo.uriel@gmail.com',
description='A suite of tools to assist in the creation of reinforcement learning applications in games using pygame',
packages=find_packages(),
classifiers=[
'Programming Language :: Python :: 3',
'License :: OSI Approved :: MIT License',
'Operating System :: OS Independent',
],
python_requires='>=3.6',
)