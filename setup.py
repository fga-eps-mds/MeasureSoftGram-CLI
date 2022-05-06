from setuptools import setup, find_packages

setup(
    name="measuresoftgram",
    version="2.1.1",
    extras_require={"dev": ["pytest", "pytest-cov", "setuptools", "wheel"]},
    packages=find_packages(),
    install_requires=["inquirer==2.8.0", "requests", "pytz"],
    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # pip to create the appropriate form of executable for the target platform.
    entry_points={"console_scripts": ["measuresoftgram=src.cli.cliRunner:main"]},
)
