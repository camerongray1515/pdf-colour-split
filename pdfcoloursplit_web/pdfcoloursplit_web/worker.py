import pdfcoloursplit
import os
from .config import config
from celery import Celery

celery_broker = config["Celery"]["broker"]
celery_backend = config["Celery"]["backend"]
app = Celery("worker", broker=celery_broker, backend=celery_backend)

@app.task
def split_pdf(temp_dir, pdf_filename, duplex, stackable):
    os.chdir(temp_dir)
    files_written = pdfcoloursplit.split_pdf(pdf_filename, duplex, stackable)

    if pdf_filename.lower().endswith(".pdf"):
        zip_filename = pdf_filename[:-4] + ".zip"
    else:
        zip_filename = pdf_filename + ".zip"
    # Create zip file here

    return zip_filename
