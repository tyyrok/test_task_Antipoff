import pytest
import json

from django.urls import reverse

from api.models import CadastralNumber

#pytestmark = pytest.mark.django_db

@pytest.fixture
def api_client():
    from rest_framework.test import APIClient
    return APIClient()

# Use this fixture wherever non-rollback database access is required.
@pytest.fixture
def db_no_rollback(request, django_db_setup, django_db_blocker):
    django_db_blocker.unblock()
    request.addfinalizer(django_db_blocker.restore)

@pytest.mark.django_db(transaction=False)
def test_ping_request(api_client):
    url = '/ping/'
    res = api_client.get(url)
    assert res.status_code == 200
    assert json.loads(res.content) == {'data': 'pong'}

@pytest.mark.django_db(transaction=False)
def test_query_incorrect_number_request(api_client):
    url = '/query/'
    data = {
        "number": "56:8230000:09",
        "long": "41.30212",
        "alt": "544.22312"
    }
    res = api_client.post(
        url, 
        json.dumps(data), 
        content_type='application/json'
    )
    assert res.status_code == 400

@pytest.mark.django_db(transaction=False)
def test_query_incorrect_alt_request(api_client):
    url = '/query/'
    data = {
        "number": "56:10:8230000:09",
        "long": "41.30212",
        "alt": "5442312"
    }
    res = api_client.post(
        url, 
        json.dumps(data), 
        content_type='application/json'
    )
    assert res.status_code == 400

@pytest.mark.django_db
def test_query_incorrect_long_request(api_client):
    url = '/query/'
    data = {
        "number": "56:10:8230000:09",
        "long": "410212",
        "alt": "544.22312"
    }
    res = api_client.post(
        url, 
        json.dumps(data), 
        content_type='application/json'
    )
    assert res.status_code == 400

def test_query_correct_request(db_no_rollback, api_client):
    url = '/query/'
    data = {
        "number": "56:10:8230000:09",
        "long": "41.30212",
        "alt": "544.22312"
    }
    res = api_client.post(
        url, 
        json.dumps(data), 
        content_type='application/json'
    )
    assert res.status_code == 201
    assert "number" in json.loads(res.content)
    assert "status" in json.loads(res.content)
    number = CadastralNumber.objects.filter(number=data['number'])[0]
    assert number
    
@pytest.mark.django_db
def test_incorrect_result_request(db_no_rollback, api_client):
    data = {
        "number": "56:10:0000000:09",
    }
    url = f"/result/{data['number']}/"

    res = api_client.get(url)
    assert res.status_code == 400
    assert json.loads(res.content) == \
        {'detail': 'Incorrect number of the object'}
    
def test_correct_result_request(db_no_rollback, api_client):
    data = {
        "number": "56:10:8230000:09",
    }
    url = f"/result/{data['number']}/"

    res = api_client.get(url)
    assert res.status_code == 200
    assert "number" in json.loads(res.content)
    assert "status" in json.loads(res.content)
    
def test_correct_history_request(db_no_rollback, api_client):
    data = {
        "number": "56:10:8230000:09",
    }
    url = f"/history/{data['number']}/"

    res = api_client.get(url)
    assert res.status_code == 200
    assert "number" in json.loads(res.content)
    assert "history_set" in json.loads(res.content)
    assert "request_type" in json.loads(res.content)['history_set'][0]

@pytest.mark.django_db
def test_incorrect_history_request(api_client):
    data = {
        "number": "56:108230000:09",
    }
    url = f"/history/{data['number']}/"

    res = api_client.get(url)
    assert res.status_code == 400
    assert json.loads(res.content) == \
        {'detail': 'Incorrect number of the object'}