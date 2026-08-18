from pypdf import PdfReader
import io


def extract_text_from_pdf(uploaded_file) -> str:
    """
    Extracts all text from an uploaded PDF file (Streamlit UploadedFile object).
    Returns the combined text from all pages.
    """
    pdf_bytes = uploaded_file.read()
    reader = PdfReader(io.BytesIO(pdf_bytes))

    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"

    return text.strip()