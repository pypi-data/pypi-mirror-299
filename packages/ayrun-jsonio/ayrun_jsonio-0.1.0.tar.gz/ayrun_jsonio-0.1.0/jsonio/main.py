from typing import Optional, Any, Union, Callable, TypeAlias
from pathlib import Path

import orjson

DefaultEncoder: TypeAlias = Callable[[Any], Any]


def loads(data: Union[str, bytes]) -> Any:
    """
    Deserialize JSON data from a string or bytes.


    Args:
        data: The JSON string or bytes to deserialize.

    Returns:
        The deserialized Python object.

    Raises:
        orjson.JSONDecodeError: If the input is not valid JSON.
    """
    return orjson.loads(data)


def load(filepath: Union[str, Path]) -> Any:
    """
    Deserialize JSON data from a file.

    Args:
        filepath: the file path to the JSON file.

    Returns:
        The deserialized Python object.

    Raises:
        FileNotFoundError: If the file does not exist.
        orjson.JSONDecodeError: If the file contents are not valid JSON.
    """
    with open(filepath, "rb") as file:
        return orjson.loads(file.read())


def dumps(
    obj: Any, *, option: Optional[int] = None, default: Optional[DefaultEncoder] = None
) -> str:
    """
    Serialize a Python object to a JSON string.

    Args:
        obj: The Python object to serialize.
        option: Optional `orjson` option flags to customize serialization.
            Defaults to None.
        default: A custom callable to handle non-serializable objects.
            Defaults to None.

    Returns:
        str: The serialized JSON string.

    Raises:
        orjson.JSONDecodeError: If the object cannot be serialized and no valid `default` function is provided.
    """
    return orjson.dumps(obj, option=option, default=default).decode("utf-8")


def dump(
    obj: Any,
    filepath: Union[str, Path],
    *,
    option: Optional[int] = None,
    default: Optional[DefaultEncoder] = None,
) -> None:
    """
    Serialize a Python object and write it to a file.

    Args:
        obj: The Python object to serialize.
        filepath: The file path where the JSON will be written.
        option: Optional `orjson` option flags to customize serialization.
            Defaults to None.
        default: A custom callable to handle non-serializable objects.
            Defaults to None.

    Returns:
        None

    Raises:
        orjson.JSONEncodeError: If the object cannot be serialized and no valid `default` function is provided.
        FileNotFoundError: If the file path is invalid or cannot be written to.
    """
    json_bytes = orjson.dumps(obj, option=option, default=default)
    with open(filepath, "wb") as file:
        file.write(json_bytes)
