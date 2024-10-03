# OpenBambuCommands
![GitHub License](https://img.shields.io/pypi/l/openbambucommands)
![PyPI - Version](https://img.shields.io/pypi/v/openbambucommands)

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

Here's a quick example of how to use StringHelper:

```python3
from openbambucommands import ftp, mqtt

print(ftp.hello_world())
print(mqtt.hello_world())
```

## Contributing
Contributions are welcome, feel free to open Issues or PRs
