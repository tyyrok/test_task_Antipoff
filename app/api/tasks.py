import time
import random
import requests
import asyncio

from celery import shared_task
from asgiref.sync import async_to_sync

from api.models import CadastralNumber

@shared_task
def mock_request_to_third_party(obj_id):
    r = random.randrange(1, 60)
    time.sleep(r)
    obj = CadastralNumber.objects.get(id=obj_id)
    status = random.choice([True, False])
    obj.status = status
    obj.save()
    
@shared_task
def make_third_party_request(obj_id):
    r = requests.post('http://antipoff-fastapi-1:8001/api/', 
                      json={"number": str(obj_id)},
                      headers={"Content-Type": "application/json"}
    )
    if r.status_code == 200:
        try:
            data = r.json()
        except requests.exceptions.JSONDecodeError:
            pass
        if 'result' in data:
            obj = CadastralNumber.objects.get(id=obj_id)
            obj.status = data['result']
            obj.save()
    else:
        print("Content ", r.content)