from click.testing import CliRunner

from exammaker.cli import cli

EXPECTED_HELP = """Usage: exammaker [OPTIONS] TITLE NVERS QUESTION_SECTION_JSON

  Generate multiple versions of an exam from a set of front pages, back pages,
  and questions.

  The front and back pages should be in HTML format. They can contain format-
  string templated variables. Current variables include the "title" and the
  "version". At the very least you will want to include the "version" somewhere
  so that you can tell from the printed exam what the correct key to use.

  The question_section_json file is a JSON list of ExamSections.
  Each Exam Section contains an optional "title" field and a
  "question_list" field, which is a JSON list of Questions.
  Each Question has the following properties
      qtype.............."SHORT_ANSWER", or "MULTIPLE_CHOICE"
      text...............the str.format templated question text
      answer.............a plusminus ArithmeticParse string used to
                         calculate the answer from the variables
      alt_answers........alternative answers for multiple choice
                         questions, which can be plusminus strings
                         including the variable "answer" which is
                         the specific answer value for this version
                         of the exam
      all_of_the_above...if true include "All of the above" as
                         a possible answer
      none_of_the_above..if true include "None of the above" as
                         a possible answer
      variables..........a list of lists of name/value strings
                         - the name is the variable name used both
                           a plusminus variable and as a str.format
                           string for the question text
                         - the value is a plusminus expression which
                           can include the "choose" function that randomly
                           picks one of its arguments.
      image_file.........the path to an image file for the question (optional)
      height.............the vertical height, in points, to be used for
                         the question

Options:
  -f, --front-page PATH   HTML format template file for front pages, repeat for
                          multiple pages.
  -b, --back-page PATH    HTML format template file for back pages, repeat for
                          multiple pages.
  -o, --output-root TEXT  Root of output file names (default is to use the
                          tittle)
  --help                  Show this message and exit.
"""


def test_cli(tmpdir):
    runner = CliRunner()

    result = runner.invoke(cli, ["--help"])
    assert result.exit_code == 0
    assert result.output == EXPECTED_HELP

    result = runner.invoke(
        cli,
        [
            "-f",
            "front1.html",
            "-f",
            "front2.html",
            "-o",
            tmpdir.join("TestExam"),
            "-b",
            "back.html",
            "Test Exam",
            "2",
            "sections.json",
        ],
    )
    assert result.exit_code == 0
    assert tmpdir.join("TestExam.a.exam.pdf").exists()
    assert tmpdir.join("TestExam.a.key.pdf").exists()
    assert tmpdir.join("TestExam.b.exam.pdf").exists()
    assert tmpdir.join("TestExam.b.key.pdf").exists()
