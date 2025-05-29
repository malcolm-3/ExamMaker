from .exam import Exam
from .section import ExamSection


class ExamBuilder:
    def __init__(
        self,
        title: str = "Exam",
        variables: dict[str, str] | None = None,
        front_pages: list[str] | None = None,
        sections: list[ExamSection] | None = None,
        back_pages: list[str] | None = None,
    ) -> None:
        if variables is None:
            variables = {}  # pragma: no cover
        if front_pages is None:
            front_pages = []  # pragma: no cover
        if sections is None:
            sections = []  # pragma: no cover
        if back_pages is None:
            back_pages = []  # pragma: no cover

        self._title = title
        self._variables = variables
        self._front_pages = front_pages
        self._sections = sections
        self._back_pages = back_pages

        self._version = 0

    def _version_to_str(self) -> str:
        char_list: list[str] = []
        orda = ord("a")
        v = self._version
        while v > 0 or len(char_list) == 0:
            v26 = v % 26
            v //= 26
            char_list.insert(0, chr(orda + v26))
        return "".join(char_list)

    def generate_exam(
        self,
    ) -> tuple[
        str,
        bytearray,
        bytearray,
    ]:
        version_str = self._version_to_str()
        self._variables["version"] = version_str
        for section in self._sections:
            section.shuffle()
            section.format_questions(self._variables)
        exam = Exam(
            title=self._title,
            variables=self._variables,
            front_pages=self._front_pages,
            sections=self._sections,
            back_pages=self._back_pages,
        )
        self._version += 1
        return version_str, exam.print_exam(), exam.print_exam(print_key=True)
