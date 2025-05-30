from pathlib import Path

from exammaker.builder import ExamBuilder
from exammaker.section import ExamSectionSchema


def test_builder() -> None:
    with Path("tests/sections.json").open("r") as fh:
        sections = ExamSectionSchema().loads(fh.read(), many=True)

    assert sections is not None
    assert len(sections) == 2

    builder = ExamBuilder(
        title="Test Exam",
        front_pages=["tests/front1.html", "tests/front2.html"],
        sections=sections,
        back_pages=["tests/back.html"],
    )

    assert builder is not None

    version, exam_pdf, key_pdf = builder.generate_exam()

    assert version == "a"
    assert exam_pdf is not None
    assert key_pdf is not None
