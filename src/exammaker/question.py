import json
import random
from base64 import b64decode, b64encode
from enum import Enum
from pathlib import Path

from marshmallow import Schema, ValidationError, fields, post_load
from PIL import Image, ImageFile

from .parser import ExamMakerParser


class QuestionType(Enum):
    TRUE_FALSE = "True/False"
    SHORT_ANSWER = "Short Answer"
    MULTIPLE_CHOICE = "Multiple Choice"


DEFAULT_HEIGHT = {
    QuestionType.TRUE_FALSE: 20,
    QuestionType.SHORT_ANSWER: 100,
    QuestionType.MULTIPLE_CHOICE: 100,
}


LETTER = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


class QuestionFormattingError(Exception):
    def __init__(self, question_text: str) -> None:
        super().__init__(f'Exception encountered with question "{question_text}"')


class Question:
    def __init__(  # noqa: PLR0913
        self,
        *,
        qtype: QuestionType = QuestionType.SHORT_ANSWER,
        text: str = "",
        answer: str = "",
        alt_answers: list[str] | None = None,
        all_of_the_above: bool = False,
        none_of_the_above: bool = False,
        variables: list[list[str]] | None = None,
        height: float | None = None,
        image: Image.Image | ImageFile.ImageFile | None = None,
        image_file: Path | None = None,
    ) -> None:
        if variables is None:
            variables = []  # pragma: no cover
        if alt_answers is None:
            alt_answers = []  # pragma: no cover
        if height is None:
            height = DEFAULT_HEIGHT[qtype]  # pragma: no cover

        self.height = height
        self.qtype = qtype
        self.text = text
        self.answer = answer
        self.alt_answers = alt_answers
        self.all_of_the_above = all_of_the_above
        self.none_of_the_above = none_of_the_above
        self.variables = variables
        self.image: Image.Image | ImageFile.ImageFile | None = None
        self.formatted_text: str = ""
        self.formatted_answer: str = ""
        self._formatted_variables: dict[str, str] = {}
        self.formatted_alt_answers: list[str] = []

        if image is None and image_file:
            self.image = Image.open(image_file)
        else:
            self.image = image

    def _clear_formatting(self) -> None:
        self._formatted_variables = {}
        self.formatted_text = ""
        self.formatted_answer = ""
        self.formatted_alt_answers = []

    def format_question(self, global_variables: dict[str, str] | None = None) -> None:
        try:
            if global_variables is None:
                global_variables = {}
            self._clear_formatting()
            parser = ExamMakerParser()
            for varnam, varexp in self.variables:
                value = parser.evaluate(f"{varnam} = {varexp}")
                self._formatted_variables[varnam] = value
            answer_value = parser.evaluate(f"answer = {self.answer}")
            for alt_answer in self.alt_answers:
                self.formatted_alt_answers.append(parser.evaluate(alt_answer))
            self.formatted_text = self.text.format(
                **global_variables,
                **self._formatted_variables,
            )
            self.formatted_answer = " = ".join([self.answer, str(answer_value)])
            if self.qtype == QuestionType.MULTIPLE_CHOICE:
                self._multiple_choice_mods(answer_value)

        except Exception as e:
            raise QuestionFormattingError(self.text) from e

    def _multiple_choice_mods(self, answer_value: str) -> None:
        answer_list = []
        if answer_value not in ("All of the above", "None of the above"):
            answer_list.append(answer_value)
        answer_list.extend(self.formatted_alt_answers)
        random.shuffle(answer_list)
        if self.all_of_the_above:
            answer_list.append("All of the above")
        if self.none_of_the_above:
            answer_list.append("None of the above")
        for i, answer in enumerate(answer_list):
            self.formatted_text += f"<br>{LETTER[i]}) {answer}"
            if answer == answer_value:
                self.formatted_answer += f" ({LETTER[i]})"


class ImageField(fields.Dict):
    def _serialize(self, value, *_, **__):  # type: ignore[no-untyped-def]
        if value is None:
            return ""
        if not isinstance(value, Image.Image):
            msg = "Image is not of type PIL.Image.Image"
            raise ValidationError(msg)
        d = {
            "width": value.size[0],
            "height": value.size[1],
            "mode": value.mode,
            "data": b64encode(value.tobytes()).decode(),
        }
        return json.dumps(d)

    def _deserialize(self, value, *_, **__):  # type: ignore[no-untyped-def]
        if not value:
            return None
        try:
            obj = json.loads(value)
            width = obj["width"]
            height = obj["height"]
            bdata = b64decode(obj["data"].encode())
            mode = obj["mode"]
            return Image.frombytes(mode, (width, height), bdata)
        except Exception as e:
            msg = "Exception encoutered deserializing ImageField"
            raise ValidationError(msg) from e


class QuestionSchema(Schema):
    height = fields.Float()
    qtype = fields.Enum(QuestionType)
    text = fields.Str()
    answer = fields.Str()
    alt_answers = fields.List(fields.Str())
    all_of_the_above = fields.Bool()
    none_of_the_above = fields.Bool()
    variables = fields.List(fields.List(fields.Str()))
    image = ImageField(required=False)
    image_file = fields.Str(required=False, load_only=True)

    @post_load
    def make_question(self, data, **_):  # type: ignore[no-untyped-def]
        return Question(**data)
