from fpdf import FPDF, Align

TOP_SKIP = 20


class Exam:

    def __init__(self,
                 title="Exam",
                 variables=None,
                 front_pages = (),
                 question_list = (),
                 back_pages =(),
                 ):
        self._title = title
        if variables is None:
            variables = {}
        self._variables = variables
        self._front_pages = front_pages
        self._question_list = question_list
        self._back_pages = back_pages

    def print_exam(self, print_key=False):
        header_string = f"{self._title} page {{page}}"

        class PDF(FPDF):
            def header(self):
                if self.pages_count > 1:
                    self.cell(w=0, text=header_string.format(page=self.pages_count), align=Align.R)

        pdf = PDF()
        page_height = pdf.eph
        for page in self._front_pages:
            pdf.add_page()
            html = page.format(**self._variables)
            pdf.write_html(html)
        if self._question_list:
            pdf.add_page()
            pdf.set_y(TOP_SKIP)
            for iq, question in enumerate(self._question_list):
                ystart = pdf.get_y()
                if ystart + question.height > page_height:
                    pdf.add_page()
                    pdf.set_y(TOP_SKIP)
                    ystart = pdf.get_y()
                pdf.write_html(f'{iq+1}. {question.formatted_text}')
                if question.image:
                    kwargs = {}
                    if question.image.height > 200:
                        kwargs['h'] = 50
                    elif question.image.width > 240:
                        kwargs['w'] = 60
                    pdf.image(question.image, **kwargs)
                if print_key:
                    pdf.set_text_color(255, 0, 0)
                    pdf.write_html(question.formatted_answer)
                    pdf.set_text_color(0)
                ystart_new = ystart + question.height
                if ystart_new > pdf.get_y():
                    pdf.set_y(ystart_new)
        for page in self._back_pages:
            pdf.add_page()
            html = page.format(**self._variables)
            pdf.write_html(html)

        return pdf.output()