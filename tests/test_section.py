from exammaker.section import ExamSectionSchema

INPUT_JSON_1 = (
    '[\n    {\n        "title": "section title",\n        "question_list": []\n    }\n]'
)

INPUT_JSON_2 = (
    "[\n"
    "    {\n"
    '        "title": "Short Answer",\n'
    '        "question_list": [\n'
    "            {\n"
    '                "height": 100.0,\n'
    '                "qtype": "SHORT_ANSWER",\n'
    '                "text": "A mass <i>m</i><sub>1</sub> of {m1} kg falls from rest a distance of {d} meters.  '
    'What is its final velocity?",\n'
    '                "answer": "sqrt(d*g)",\n'
    '                "alt_answers": [],\n'
    '                "all_of_the_above": false,\n'
    '                "none_of_the_above": false,\n'
    '                "variables": [\n'
    "                    [\n"
    '                        "g",\n'
    '                        "9.8"\n'
    "                    ],\n"
    "                    [\n"
    '                        "m1",\n'
    '                        "choose(1,2,3)"\n'
    "                    ],\n"
    "                    [\n"
    '                        "d",\n'
    '                        "choose(11,12,13)"\n'
    "                    ]\n"
    "                ],\n"
    '                "image": ""\n'
    "            },\n"
    "            {\n"
    '                "height": 100.0,\n'
    '                "qtype": "SHORT_ANSWER",\n'
    '                "text": "A mass <i>m</i><sub>1</sub> of {m1} kg falls from rest a distance of {d} meters.  '
    'What is its final kinetic energy?",\n'
    '                "answer": "m1 * d * g / 2",\n'
    '                "alt_answers": [],\n'
    '                "all_of_the_above": false,\n'
    '                "none_of_the_above": false,\n'
    '                "variables": [\n'
    "                    [\n"
    '                        "g",\n'
    '                        "9.8"\n'
    "                    ],\n"
    "                    [\n"
    '                        "m1",\n'
    '                        "choose(1,2,3)"\n'
    "                    ],\n"
    "                    [\n"
    '                        "d",\n'
    '                        "choose(11,12,13)"\n'
    "                    ]\n"
    "                ],\n"
    '                "image_file": "x.png"\n'
    "            }\n"
    "        ]\n"
    "    },\n"
    "    {\n"
    '        "title": "Multiple Choice",\n'
    '        "question_list": [\n'
    "            {\n"
    '                "height": 100.0,\n'
    '                "qtype": "MULTIPLE_CHOICE",\n'
    '                "text": "Is it shorter to New York or by bus?",\n'
    '                "answer": "\'None of the above\'",\n'
    '                "alt_answers": [\n'
    "                    \"'Who'\",\n"
    "                    \"'What'\",\n"
    "                    \"'Where'\"\n"
    "                ],\n"
    '                "all_of_the_above": true,\n'
    '                "none_of_the_above": true,\n'
    '                "variables": [],\n'
    '                "image": ""\n'
    "            },\n"
    "            {\n"
    '                "height": 100.0,\n'
    '                "qtype": "MULTIPLE_CHOICE",\n'
    '                "text": "Is it shorter to New York or by bus?",\n'
    '                "answer": "\'Why\'",\n'
    '                "alt_answers": [\n'
    "                    \"'Who'\",\n"
    "                    \"'What'\",\n"
    "                    \"'Where'\"\n"
    "                ],\n"
    '                "all_of_the_above": false,\n'
    '                "none_of_the_above": false,\n'
    '                "variables": [],\n'
    '                "image": ""\n'
    "            }\n"
    "        ]\n"
    "    }\n"
    "]"
)

