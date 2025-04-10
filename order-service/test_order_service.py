import pytest
from unittest.mock import patch, MagicMock

from order_service import app

@pytest.fixture
def client():
    app.testing = True
    with app.test_client() as client:
        yield client

def test_homepage(client):
    response = client.get("/orders")
    assert response.status_code == 200
    assert response.get_json() == {'message': 'Welcome to order service'}

@patch("order_service.session")
def test_create_order(mock_session, client):
    mock_order = {
        'id': 'order123',
        'item': 'Laptop',
        'quantity': 1,
        'user_id': 'user456'
    }

    response = client.post("/orders", json=mock_order)
    
    assert response.status_code == 201
    assert response.get_json() == {'message': 'Order created'}

    # Ensure session.merge and commit were called
    assert mock_session.merge.called
    assert mock_session.commit.called

@patch("order_service.session")
def test_get_order_not_found(mock_session, client):
    mock_session.get.return_value = None

    response = client.get("/orders/nonexistent")
    assert response.status_code == 404
    assert response.get_json() == {'error': 'Order not found'}