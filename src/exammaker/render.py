from fpdf import FPDF

def render_exam(exam_template, question_list):
    exam = FPDF()
    for page in exam_template.front_matter:
        render_page(page)
    for question in question_list:
        rend