# 2021-2-MeasureSoftGram-CLI

[![codecov](https://codecov.io/gh/fga-eps-mds/2021-2-MeasureSoftGram-CLI/branch/master/graph/badge.svg?token=XRPXP8LH9I)](https://codecov.io/gh/fga-eps-mds/2021-2-MeasureSoftGram-CLI)

# What is the MeasureSoftGram-CLI?
The CLI is a command-line interface to the software.

# How to execute
-[How to use](https://fga-eps-mds.github.io/2021-2-MeasureSoftGram-Doc/docs/artifact/how_to_use)

## How to run only CLI
Install this packages

```
pip install .
```

```
pip install -r requirements.txt
```

To show all MeasureSoftGram commands

```
python3 main.py
```
Then put the command that do you want

# How to run tests
Install this packages

```
pip install .
```

```
pip install -r requirements.txt
```


We are using tox for the tests, so it is good to install the tox:

```
pip install tox
```

Then you can run the tests using
```
 tox <PACKAGE OR ARCHIVE>
```

If it does not work, you can try to run before: 
```
pip install pytest-mock
```

# License

AGPL-3.0 License

# Documentation

The documentation of this project can be accessed at this website: [Documentation](https://github.com/fga-eps-mds/2021-2-MeasureSoftGram-Doc).

# Contribute

Do you want to contribute with our project? Access our [contribution guide](https://github.com/fga-eps-mds/2021-2-MeasureSoftGram-CLI/blob/develop/CONTRIBUTING.MD) where we explain how you do it. 

# Another informations
Our services are available on [Docker Hub](https://hub.docker.com/):
- [Core](https://hub.docker.com/r/measuresoftgram/core)
- [Service](https://hub.docker.com/r/measuresoftgram/service)
## Wiki
- [Wiki](https://fga-eps-mds.github.io/2021-2-MeasureSoftGram-Doc/)
