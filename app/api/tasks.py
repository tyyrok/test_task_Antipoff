import time
import random
import requests
import asyncio

from celery import shared_task
from asgiref.sync import async_to_sync

from api.models import CadastralNumber

@shared_task
def mock_request_to_third_party(obj_id: int):
    """Mock function that emulates delay in request to third-party server"""
    r = random.randrange(1, 60)
    time.sleep(r)
    try:
        obj = CadastralNumber.objects.get(id=obj_id)
        status = random.choice([True, False])
        obj.status = status
        obj.save()
    except CadastralNumber.DoesNotExist:
        pass
    
@shared_task
def make_third_party_request(obj_id: int):
    """Function that makes post request to third-party server"""
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
            try:
                obj = CadastralNumber.objects.get(id=obj_id)
                obj.status = data['result']
                obj.save()
            except CadastralNumber.DoesNotExist:
                pass
    else:
        print("Content ", r.content)