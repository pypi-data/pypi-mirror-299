# OpenBambuCommands
![GitHub License](https://img.shields.io/pypi/l/openbambucommands)
![PyPI - Version](https://img.shields.io/pypi/v/openbambucommands)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

OpenBambuCommands is a Python package that provides helper functions to return
the strings for BambuLabs printers in an easy, hassle-free way. No more
fighting with string formatting!

This builds off of the work documented in [OpenBambuAPI](https://github.com/Doridian/OpenBambuAPI)

## Installation

You can install OpenBambuCommands using pip:

```
pip install openbambucommands
```

## Usage

Here's a quick example of how to use OpenBambuCommands:

```python3
from openbambucommands.mqtt import ledctrl

# get the command to turn the light on
command = ledctrl.set_light(True)
```

## Development
To set up the development environment:

1. Clone the repository
2. Create and activate a virtual environment
3. Install the package with development dependencies:
```
pip install -e .[dev]
```
4. Install `pre-commit`:
```
pre-commit install
```
5. Run tests:
```
# run with unittest
python -m unittest

# run with pytest
pytest
```

## Contributing
Contributions are welcome, feel free to open Issues or PRs
