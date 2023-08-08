from typing import Any


def validate_key(data: list, value_type: str, key: str, sub_key: str) -> Any:
    """В принимаемом словаре data проверяется наличие значений по ключу key."""
    value: Any = None

    if data[key] is not None and data[key][sub_key] is not None:
        value = data[key][sub_key]
    else:
        match value_type:
            case 'int':
                value = 0
            case 'float':
                value = 0.0
            case 'str':
                value = ''
            case 'bool':
                value = False
            case 'list':
                value = []
            case 'dict':
                value = {}
            case 'tuple':
                value = ()
    return value
