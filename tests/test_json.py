import json
from io import StringIO

from exammaker.json import dump, dumps, load, loads
from exammaker.question import QuestionType

JSON_OBJ = {
    "i": 1,
    "f": 1.1,
    "s": "abc",
    "l": ["a", "b", "c"],
    "e": QuestionType.SHORT_ANSWER,
}


def test_dumps_loads() -> None:
    s = dumps(JSON_OBJ)  # type: ignore[no-untyped-call]
    assert s is not None
    o = loads(s)  # type: ignore[no-untyped-call]
    assert o is not None
    assert o == JSON_OBJ


def test_dump_load() -> None:
    outfile = StringIO()
    dump(JSON_OBJ, outfile)  # type: ignore[no-untyped-call]
    s = outfile.getvalue()
    assert s is not None
    infile = StringIO(s)
    o = load(infile)  # type: ignore[no-untyped-call]
    assert o is not None
    assert o == JSON_OBJ


def test_dumps_loads_with_encoder() -> None:
    s = dumps(JSON_OBJ, cls=json.JSONEncoder)  # type: ignore[no-untyped-call]
    assert s is not None
    o = loads(s)  # type: ignore[no-untyped-call]
    assert o is not None
    assert o == JSON_OBJ
