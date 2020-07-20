from apscheduler.schedulers.background import BackgroundScheduler
from random import random
import requests
import math


URL = 'http://localhost:8000/api/medicion'

def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(createMeasures, 'interval', minutes=0.5)
    scheduler.start()

def createMeasures():
    data = []
    for s in range(1,11):
        nivel = 30 * random()
        data.append({
            'id_sensor': s,
            'nivel_agua': truncate(nivel,2)
        })
    try:
        r = requests.post(URL,json=data)
    except Exception as e:
        print(e)

def truncate(number, digits) -> float:
    stepper = 10.0 ** digits
    return math.trunc(stepper * number) / stepper
