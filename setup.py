from setuptools import setup, find_packages

setup(
    name="msgram",
    long_description="CLI da ferramenta MeasureSoftGram",
    version="0.1.0",
    extras_require={"dev": ["pytest", "pytest-cov", "setuptools", "wheel"]},
    packages=find_packages(),
    install_requires=[
        "requests==2.28.1",
        "pytz",
        "typing~=3.7.4.3",
        "tabulate==0.8.10",
        "termcolor==1.1.0",
        "pandas~=1.4.4",
        "setuptools~=60.2.0",
        "python-dotenv",
        "rich",
        "msgram-core==0.1.0",
        "validators==0.20.0",
    ],
    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # pip to create the appropriate form of executable for the target platform.
    entry_points={"console_scripts": ["msgram=src.cli.cliRunner:main"]},
)
