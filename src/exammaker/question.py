import json
from base64 import b64encode, b64decode
from enum import Enum
from pathlib import Path
from typing import Optional, List

from PIL import Image
from marshmallow import Schema, fields, post_load, ValidationError

from .parser import ExamMakerParser


class QuestionType(Enum):
    TRUE_FALSE = 'True/False'
    SHORT_ANSWER = 'Short Answer'


DEFAULT_HEIGHT = {
    QuestionType.TRUE_FALSE: 20,
    QuestionType.SHORT_ANSWER: 100,
}


class Question:

    def __init__(self,
                 qtype: QuestionType = QuestionType.SHORT_ANSWER,
                 text: str = "",
                 answer: str = "",
                 variables: Optional[List[List[str]]] = None,
                 height: Optional[float] = None,
                 image: Optional[Image.Image] = None,
                 image_file: Optional[Path] = None,
                 ):
        if variables is None:
            variables = {}
        if height is None:
            height = DEFAULT_HEIGHT[qtype]

        self.height = height
        self.qtype = qtype
        self.text = text
        self.answer = answer
        self.variables = variables
        self.image = None
        self.formatted_text = None
        self.formatted_answer = None

        if image is None and image_file:
            self.image = Image.open(image_file)
        else:
            self.image = image

    def _clear_formatting(self):
        self._formatted_variables = {}
        self.formatted_text = ""
        self.formatted_answer = ""

    def format_question(self, global_variables=None):
        try:
            if global_variables is None:
                global_variables = {}
            self._clear_formatting()
            parser = ExamMakerParser()
            for varnam, varexp in self.variables:
                value = parser.evaluate(f'{varnam} = {varexp}')
                self._formatted_variables[varnam] = value
            self.formatted_text = self.text.format(**global_variables, **self._formatted_variables)
            answer_value = parser.evaluate(self.answer)
            self.formatted_answer = " = ".join([self.answer, str(answer_value)])
        except Exception as e:
            raise Exception('Exception encountered with question "'+self.text+'"') from e


class ImageField(fields.Dict):
    def _serialize(self, value, attr, obj, **kwargs):
        if value is None:
            return ""
        if not isinstance(value, Image.Image):
            raise ValidationError('Image is not of type PIL.Image.Image')
        d = {
            'width': value.size[0],
            'height': value.size[1],
            'mode': value.mode,
            'data': b64encode(value.tobytes()).decode()
        }
        return json.dumps(d)

    def _deserialize(self, value, attr, data, **kwargs):
        if not value:
            return None
        try:
            obj = json.loads(value)
            width = obj['width']
            height = obj['height']
            bdata = b64decode(obj['data'].encode())
            mode = obj['mode']
            return Image.frombytes(mode, (width, height), bdata)
        except Exception as e:
            raise ValidationError(str(e))


class QuestionSchema(Schema):
    height = fields.Float()
    qtype = fields.Enum(QuestionType)
    text = fields.Str()
    answer = fields.Str()
    variables = fields.List(fields.List(fields.Str()))
    image = ImageField(required=False)
    image_file = fields.Str(required=False, load_only=True)

    @post_load
    def make_question(self, data, **_):
        return Question(**data)

