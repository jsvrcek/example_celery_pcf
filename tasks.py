from celery import Celery
import os
import json

BROKER_URL = None
if os.getenv("VCAP_SERVICES"):
    for service, listings in json.loads(os.getenv("VCAP_SERVICES")).items():
        try:
            if "rabbitmq" in service:
                BROKER_URL = listings[0]["credentials"]["protocols"]["amqp"]["uri"]
            if "cloudamqp" in service:
                BROKER_URL = listings[0]["credentials"]["uri"]
        except KeyError as TypeError:
            continue
        if BROKER_URL:
            break
if not BROKER_URL:
    BROKER_URL = os.environ.get("BROKER_URL", "amqp://guest:guest@localhost:5672//")
app = Celery('tasks', broker=BROKER_URL)

@app.task
def add(x, y):
    print("tasks output: " + str(x + y))
    return x + y
