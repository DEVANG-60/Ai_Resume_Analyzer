from pypdf import PdfReader
from docx import Document


def extract_from_pdf(file):
    text = ""

    reader = PdfReader(file)

    for page in reader.pages:
        page_text = page.extract_text()

        if page_text:
            text += page_text + "\n"

    return text


def extract_from_docx(file):
    text = ""

    document = Document(file)

    for paragraph in document.paragraphs:
        text += paragraph.text + "\n"

    return text


def extract_resume_text(file):
    file_name = file.name.lower()

    if file_name.endswith(".pdf"):
        return extract_from_pdf(file)

    elif file_name.endswith(".docx"):
        return extract_from_docx(file)

    else:
        return ""