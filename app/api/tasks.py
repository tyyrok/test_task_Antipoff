import time
import requests
import random

from celery import shared_task

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
def make_third_party_request():
    pass
    