import pytest
from Flask import app
from flask import json

"""
plik z testami wystawionego API, 
ułożenie szachownicy jest takie jak na początku standardowej rozgrywki
"""

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_running(client):
    response = client.get("/")
    assert response.data == b'<p>Hello, world!</p>'

def test_figure_moves(client):
    response = client.get('/api/v1/rook/a1')
    data = json.loads(response.data.decode('utf-8'))
    assert response.status_code == 200
    assert 'availableMoves' in data
    assert 'error' in data and data['error'] == 'None'

def test_invalid_move(client):
    response = client.get('/api/v1/pawn/a2/a5')
    data = json.loads(response.data.decode('utf-8'))
    assert data['error'] == 'Current move is not permitted'

def test_invalid_field(client):
    response = client.get('/api/v1/queen/c10')
    data = json.loads(response.data.decode('utf-8'))
    assert response.status_code == 409
    assert data['error'] == 'Field does not exist'

def test_figure_on_field(client):
    response = client.get('/api/v1/queen/a1')
    data = json.loads(response.data.decode('utf-8'))
    assert response.status_code == 404
    assert data['error'] == 'There is no such piece here'