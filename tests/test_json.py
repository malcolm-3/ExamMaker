import json
from io import StringIO

from exammaker.json import dumps, loads, dump, load
from exammaker.question import QuestionType

JSON_OBJ = {
    "i": 1,
    "f": 1.1,
    "s": "abc",
    "l": ["a", "b", "c"],
    "e": QuestionType.SHORT_ANSWER,
}


def test_dumps_loads() -> None:
    s = dumps(JSON_OBJ)
    assert s is not None
    o = loads(s)
    assert o is not None
    assert o == JSON_OBJ


def test_dump_load() -> None:
    outfile = StringIO()
    dump(JSON_OBJ, outfile)
    s = outfile.getvalue()
    assert s is not None
    infile = StringIO(s)
    o = load(infile)
    assert o is not None
    assert o == JSON_OBJ


def test_dumps_loads_with_encoder() -> None:
    s = dumps(JSON_OBJ, cls=json.JSONEncoder)
    assert s is not None
    o = loads(s)
    assert o is not None
    assert o == JSON_OBJ
