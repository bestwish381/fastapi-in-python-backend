from PyPDF2 import PdfReader, PdfWriter
from PyPDF2.generic import AnnotationBuilder
import os
from fastapi import FastAPI
from fastapi.responses import FileResponse
# Fill the writer with the pages you want


app = FastAPI()



# Create the annotation and add it
@app.get("/")
def annotate():
    pdf_path = "2109.00813.pdf"
    reader = PdfReader(pdf_path)
    page = reader.pages[0]
    writer = PdfWriter()
    writer.add_page(page)
    annotation = AnnotationBuilder.free_text(
        "Hello World\nThis is the second line!",
        rect=(50, 550, 200, 650),
        font="Arial",
        bold=True,
        italic=True,
        font_size="20pt",
        font_color="00ff00",
        border_color="0000ff",
        background_color="ff0000",
    )
    writer.add_annotation(page_number=0, annotation=annotation)

    # Write the annotated file to disk
    output_path = "annotated.pdf"
    with open(output_path, "wb") as fp:
        writer.write(fp)

    return FileResponse(output_path)