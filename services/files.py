import os
import shutil

from fastapi import UploadFile
from fpdf import FPDF


async def add_file(file: UploadFile | None):
    if file:
        name_dir = "image" if file.content_type.startswith("image/") else "other_file"
        os.makedirs(f"upload_files/{name_dir}", exist_ok=True)
        file_location = f"upload_files/{name_dir}/{name_dir}_{file.filename}"
        with open(file_location, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        return file_location
    return None


def generate_simple_report(
    filename: str, report_title: str, content_lines: list[str]
) -> str:
    pdf = FPDF()
    pdf.add_page()

    pdf.add_font("Tinos-regular", "", "/app/fonts/Tinos-Regular.ttf")
    pdf.add_font("Tinos-bold", "", "/app/fonts/Tinos-Bold.ttf")

    pdf.set_font("Tinos-bold", size=16)

    pdf.cell(0, 10, report_title, ln=True, align="C")

    pdf.ln(10)

    pdf.set_font("Tinos-regular", size=12)

    for line in content_lines:
        pdf.multi_cell(0, 10, line, ln=True)
        pdf.ln(4)

    filepath = f"./{filename}"
    pdf.output(filepath)

    return filepath
