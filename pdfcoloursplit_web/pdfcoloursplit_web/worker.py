import pdfcoloursplit
import os
import zipfile
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

    with zipfile.ZipFile(zip_filename, "w") as z:
        for filename in files_written:
            z.write(filename)

    return zip_filename
