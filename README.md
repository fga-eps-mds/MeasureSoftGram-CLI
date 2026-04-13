# 2024-1 MeasureSoftGram-CLI
Command line project to MeasureSoftGram
## Badges

[![Code Smells](https://sonarcloud.io/api/project_badges/measure?project=fga-eps-mds_2023-1-MeasureSoftGram-CLI&metric=code_smells)](https://sonarcloud.io/summary/new_code?id=fga-eps-mds_2023-1-MeasureSoftGram-CLI)
[![Maintainability Rating](https://sonarcloud.io/api/project_badges/measure?project=fga-eps-mds_2023-1-MeasureSoftGram-CLI&metric=sqale_rating)](https://sonarcloud.io/summary/new_code?id=fga-eps-mds_2023-1-MeasureSoftGram-CLI)
[![Security Rating](https://sonarcloud.io/api/project_badges/measure?project=fga-eps-mds_2023-1-MeasureSoftGram-CLI&metric=security_rating)](https://sonarcloud.io/summary/new_code?id=fga-eps-mds_2023-1-MeasureSoftGram-CLI)
[![Bugs](https://sonarcloud.io/api/project_badges/measure?project=fga-eps-mds_2023-1-MeasureSoftGram-CLI&metric=bugs)](https://sonarcloud.io/summary/new_code?id=fga-eps-mds_2023-1-MeasureSoftGram-CLI)
[![Vulnerabilities](https://sonarcloud.io/api/project_badges/measure?project=fga-eps-mds_2023-1-MeasureSoftGram-CLI&metric=vulnerabilities)](https://sonarcloud.io/summary/new_code?id=fga-eps-mds_2023-1-MeasureSoftGram-CLI)
[![Duplicated Lines (%)](https://sonarcloud.io/api/project_badges/measure?project=fga-eps-mds_2023-1-MeasureSoftGram-CLI&metric=duplicated_lines_density)](https://sonarcloud.io/summary/new_code?id=fga-eps-mds_2023-1-MeasureSoftGram-CLI)
[![Reliability Rating](https://sonarcloud.io/api/project_badges/measure?project=fga-eps-mds_2023-1-MeasureSoftGram-CLI&metric=reliability_rating)](https://sonarcloud.io/summary/new_code?id=fga-eps-mds_2023-1-MeasureSoftGram-CLI)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=fga-eps-mds_2023-1-MeasureSoftGram-CLI&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=fga-eps-mds_2023-1-MeasureSoftGram-CLI)
[![Technical Debt](https://sonarcloud.io/api/project_badges/measure?project=fga-eps-mds_2023-1-MeasureSoftGram-CLI&metric=sqale_index)](https://sonarcloud.io/summary/new_code?id=fga-eps-mds_2023-1-MeasureSoftGram-CLI)
[![Coverage](https://sonarcloud.io/api/project_badges/measure?project=fga-eps-mds_2023-1-MeasureSoftGram-CLI&metric=coverage)](https://sonarcloud.io/summary/new_code?id=fga-eps-mds_2023-1-MeasureSoftGram-CLI)
[![Lines of Code](https://sonarcloud.io/api/project_badges/measure?project=fga-eps-mds_2023-1-MeasureSoftGram-CLI&metric=ncloc)](https://sonarcloud.io/summary/new_code?id=fga-eps-mds_2023-1-MeasureSoftGram-CLI)
[![Downloads](https://pepy.tech/badge/msgram)](https://pepy.tech/project/msgram)
[![Downloads](https://pepy.tech/badge/msgram/month)](https://pepy.tech/project/msgram)
[![Downloads](https://pepy.tech/badge/msgram/week)](https://pepy.tech/project/msgram)

[![PyPI](https://img.shields.io/pypi/v/msgram.svg)](https://pypi.python.org/pypi/msgram/)

## What is the MeasureSoftGram-CLI?
The CLI is a command-line interface to the software.

## How to use CLI
- [How to use](https://fga-eps-mds.github.io/2021-2-MeasureSoftGram-Doc/docs/artifact/how_to_use)

## How to run the project
Use Python 3.9 or higher. The CI currently uses Python 3.10.

First, clone the repository and enter the project folder:

```
git clone <repository-url>
cd <repository-folder>
```

It is recommended to create and activate a virtual environment:

```
python3 -m venv .venv
source .venv/bin/activate
```

Then install the project dependencies:

```
pip install -r requirements.txt
```

The `requirements.txt` file already installs the local application in editable mode through `-e .`. After that, the `msgram` command is available in the terminal.

To show all MeasureSoftGram commands, use:

```
msgram -h
```

If you do not want to use the installed `msgram` command, run the Python entry point directly:

```
python3 main.py -h
```

If a module is not found, check if the virtual environment is activated and run `pip install -r requirements.txt` again.

## Basic usage
Create the default configuration file:

```
msgram init
```

This creates the `.msgram/msgram.json` file in the current directory.

List the configuration:

```
msgram list
```

Extract metrics from SonarQube/SonarCloud JSON files:

```
msgram extract -sp analytics-raw-data -ep .msgram
```

The `-sp` argument is the path to the directory with the JSON files. The `-ep` argument is the path where the extracted `.metrics` files will be saved.

Calculate the model values from extracted metrics:

```
msgram calculate -ep .msgram -cp .msgram -o csv
```

The `-ep` argument is the path to the extracted metrics. The `-cp` argument is the path to the folder with `msgram.json`. The `-o` argument defines the output format.

To see the options of a specific command, use:

```
msgram <command> -h
```

## Common errors
If the project does not run, check these points first:

```
python --version
which python
which msgram
```

If the error is `ModuleNotFoundError: No module named 'dotenv'`, the dependencies were probably not installed in the current environment. Activate the virtual environment and install the requirements again:

```
source .venv/bin/activate
pip install -r requirements.txt
```

If the `msgram` command is not found, check if the virtual environment is activated. You can also run the project using the Python entry point:

```
python3 main.py -h
```

If you use `msgram init -cp <path>`, make sure the parent directory already exists. The simplest option is to run `msgram init` inside the project folder.

## How to run tests
Install the dependencies:

```
pip install -r requirements.txt
```

We are using tox for the tests, so it is good to install tox:

```
pip install tox
```

Then you can run the tests using:

```
tox
```

If you want to specify a test file, use pytest:

```
pip install pytest pytest-cov pytest-mock
pytest tests/unit/test_calculate.py
```

## License

AGPL-3.0 License

## Documentation

The documentation of this project can be accessed at this website: [Documentation](https://github.com/fga-eps-mds/2023-1-MeasureSoftGram-Doc).

## Contribute

Do you want to contribute with our project? Access our [contribution guide](https://github.com/fga-eps-mds/2022-2-MeasureSoftGram-Doc/blob/main/docs/politicas/contribuindo.md) where we explain how you do it.

## Another informations
Our services are available on [Docker Hub](https://hub.docker.com/):
- [Core](https://hub.docker.com/r/measuresoftgram/core)
- [Service](https://hub.docker.com/r/measuresoftgram/service)

### Wiki
For more informations, you can see our wiki:
- [Wiki](https://fga-eps-mds.github.io/2023-1-MeasureSoftGram-Doc/)

### Demais repositórios do produto
- [Core](https://github.com/fga-eps-mds/MeasureSoftGram-Core)
- [Service](https://github.com/fga-eps-mds/MeasureSoftGram-Service)
- [Front Web](https://github.com/fga-eps-mds/MeasureSoftGram-Front)
- [Action](https://github.com/fga-eps-mds/MeasureSoftGram-Action)
- [Parser](https://github.com/fga-eps-mds/MeasureSoftGram-Parser)
