import os
from fastapi.testclient import TestClient
from app.main import app, parse_command

client = TestClient(app)

def test_health():
    data = client.get('/api/health').json()
    assert data['status'] == 'healthy'
    assert data['mode'] == 'simulation'

def test_intent_routing():
    assert parse_command('Buy milk tomorrow')['item']['category'] == 'grocery'
    assert parse_command('Turn on the light')['intent'] == 'device'
    assert parse_command('help me')['intent'] == 'emergency'

def test_item_lifecycle():
    item = client.post('/api/items', json={'title':'Test task','category':'task','priority':'low'}).json()
    assert item['title'] == 'Test task'
    assert client.patch('/api/items/'+item['id']).json()['completed'] is True
    assert client.delete('/api/items/'+item['id']).status_code == 204

