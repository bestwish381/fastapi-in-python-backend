from fastapi import FastAPI, Query
from fastapi.responses import FileResponse
from PyPDF2 import PdfReader, PdfWriter
from PyPDF2.generic import AnnotationBuilder
import time


app = FastAPI()


@app.get("/")
def annotate(file_name: str = Query(...), pg_num: int = Query(None), con: str = Query(None), pos: str = Query(None)):
    pdf_path = f"./{file_name}"
    if pg_num is not None and con is not None and pos is not None:
        reader = PdfReader(pdf_path)
        writer = PdfWriter()
        for page in reader.pages:
            writer.add_page(page)
            # Create the annotation and add it to each page
            if reader.pages == pg_num:
                annotation = AnnotationBuilder.free_text(
                    {con},
                    rect=pos,
                    font="Arial",
                    bold=True,
                    italic=True,
                    font_size="20pt",
                    font_color="FF0000",
                    border_color="00FF00",
                    background_color="0000FF",
                )
                print(pos)
                writer.add_annotation(page_number=reader.pages.index(
                    page), annotation=annotation)

        timestamp = time.time()
        output_path = f"annotated_{file_name}_{timestamp}.pdf"
        with open(output_path, "wb") as fp:
            writer.write(fp)

        return FileResponse(output_path)

    else:
        reader = PdfReader(pdf_path)
        writer = PdfWriter()

        for page in reader.pages:
            writer.add_page(page)

        # Write the annotated file to disk
        output_path = f"annotated_{file_name}"
        with open(output_path, "wb") as fp:
            writer.write(fp)

        return FileResponse(output_path)
