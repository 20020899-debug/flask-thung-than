from flask import Blueprint, render_template

pdf_bp = Blueprint("pdf", __name__)

@pdf_bp.route("/merge-pdf")
def merge_pdf():
    return render_template(
        "merge_pdf.html",
        active_page="pdf"
    )