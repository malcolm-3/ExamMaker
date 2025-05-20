import random
from typing import List, Optional

from marshmallow import Schema, post_load
from marshmallow.fields import Nested, String

from .question import Question, QuestionSchema


class ExamSection:

    def __init__(self,
                 title: Optional[str] = None,
                 question_list: Optional[List[Question]] = None,
    ):
        self.title = title
        if question_list is None:
            question_list = []  # pragma: no cover
        self.question_list = question_list

    def shuffle(self):
        random.shuffle(self.question_list)

    def format_questions(self, global_variables=None):
        for question in self.question_list:
            question.format_question(global_variables)


class ExamSectionSchema(Schema):
    title = String()
    question_list = Nested(QuestionSchema, many=True)

    @post_load
    def make_section(self, data, **_):
        return ExamSection(**data)