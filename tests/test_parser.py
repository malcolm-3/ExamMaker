import pytest

from exammaker.parser import ExamMakerParser

tests = [
    {"expression": "2+2", "check": lambda x: x == 4},
    {"expression": "4+4/2", "check": lambda x: x == 6},
    {"expression": "choose(1.1, 2.2, 3.3)", "check": lambda x: x in (1.1, 2.2, 3.3)},
    {"expression": "pi", "check": lambda x: x == pytest.approx(3.14, rel=1e-3)},
    {"expression": "i=choose(0,1,2)", "check": lambda x: x in (0, 1, 2)},
    {"expression": "select(i,0,1,2) - i", "check": lambda x: x == 0},
]


def test_parser() -> None:
    parser = ExamMakerParser()
    assert parser is not None
    for test in tests:
        if callable(test["check"]):
            assert test["check"](parser.evaluate(test["expression"]))
