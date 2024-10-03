# Python Geoprocessing Library

[![Pipeline Status](https://ci.clearroadlab.io/clearroad/pygeoprocessing/badges/master/pipeline.svg)](https://ci.clearroadlab.io/clearroad/pygeoprocessing/commits/master)
[![Coverage Report](https://ci.clearroadlab.io/clearroad/pygeoprocessing/badges/master/coverage.svg)](https://ci.clearroadlab.io/clearroad/pygeoprocessing/commits/master)

# Requirements

* python 3
* python3-dev (for linux)

# Install

```bash
pip install git+ssh://git@ci.clearroadlab.io/clearroad/pygeoprocessing.git
```
Or
```bash
pip install geoprocessing --extra-index-url https://<user>:<password>@registry.clearroadlab.io/simple/
```

## Run the tests

### Using local install

```bash
python -m unittest discover
```

### Using Docker

```bash
docker-compose -f docker-compose.test.yml up --build
```
