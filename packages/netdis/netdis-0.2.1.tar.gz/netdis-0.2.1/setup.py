from setuptools import setup, find_packages

setup(
    name='netdis',
    version='0.2.1',
    packages=find_packages(),
    install_requires=[],
    package_data={'netdis': ['*.py', '*.ipynb','*.zip']},
)
