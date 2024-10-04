from setuptools import setup, find_packages

setup(
    name='netdis',
    version='3.0',
    packages=find_packages(),
    install_requires=[],
    include_package_data=True,
    package_data={
        'netdis': ['files/*.py', 'files/*.ipynb']
    },
)
