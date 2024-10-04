from setuptools import setup, find_packages

setup(
    name='netdis',
    version='0.6',
    packages=find_packages(),
    install_requires=[],
    package_data={'netdis': ['*.txt', '*.html', '*.zip', '*.rb']},
)
