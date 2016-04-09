from .config import config

def main():
    print(config["Celery"]["broker"])
