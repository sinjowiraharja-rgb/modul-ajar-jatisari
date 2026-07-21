import os
from jinja2 import Environment, FileSystemLoader

WEASYPRINT_AVAILABLE = False
HTML = None
CSS = None

def _init_weasyprint():
    global WEASYPRINT_AVAILABLE, HTML, CSS
    if not WEASYPRINT_AVAILABLE:
        try:
            from weasyprint import HTML as _HTML, CSS as _CSS
            HTML = _HTML
            CSS = _CSS
            WEASYPRINT_AVAILABLE = True
        except (ImportError, OSError):
            WEASYPRINT_AVAILABLE = False

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates')


def generate_pdf(modul, output_path):
    """
    Generate dokumen PDF dari modul ajar menggunakan WeasyPrint (HTML to PDF).
    Jika WeasyPrint tidak tersedia, return None.
    """
    _init_weasyprint()
    if not WEASYPRINT_AVAILABLE:
        return None

    env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))
    template = env.get_template('pdf_template.html')

    dimensi = modul.get('dimensi_pancasila', '')
    if isinstance(dimensi, str):
        dimensi = [d.strip() for d in dimensi.split(',') if d.strip()]

    html_content = template.render(modul=modul, dimensi_list=dimensi)

    HTML(string=html_content, base_url=BASE_DIR).write_pdf(output_path)
    return output_path
