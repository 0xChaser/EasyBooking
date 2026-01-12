from inspect import isclass

from pydantic import BaseModel
from pydantic_core import SchemaSerializer, SchemaValidator


def optional(*fields):
    """Turn pydantic fields into optional"""

    def dec(_class: BaseModel):
        _core = _class.__pydantic_core_schema__

        _fields = {}

        if _core["schema"]["type"] == "model-fields":
            _fields = _core["schema"]["fields"]
        if _core["schema"]["type"] == "model":
            _fields = _core["schema"]["schema"]["fields"]

        for field in fields:
            if _class.model_fields[field].is_required():
                _fields[field]["schema"] = {
                    "type": "default",
                    "schema": _fields[field]["schema"],
                    "default": None,
                }
                _class.model_fields[field].default = None

        _class.__pydantic_validator__ = SchemaValidator(_core)
        _class.__pydantic_serializer__ = SchemaSerializer(_core)

        return _class

    if fields and isclass(fields[0]) and issubclass(fields[0], BaseModel):
        _class = fields[0]
        fields = _class.model_fields
        return dec(_class)

    return dec