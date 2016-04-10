from .config import config
from celery import Celery

celery_broker = config["Celery"]["broker"]
celery_backend = config["Celery"]["backend"]
app = Celery("worker", broker=celery_broker, backend=celery_backend)

@app.task
def add(x, y):
    import time
    time.sleep(5)
    return x+y
