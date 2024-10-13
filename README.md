[![Build Status](https://dev.azure.com/42nick/Test/_apis/build/status%2F42nick.gpu_usage_plotter?branchName=master)](https://dev.azure.com/42nick/Test/_build/latest?definitionId=1&branchName=master)

# gpu_usage_plotter
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
Start the app by running: 
```bash     
python src/gpu_usage_plotter/main.py

# or without the dash app
python src/gpu_usage_plotter/main.py --no-dash
```


## Building the docs
```
sphinx-build -b html docs/source docs/build
```

[Documentation](./docs/source/index.rst)

