from flask import Blueprint, render_template, request, send_file
from pypdf import PdfMerger
import os
import uuid

pdf_bp = Blueprint("pdf", __name__)

UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "outputs"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)


@pdf_bp.route("/merge-pdf")
def merge_pdf():
    return render_template(
        "merge_pdf.html",
        active_page="pdf"
    )


@pdf_bp.route("/merge-pdf/run", methods=["POST"])
def merge_pdf_run():

    files = request.files.getlist("pdfs")

    merger = PdfMerger()

    for file in files:
        merger.append(file)

    filename = f"{uuid.uuid4().hex}.pdf"

    output_path = os.path.join(
        OUTPUT_FOLDER,
        filename
    )

    merger.write(output_path)
    merger.close()

    return send_file(
        output_path,
        as_attachment=True,
        download_name="Merged.pdf"
    )