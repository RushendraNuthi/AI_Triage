from weasyprint import HTML
from flask import render_template

def generate_pdf_report(incidents):
    html_string = render_template('report_template.html', incidents=incidents)
    html = HTML(string=html_string)
    html.write_pdf('reports/weekly_report.pdf')
