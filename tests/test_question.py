from math import sqrt

from PIL import Image, ImageChops

from exammaker.question import QuestionSchema

INPUT_JSON_1 = ("{\n"
                "    \"height\": 100.0,\n"
                "    \"qtype\": \"SHORT_ANSWER\",\n"
                "    \"text\": \"A mass <i>m</i><sub>1</sub> of {m1} kg falls from rest a distance of {d} meters.  "
                "What is its final velocity?\",\n"
                "    \"answer\": \"sqrt(d*g)\",\n"
                "    \"variables\": [\n"
                "        [\n"
                "            \"g\",\n"
                "            \"9.8\"\n"
                "        ],\n"
                "        [\n"
                "            \"m1\",\n"
                "            \"choose(1,2,3)\"\n"
                "        ],\n"
                "        [\n"
                "            \"d\",\n"
                "            \"choose(11,12,13)\"\n"
                "        ]\n"
                "    ],\n"
                "    \"image\": \"\"\n"
                "}")

INPUT_JSON_2 = ("{\n"
                "    \"height\": 100.0,\n"
                "    \"qtype\": \"SHORT_ANSWER\",\n"
                "    \"text\": \"A mass <i>m</i><sub>1</sub> of {m1} kg falls from rest a distance of {d} meters.  "
                "What is its final kinetic energy?\",\n"
                "    \"answer\": \"m1 * d * g / 2\",\n"
                "    \"variables\": [\n"
                "        [\n"
                "            \"g\",\n"
                "            \"9.8\"\n"
                "        ],\n"
                "        [\n"
                "            \"m1\",\n"
                "            \"choose(1,2,3)\"\n"
                "        ],\n"
                "        [\n"
                "            \"d\",\n"
                "            \"choose(11,12,13)\"\n"
                "        ]\n"
                "    ],\n"
                "    \"image_file\": \"x.png\"\n"
                "}")


def test_question():

    schema = QuestionSchema()

    q = schema.loads(INPUT_JSON_1)

    assert q is not None
    assert schema.dumps(q, indent=4) == INPUT_JSON_1

    q.format_question()

    g = q._formatted_variables['g']
    m1 = q._formatted_variables['m1']
    d = q._formatted_variables['d']

    assert g == 9.8
    assert m1 in (1, 2, 3)
    assert d in (11, 12, 13)

    assert q.formatted_answer == f'{q.answer} = {sqrt(g * d)}'


def test_question_with_image():

    schema = QuestionSchema()

    q = schema.loads(INPUT_JSON_2)

    assert q is not None
    assert isinstance(q.image, Image.Image)

    q.format_question()

    g = q._formatted_variables['g']
    m1 = q._formatted_variables['m1']
    d = q._formatted_variables['d']

    assert g == 9.8
    assert m1 in (1, 2, 3)
    assert d in (11, 12, 13)

    assert q.formatted_answer == f'{q.answer} = {m1 * g * d / 2}'

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
