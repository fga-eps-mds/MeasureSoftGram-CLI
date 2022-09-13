from setuptools import setup, find_packages

setup(
    name="measuresoftgram",
    long_description="CLI da ferramenta MeasureSoftGram",
    version="3.1.4",
    extras_require={"dev": ["pytest", "pytest-cov", "setuptools", "wheel"]},
    packages=find_packages(),
    install_requires=[
        "inquirer==2.8.0",
        "requests==2.28.1",
        "pytz",
        "tabulate==0.8.10",
        "termcolor==1.1.0"
    ],
    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # pip to create the appropriate form of executable for the target platform.
    entry_points={"console_scripts": ["measuresoftgram=src.cli.cliRunner:main"]},
)