EXPECTED_JSON_2 = (
    "[\n"
    "    {\n"
    '        "title": "Short Answer",\n'
    '        "question_list": [\n'
    "            {\n"
    '                "height": 100.0,\n'
    '                "qtype": "SHORT_ANSWER",\n'
    '                "text": "A mass <i>m</i><sub>1</sub> of {m1} kg falls from rest a distance of {d} meters.  '
    'What is its final velocity?",\n'
    '                "answer": "sqrt(d*g)",\n'
    '                "alt_answers": [],\n'
    '                "all_of_the_above": false,\n'
    '                "none_of_the_above": false,\n'
    '                "variables": [\n'
    "                    [\n"
    '                        "g",\n'
    '                        "9.8"\n'
    "                    ],\n"
    "                    [\n"
    '                        "m1",\n'
    '                        "choose(1,2,3)"\n'
    "                    ],\n"
    "                    [\n"
    '                        "d",\n'
    '                        "choose(11,12,13)"\n'
    "                    ]\n"
    "                ],\n"
    '                "image": ""\n'
    "            },\n"
    "            {\n"
    '                "height": 100.0,\n'
    '                "qtype": "SHORT_ANSWER",\n'
    '                "text": "A mass <i>m</i><sub>1</sub> of {m1} kg falls from rest a distance of {d} meters.  '
    'What is its final kinetic energy?",\n'
    '                "answer": "m1 * d * g / 2",\n'
    '                "alt_answers": [],\n'
    '                "all_of_the_above": false,\n'
    '                "none_of_the_above": false,\n'
    '                "variables": [\n'
    "                    [\n"
    '                        "g",\n'
    '                        "9.8"\n'
    "                    ],\n"
    "                    [\n"
    '                        "m1",\n'
    '                        "choose(1,2,3)"\n'
    "                    ],\n"
    "                    [\n"
    '                        "d",\n'
    '                        "choose(11,12,13)"\n'
    "                    ]\n"
    "                ],\n"
    '                "image": "{\\"width\\": 5, \\"height\\": 5, \\"mode\\": \\"RGB\\", \\"data\\": \\"vLy8////////9fX12NjY////y8vL4ODg19fX9fX1////9fX1ycnJ9fX1////////2NjY9fX1vLy8////vLy8////////9fX12NjY\\"}"\n'
    "            }\n"
    "        ]\n"
    "    },\n"
    "    {\n"
    '        "title": "Multiple Choice",\n'
    '        "question_list": [\n'
    "            {\n"
    '                "height": 100.0,\n'
    '                "qtype": "MULTIPLE_CHOICE",\n'
    '                "text": "Is it shorter to New York or by bus?",\n'
    '                "answer": "\'None of the above\'",\n'
    '                "alt_answers": [\n'
    "                    \"'Who'\",\n"
    "                    \"'What'\",\n"
    "                    \"'Where'\"\n"
    "                ],\n"
    '                "all_of_the_above": true,\n'
    '                "none_of_the_above": true,\n'
    '                "variables": [],\n'
    '                "image": ""\n'
    "            },\n"
    "            {\n"
    '                "height": 100.0,\n'
    '                "qtype": "MULTIPLE_CHOICE",\n'
    '                "text": "Is it shorter to New York or by bus?",\n'
    '                "answer": "\'Why\'",\n'
    '                "alt_answers": [\n'
    "                    \"'Who'\",\n"
    "                    \"'What'\",\n"
    "                    \"'Where'\"\n"
    "                ],\n"
    '                "all_of_the_above": false,\n'
    '                "none_of_the_above": false,\n'
    '                "variables": [],\n'
    '                "image": ""\n'
    "            }\n"
    "        ]\n"
    "    }\n"
    "]"
)


def test_section():
    schema = ExamSectionSchema()

    section_list = schema.loads(INPUT_JSON_1, many=True)

    assert section_list is not None
    assert schema.dumps(section_list, indent=4, many=True) == INPUT_JSON_1

    for section in section_list:
        section.format_questions()

    section_list = schema.loads(INPUT_JSON_2, many=True)

    assert section_list is not None
    assert schema.dumps(section_list, indent=4, many=True) == EXPECTED_JSON_2

    for section in section_list:
        section.format_questions()
        for question in section.question_list:
            assert question.formatted_text is not None
            assert question.formatted_answer is not None
        section.shuffle()
