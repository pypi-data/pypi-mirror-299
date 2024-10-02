"""
A high-level API for interacting with the `orjson` library to provide more user-friendly functions for
loading and dumping JSON data.

This module includes utilities to serialize and deserialize Python objects to and from JSON, with support
for custom serialization of non-JSON-compatible types using a `default` encoder function. It also includes
optional support for various `orjson` options to customize the serialization and deserialization process.

Functions:
    - loads: Deserialize JSON data from a string or bytes.
    - load: Deserialize JSON data from a file.
    - dumps: Serialize a Python object to a JSON string.
    - dump: Serialize a Python object and write it to a file.
"""

from jsonio.main import (
    load as load,
    dump as dump,
    dumps as dumps,
    loads as loads,
)
