import json

from .question import QuestionType

PUBLIC_ENUMS = {
    'QuestionType': QuestionType,
    # ...
}

ENCODER_KWARG = 'cls'
DECODER_KWARG = 'object_hook'

# This code provides a generic mechanism for enum serialization/deserialization
# The JSON might be "prettier" and/or more easily manually generated with a
# more class specific serializer, but for now...


def _generate_enum_encoder(existing_encoder_cls):
    if existing_encoder_cls is None:
        existing_encoder_cls = json.JSONEncoder

    class EnumEncoder(existing_encoder_cls):
        def default(self, obj):
            if type(obj) in PUBLIC_ENUMS.values():
                return {"__enum__": str(obj)}
            return super().default(obj)

    return EnumEncoder


def _generate_object_hook(existing_object_hook):
    if existing_object_hook is None:
        def existing_object_hook(d):
            return d

    def as_enum(d):
        if "__enum__" in d:
            name, member = d["__enum__"].split(".")
            return getattr(PUBLIC_ENUMS[name], member)
        else:
            return existing_object_hook(d)

    return as_enum


def dump(obj, fp, *args, **kwargs):
    kwargs[ENCODER_KWARG] = _generate_enum_encoder(kwargs.get(ENCODER_KWARG))
    return json.dump(obj, fp, *args, **kwargs)


def dumps(obj, *args, **kwargs):
    kwargs[ENCODER_KWARG] = _generate_enum_encoder(kwargs.get(ENCODER_KWARG))
    return json.dumps(obj, *args, **kwargs)


def load(fp, *args, **kwargs):
    kwargs[DECODER_KWARG] = _generate_object_hook(kwargs.get(DECODER_KWARG))
    return json.load(fp, *args, **kwargs)


def loads(s, *args, **kwargs):
    kwargs[DECODER_KWARG] = _generate_object_hook(kwargs.get(DECODER_KWARG))
    return json.loads(s, *args, **kwargs)
