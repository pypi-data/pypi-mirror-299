from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='geoprocessing',
    version='3.1.5',
    description='Geoprocessing Library',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://ci.clearroadlab.io/clearroad/pygeoprocessing.git',
    author='Arman Davidyan',
    author_email='arman.davidyan@clearroad.io',
    license='unlicense',
    packages=['geoprocessing'],
    install_requires=[
        'requests==2.25.0',
        'urllib3==1.24.0',
        'python-dateutil==2.8.0',
        'numpy==2.1.1',
        'shapely==1.6.4.post2',
        'fiona==1.10.1'
    ],
    zip_safe=False
)
