import json
from typing import List

import click

from .builder import ExamBuilder
from .question import QuestionSchema


@click.command(help="""
Generate multiple versions of an exam from a set of front pages, back pages, and questions.

The front and back pages should be in HTML format.
They can contain format-string templated variables.
Current variables include the "title" and the "version".
At the very least you will want to include the "version"
somewhere so that you can tell from the printed exam what
the correct key to use.

\b
The questions.json file is a list of Questions.
Each Question has the following properties
    qtype        currently this can only be "SHORT_ANSWER"
    text         the str.format templated question text
    answer       a plusminus AritmeticParse string used to 
                 calculate the answer from the variables
    variables    a list of lists of name/value strings
                 - the name is the variable name used both
                   a plusminus variable and as a str.format
                   string for the question text
                 - the value is a plusminus expression which
                   can include the "choose" function that randomly
                   picks one of its arguments.
    image_file   the path to an image file for the question (optional)
    height       the vertical height, in points, to be used for
                 the question
                 
""")
@click.option("-f",
              "--front-page",
              multiple=True,
              type=click.Path(exists=True),
              help='HTML format template file for front pages, repeat for multiple pages.',
              )
@click.option("-b",
              "--back-page",
              multiple=True,
              type=click.Path(exists=True),
              help='HTML format template file for back pages, repeat for multiple pages.',
              )
@click.option("-o",
              "--output-root",
              type=str,
              help='Root of output file names (default is to use the tittle)',
              )
@click.argument('title', type=str, required=True)
@click.argument('nvers', type=int, required=True)
@click.argument('question_json', type=click.Path(exists=True), required=True)
def cli(title: str,
        nvers: int,
        question_json: str,
        front_page: List[str],
        back_page: List[str],
        output_root: str,):

    if not output_root:
        output_root = title

    front_pages = []
    for page_file in front_page:
        with open(page_file, 'r') as fh:
            front_pages.append(fh.read())

    back_pages = []
    for page_file in back_page:
        with open(page_file, 'r') as fh:
            back_pages.append(fh.read())

    with open(question_json, 'r') as fh:
        question_list = QuestionSchema().loads(fh.read(), many=True)

    builder = ExamBuilder(title, variables={'title': title},
                          front_pages=front_pages, question_list=question_list, back_pages=back_pages)

    while nvers > 0:
        version_str, exam, exam_key = builder.generate_exam()

        exam_output_file = f'{output_root}.{version_str}.exam.pdf'
        with open(exam_output_file, 'wb') as fh:
            fh.write(exam)

        key_output_file = f'{output_root}.{version_str}.key.pdf'
        with open(key_output_file, 'wb') as fh:
            fh.write(exam_key)

        nvers -= 1
