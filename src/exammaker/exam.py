from fpdf import FPDF, Align

from exammaker.section import ExamSection

MAX_IMAGE_WIDTH_PX = 240
MAX_IMAGE_WIDTH_PDF = MAX_IMAGE_WIDTH_PX // 4
MAX_IMAGE_HEIGHT_PX = 200
MAX_IMAGE_HEIGHT_PDF = MAX_IMAGE_HEIGHT_PX // 4

TOP_SKIP = 20


class Exam:
    def __init__(
        self,
        *,
        title: str = "Exam",
        variables: dict[str, str] | None = None,
        front_pages: list[str] | None = None,
        sections: list[ExamSection] | None = None,
        back_pages: list[str] | None = None,
    ):
        if back_pages is None: back_pages = []
        if sections is None: sections = []
        if front_pages is None: front_pages = []
        self._title = title
        if variables is None:
            variables = {}  # pragma: no cover
        self._variables = variables
        self._front_pages = front_pages
        self._sections = sections
        self._back_pages = back_pages

    def print_exam(self, *, print_key: bool = False) -> bytearray:
        header_string = f"{self._title} page {{page}}"

        class PDF(FPDF):
            def header(self) -> None:
                if self.pages_count > 1:
                    self.cell(
                        w=0,
                        text=header_string.format(page=self.pages_count),
                        align=Align.R,
                    )

        pdf = PDF()
        page_height = pdf.eph
        for page in self._front_pages:
            pdf.add_page()
            html = page.format(**self._variables)
            pdf.write_html(html)
        for section in self._sections:
            self._print_section(page_height, pdf, print_key, section)
        for page in self._back_pages:
            pdf.add_page()
            html = page.format(**self._variables)
            pdf.write_html(html)

        return pdf.output()

    @staticmethod
    def _print_section(
        page_height: float,
        pdf: FPDF,
        print_key: bool,  # noqa: FBT001
        section: ExamSection,
    ) -> None:
        pdf.add_page()
        if section.title:
            pdf.write_html(section.title)
        if section.question_list:
            pdf.set_y(TOP_SKIP)
            for iq, question in enumerate(section.question_list):
                ystart = pdf.get_y()
                if ystart + question.height > page_height:
                    pdf.add_page()
                    pdf.set_y(TOP_SKIP)
                    ystart = pdf.get_y()
                pdf.write_html(f"{iq + 1}. {question.formatted_text}")
                if question.image:
                    kwargs = {}
                    if question.image.height > MAX_IMAGE_HEIGHT_PX:
                        kwargs["h"] = MAX_IMAGE_HEIGHT_PDF  # pragma: no cover
                    elif question.image.width > MAX_IMAGE_WIDTH_PX:
                        kwargs["w"] = MAX_IMAGE_WIDTH_PDF  # pragma: no cover
                    pdf.image(question.image, **kwargs)  # type: ignore[arg-type]
                if print_key:
                    pdf.set_text_color(255, 0, 0)
                    pdf.write_html(question.formatted_answer)
                    pdf.set_text_color(0)
                ystart_new = ystart + question.height
                if ystart_new > pdf.get_y():
                    pdf.set_y(ystart_new)
