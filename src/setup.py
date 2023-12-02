from setuptools import find_packages, setup

setup(name="pretix_api",
      version="1.0",
      packages=find_packages(),
      install_requires=["openpyxl", "requests", "python-decouple"]
      )
