
# Package python for Lagoon

![lagoon-python-api](https://github.com/fatfish-lab/lagoon-python-api/blob/main/docs/source/_static/logo.png?raw=true)

> Lagoon python API is a tool that allows [Lagoon](https://fatfi.sh/lagoon) users to interact with there data from directly from Python.

Lagoon is developed by [Fatfish Lab](https://fatfi.sh)

```python
# -*- coding: utf-8 -*-
from lagoon import Lagoon

lg = Lagoon('https://your-lagoon-server')
lg.connect(LG_USER, LG_PASSWORD)

organisations = lg.get_organisations()
hardware = organisations[0].get_hardware()
```

## Installation
This package is compatible with Python 2.7 and 3.7+

```python
python -m pip install lagoon-python-api
```
OR
```python
python -m pip install git+https://github.com/fatfish-lab/lagoon-python-api.git
```

## Documentation

Check our [documentation](https://docs.python.lagoon.fatfishlab.app) to find all the information you need.

## Maintainer

The repository is maintained by [Fatfish Lab](https://fatfi.sh)

## Support

You can contact our team at [support@fatfi.sh](mailto:support@fatfi.sh).

## Development

> Rather the package is compatible with python 2.7 and 3, the Sphinx documentation is using python 3.

1. Clone this repository
1. Setup a virtual env : `virtualenv pylg`
   1. If needed, you can specify the version of python used in your virtual env : `virtualenv --python=/usr/bin/python3 pylg3`
1. Enable your virtual env : `source pylg/bin/activate`
1. Install local Lagoon package to your virtual env : `pip install -e /path/to/package/lagoon-python-api`

### Build the documation

1. `cd /path/to/package/lagoon-python-api/docs`
2. `make html`

## Licence

This project uses the following license: GPL-3.0-only.
See the license file to read it.

