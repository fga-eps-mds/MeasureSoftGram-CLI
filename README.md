# 2021-2-MeasureSoftGram-CLI

[![codecov](https://codecov.io/gh/fga-eps-mds/2021-2-MeasureSoftGram-CLI/branch/master/graph/badge.svg?token=XRPXP8LH9I)](https://codecov.io/gh/fga-eps-mds/2021-2-MeasureSoftGram-CLI)

# How to execute

Create a folder on the system for MeasureSoftGram, as it will be necessary to download some scripts to run it.
Download the scripts of start and stop:
```
curl https://raw.githubusercontent.com/fga-eps-mds/2021-2-MeasureSoftGram-Doc/main/installation/start.sh -o start.sh && curl https://raw.githubusercontent.com/fga-eps-mds/2021-2-MeasureSoftGram-Doc/main/installation/stop.sh -o stop.sh
```

# Contribute

Do you want to contribute with our project? Access our [contribution guide](https://github.com/fga-eps-mds/2021-2-MeasureSoftGram-CLI/blob/develop/CONTRIBUTING.MD) where we explain how you do it. 
# Scripts

## Start
 The start script takes 3 optional parameters:
 1. Core tag version (default latest)
 2. Service tag version (default latest)
 3. Service port (default 5000)

Example:

```
sh start.sh v1.0.4 v1.0.1 5000
```

## Stop

The stop script does not take any parameters
Example:

```
sh stop.sh
```
# CLI

The CLI is available on [PyPi](https://pypi.org/project/measuresoftgram/). To run the CLI it is necessary to install:

```
pip install measuresoftgram
```

To execute the program:

```
measuresoftgram
```

And with that a help menu will be displayed.

# License

AGPL-3.0 License

# Documentation

The documentation of this project can be accessed at this website: [Documentation](https://github.com/fga-eps-mds/2021-2-MeasureSoftGram-Doc).

# Another informations
Our services are available on [Docker Hub](https://hub.docker.com/):
- [Core](https://hub.docker.com/r/measuresoftgram/core)
- [Service](https://hub.docker.com/r/measuresoftgram/service)
