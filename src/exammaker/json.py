import json
from json import JSONEncoder

from .question import QuestionType

PUBLIC_ENUMS = {
        'QuestionType': QuestionType,
        # ...
}

class EnumEncoder(json.JSONEncoder):
    def __init__(self, encoder=None):
        if encoder is not None:
            self._default_encoder = encoder
        else:
            self._default_encoder = json.JSONEncoder

        self._default_encoder = encoder
    def default(self, obj):
        if type(obj) in PUBLIC_ENUMS.values():
            return {"__enum__": str(obj)}
        return self._default_encoder.default(self, obj)

def _generate_object_hook(existing_object_hook):
    if existing_object_hook is None:
        existing_object_hook = lambda d: d
    def as_enum(d):
        if "__enum__" in d:
            name, member = d["__enum__"].split(".")
            return getattr(PUBLIC_ENUMS[name], member)
        else:
            return existing_object_hook(d)
    return as_enum


def dump(obj, fp, *args, **kwargs):
    kwargs['cls'] = EnumEncoder(kwargs.get('cls'))
    return json.dump(obj, fp, *args, **kwargs)

def dumps(obj, *args, **kwargs):
    kwargs['cls'] = EnumEncoder(kwargs.get('cls'))
    return json.dumps(obj, *args, **kwargs)

def load(fp, *args, **kwargs):
    kwargs['object_hook'] = _generate_object_hook(kwargs.get('object_hook'))
    return json.load(fp, *args, **kwargs)

def loads(s, *args, **kwargs):
    kwargs['object_hook'] = _generate_object_hook(kwargs.get('object_hook'))
    return json.loads(s, *args, **kwargs)