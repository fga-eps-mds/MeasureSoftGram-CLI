# 2022-2-MeasureSoftGram-CLI

## Badges

[![Code Smells](https://sonarcloud.io/api/project_badges/measure?project=fga-eps-mds_2022-2-MeasureSoftGram-CLI&metric=code_smells)](https://sonarcloud.io/summary/new_code?id=fga-eps-mds_2022-2-MeasureSoftGram-CLI)
[![Maintainability Rating](https://sonarcloud.io/api/project_badges/measure?project=fga-eps-mds_2022-2-MeasureSoftGram-CLI&metric=sqale_rating)](https://sonarcloud.io/summary/new_code?id=fga-eps-mds_2022-2-MeasureSoftGram-CLI)
[![Security Rating](https://sonarcloud.io/api/project_badges/measure?project=fga-eps-mds_2022-2-MeasureSoftGram-CLI&metric=security_rating)](https://sonarcloud.io/summary/new_code?id=fga-eps-mds_2022-2-MeasureSoftGram-CLI)
[![Bugs](https://sonarcloud.io/api/project_badges/measure?project=fga-eps-mds_2022-2-MeasureSoftGram-CLI&metric=bugs)](https://sonarcloud.io/summary/new_code?id=fga-eps-mds_2022-2-MeasureSoftGram-CLI)
[![Vulnerabilities](https://sonarcloud.io/api/project_badges/measure?project=fga-eps-mds_2022-2-MeasureSoftGram-CLI&metric=vulnerabilities)](https://sonarcloud.io/summary/new_code?id=fga-eps-mds_2022-2-MeasureSoftGram-CLI)
[![Duplicated Lines (%)](https://sonarcloud.io/api/project_badges/measure?project=fga-eps-mds_2022-2-MeasureSoftGram-CLI&metric=duplicated_lines_density)](https://sonarcloud.io/summary/new_code?id=fga-eps-mds_2022-2-MeasureSoftGram-CLI)
[![Reliability Rating](https://sonarcloud.io/api/project_badges/measure?project=fga-eps-mds_2022-2-MeasureSoftGram-CLI&metric=reliability_rating)](https://sonarcloud.io/summary/new_code?id=fga-eps-mds_2022-2-MeasureSoftGram-CLI)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=fga-eps-mds_2022-2-MeasureSoftGram-CLI&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=fga-eps-mds_2022-2-MeasureSoftGram-CLI)
[![Technical Debt](https://sonarcloud.io/api/project_badges/measure?project=fga-eps-mds_2022-2-MeasureSoftGram-CLI&metric=sqale_index)](https://sonarcloud.io/summary/new_code?id=fga-eps-mds_2022-2-MeasureSoftGram-CLI)
[![Coverage](https://sonarcloud.io/api/project_badges/measure?project=fga-eps-mds_2022-2-MeasureSoftGram-CLI&metric=coverage)](https://sonarcloud.io/summary/new_code?id=fga-eps-mds_2022-2-MeasureSoftGram-CLI)
[![Lines of Code](https://sonarcloud.io/api/project_badges/measure?project=fga-eps-mds_2022-2-MeasureSoftGram-CLI&metric=ncloc)](https://sonarcloud.io/summary/new_code?id=fga-eps-mds_2022-2-MeasureSoftGram-CLI)
[![Downloads](https://pepy.tech/badge/msgram)](https://pepy.tech/project/msgram)
[![Downloads](https://pepy.tech/badge/msgram/month)](https://pepy.tech/project/msgram)
[![Downloads](https://pepy.tech/badge/msgram/week)](https://pepy.tech/project/msgram)

[![PyPI](https://img.shields.io/pypi/v/msgram.svg)](https://pypi.python.org/pypi/msgram/)

## What is the MeasureSoftGram-CLI?
The CLI is a command-line interface to the software.

## How to use CLI
-[How to use](https://fga-eps-mds.github.io/2021-2-MeasureSoftGram-Doc/docs/artifact/how_to_use)

### How to run only CLI
Install this packages

```
pip install .
```

```
pip install -r requirements.txt
```

To show all MeasureSoftGram commands
If do you want to see all commands use:

```
pip install .
```
then use this command to see the commands:
```
msgram -h
```
or if you don´t want to run the pip install . , use:
```
python3 main.py
```
Then put the command that do you want

## How to run tests
Install this dependencies

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
 tox 
```

if you want to especify the file use:
```
 tox <PACKAGE OR FILE>
```

If it does not work, you can try to run before: 
```
pip install pytest-mock
```

## License

AGPL-3.0 License

## Documentation

The documentation of this project can be accessed at this website: [Documentation](https://github.com/fga-eps-mds/2022-2-MeasureSoftGram-Doc).

## Contribute

Do you want to contribute with our project? Access our [contribution guide](https://github.com/fga-eps-mds/2022-2-MeasureSoftGram-Doc/blob/main/docs/politicas/contribuindo.md) where we explain how you do it. 

## Another informations
Our services are available on [Docker Hub](https://hub.docker.com/):
- [Core](https://hub.docker.com/r/measuresoftgram/core)
- [Service](https://hub.docker.com/r/measuresoftgram/service)

### Wiki
For more informations, you can see our wiki:
- [Wiki](https://fga-eps-mds.github.io/2022-2-MeasureSoftGram-Doc/)
