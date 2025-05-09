from enum import Enum

class QuestionType(Enum):
    TRUE_FALSE = 'True/False'
    SHORT_ANSWER = 'Short Answer'

DEFAULT_QUESTION_TYPE = QuestionType.SHORT_ANSWER
DEFAULT_TEMPLATE = "Question?"

class Question:

    def __init__(self,
                 qtype: QuestionType=DEFAULT_QUESTION_TYPE,
                 template=DEFAULT_TEMPLATE,
                 ):
        self._type = type
        self._template = template
