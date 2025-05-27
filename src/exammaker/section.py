import random

from marshmallow import Schema, post_load
from marshmallow.fields import Nested, String

from .question import Question, QuestionSchema


class ExamSection:
    def __init__(
        self,
        title: str | None = None,
        question_list: list[Question] | None = None,
    ) -> None:
        self.title = title
        if question_list is None:
            question_list = []  # pragma: no cover
        self.question_list = question_list

    def shuffle(self) -> None:
        random.shuffle(self.question_list)

    def format_questions(self, global_variables: dict[str, str] | None = None) -> None:
        for question in self.question_list:
            question.format_question(global_variables)


class ExamSectionSchema(Schema):
    title = String()
    question_list = Nested(QuestionSchema, many=True)

    @post_load
    def make_section(self, data, **_):  # type: ignore[no-untyped-def]
        return ExamSection(**data)
