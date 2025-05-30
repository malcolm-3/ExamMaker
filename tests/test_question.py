import re
from math import sqrt

import pytest
from marshmallow import ValidationError
from PIL import Image, ImageChops

from exammaker.question import QuestionFormattingError, QuestionSchema

INPUT_JSON_1 = (
    "{\n"
    '    "height": 100.0,\n'
    '    "qtype": "SHORT_ANSWER",\n'
    '    "text": "A mass <i>m</i><sub>1</sub> of {m1} kg falls from rest a distance of {d} meters.  '
    'What is its final velocity?",\n'
    '    "answer": "sqrt(d*g)",\n'
    '    "solution_text": "{answer_expression} = {answer_value}",\n'
    '    "alt_answers": [],\n'
    '    "all_of_the_above": false,\n'
    '    "none_of_the_above": false,\n'
    '    "variables": [\n'
    "        [\n"
    '            "g",\n'
    '            "9.8"\n'
    "        ],\n"
    "        [\n"
    '            "m1",\n'
    '            "choose(1,2,3)"\n'
    "        ],\n"
    "        [\n"
    '            "d",\n'
    '            "choose(11,12,13)"\n'
    "        ]\n"
    "    ],\n"
    '    "image": ""\n'
    "}"
)

INPUT_JSON_2 = (
    "{\n"
    '    "height": 100.0,\n'
    '    "qtype": "SHORT_ANSWER",\n'
    '    "text": "A mass <i>m</i><sub>1</sub> of {m1} kg falls from rest a distance of {d} meters.  '
    'What is its final kinetic energy?",\n'
    '    "answer": "m1 * d * g / 2",\n'
    '    "solution_text": "{answer_expression} = {answer_value}",\n'
    '    "alt_answers": [],\n'
    '    "all_of_the_above": false,\n'
    '    "none_of_the_above": false,\n'
    '    "variables": [\n'
    "        [\n"
    '            "g",\n'
    '            "9.8"\n'
    "        ],\n"
    "        [\n"
    '            "m1",\n'
    '            "choose(1,2,3)"\n'
    "        ],\n"
    "        [\n"
    '            "d",\n'
    '            "choose(11,12,13)"\n'
    "        ]\n"
    "    ],\n"
    '    "image_file": "tests/x.png"\n'
    "}"
)

INPUT_JSON_3 = (
    "{\n"
    '    "height": 100.0,\n'
    '    "qtype": "MULTIPLE_CHOICE",\n'
    '    "text": "Is it shorter to New York or by bus?",\n'
    '    "answer": "\'None of the above\'",\n'
    '    "solution_text": "{answer_expression} = {answer_value}",\n'
    '    "alt_answers": ["\'Who\'", "\'What\'", "\'Where\'"],\n'
    '    "all_of_the_above": true,\n'
    '    "none_of_the_above": true,\n'
    '    "variables": [\n'
    "    ],\n"
    '    "image": ""\n'
    "}"
)

INPUT_JSON_4 = (
    "{\n"
    '    "height": 100.0,\n'
    '    "qtype": "MULTIPLE_CHOICE",\n'
    '    "text": "Is it shorter to New York or by bus?",\n'
    '    "answer": "\'Why\'",\n'
    '    "solution_text": "{answer_expression} = {answer_value}",\n'
    '    "alt_answers": ["\'Who\'", "\'What\'", "\'Where\'"],\n'
    '    "all_of_the_above": false,\n'
    '    "none_of_the_above": false,\n'
    '    "variables": [\n'
    "    ],\n"
    '    "image": ""\n'
    "}"
)
BAD_JSON_1 = (
    "{\n"
    '    "height": 100.0,\n'
    '    "qtype": "MULTIPLE_CHOICE",\n'
    '    "text": "Is it shorter to New York or by bus?",\n'
    '    "answer": "\'None of the above\'",\n'
    '    "solution_text": "{answer_expression} = {answer_value}",\n'
    '    "alt_answers": ["\'Who\'", "\'What\'", "\'Where\'"],\n'
    '    "all_of_the_above": true,\n'
    '    "none_of_the_above": true,\n'
    '    "variables": [\n'
    "    ],\n"
    '    "image": "NOT A PIL IMAGE"\n'
    "}"
)

