from setuptools import setup, find_packages

setup(
    name="lot-tracker",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "click",
        "requests",
        "beautifulsoup4",
        "selenium",
        "webdriver-manager",
        "pytz"
    ],
    entry_points={
        "console_scripts": [
            "lot-tracker=src.cli:cli",
        ],
    },
) 