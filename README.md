# pretix_api

Usefull scripts for Pretix

# Local use

### Package

```console
pip install setuptools
pip install wheel
python setup.py bdist_wheel


pip install "path\to\project\pretix_api\dist\{distname}" --force-reinstall
```

### As Requirement in setup.py

```python
setup(name="App",
      version="1.0",
      packages=find_packages(),
      install_requires=[
                        "Pretix_API@git+ssh://git@github.com/nds-pfadfinden/pretix_api_package.git"
                        ]
      )
```

# Auth

user = Pretix(organ)