BAD_JSON_2 = (
    "{\n"
    '    "height": "Not a Number",\n'
    '    "qtype": "MULTIPLE_CHOICE",\n'
    '    "text": "Is it shorter to New York or by bus?",\n'
    '    "answer": "\'None of the above\'",\n'
    '    "solution_text": "{answer_expression} = {answer_value}",\n'
    '    "alt_answers": ["\'Who\'", "\'What\'", "\'Where\'"],\n'
    '    "all_of_the_above": true,\n'
    '    "none_of_the_above": true,\n'
    '    "variables": [\n'
    "    ],\n"
    '    "image": ""\n'
    "}"
)


def test_question() -> None:
    schema = QuestionSchema()

    q = schema.loads(INPUT_JSON_1)

    assert q is not None
    assert schema.dumps(q, indent=4) == INPUT_JSON_1

    q.format_question()

    g = q._formatted_variables["g"]
    m1 = q._formatted_variables["m1"]
    d = q._formatted_variables["d"]

    assert g == 9.8
    assert m1 in (1, 2, 3)
    assert d in (11, 12, 13)

    assert q.formatted_answer == f"{q.answer} = {sqrt(g * d)}"


def test_question_with_image() -> None:
    schema = QuestionSchema()

    q = schema.loads(INPUT_JSON_2)

    assert q is not None
    assert isinstance(q.image, Image.Image)

    q.format_question()

    g = q._formatted_variables["g"]
    m1 = q._formatted_variables["m1"]
    d = q._formatted_variables["d"]

    assert g == 9.8
    assert m1 in (1, 2, 3)
    assert d in (11, 12, 13)

    assert q.formatted_answer == f"{q.answer} = {m1 * g * d / 2}"

    qjson = schema.dumps(q)

    assert qjson is not None
    assert '"image"' in qjson

    q2 = schema.loads(qjson)

    assert q2.height == q.height
    assert q2.qtype == q.qtype
    assert q2.text == q.text
    assert q2.answer == q.answer
    assert q2.variables == q.variables
    assert not ImageChops.difference(q2.image, q.image).getbbox()


def test_multiple_choice() -> None:
    schema = QuestionSchema()

    q = schema.loads(INPUT_JSON_3)

    assert q is not None

    q.format_question()

    assert re.search(r"[ABC]\) Who", q.formatted_text)
    assert re.search(r"[ABC]\) What", q.formatted_text)
    assert re.search(r"[ABC]\) Where", q.formatted_text)
    assert re.search(r"D\) All of the above", q.formatted_text)
    assert re.search(r"E\) None of the above", q.formatted_text)
    assert q.formatted_answer == "'None of the above' = None of the above (E)"

    q = schema.loads(INPUT_JSON_4)

    assert q is not None

    q.format_question()

    assert re.search(r"[ABCD]\) Who", q.formatted_text)
    assert re.search(r"[ABCD]\) What", q.formatted_text)
    assert re.search(r"[ABCD]\) Where", q.formatted_text)
    assert re.search(r"[ABCD]\) Why", q.formatted_text)
    assert re.search(r"'Why' = Why \([ABCD]\)", q.formatted_answer)


def test_bad_input() -> None:
    schema = QuestionSchema()

    with pytest.raises(ValidationError):
        schema.loads(BAD_JSON_1)

    with pytest.raises(ValidationError):
        schema.loads(BAD_JSON_2)

    q = schema.loads(INPUT_JSON_1)
    assert q is not None

    q.image = "THIS IS NOT A PIL IMAGE"
    with pytest.raises(ValidationError):
        schema.dumps(q)

    q.image = ""
    q.variables.append(["badvar", "unknown_func()"])

    with pytest.raises(QuestionFormattingError):
        q.format_question()
