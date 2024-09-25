import pytest
from unittest.mock import patch, MagicMock
from insuranceapi import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_home_page(client):
    """Test the home page."""
    response = client.get('/')
    assert response.status_code == 200
    assert response.data.startswith(b'<!DOCTYPE html>')

@patch('app.mongo.db.policies')
def test_get_all_policies(mock_policies, client):
    """Test retrieving all policies."""
    mock_policies.find.return_value = [
        {'_id': '1', 'policy_number': 'P001', 'policy_holder_name': 'John Doe', 'premium_amount': 100, 'status': 'active'},
        {'_id': '2', 'policy_number': 'P002', 'policy_holder_name': 'Jane Smith', 'premium_amount': 200, 'status': 'inactive'},
    ]

    response = client.get('/api/policies')
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 2
    assert data[0]['policy_number'] == 'P001'
    assert data[1]['policy_holder_name'] == 'Jane Smith'

@patch('app.mongo.db.policies')
def test_search_policy(mock_policies, client):
    """Test searching for a policy."""
    mock_policies.find.return_value = [
        {'_id': '1', 'policy_number': 'P001', 'policy_holder_name': 'John Doe', 'premium_amount': 100, 'status': 'active'},
    ]

    response = client.get('/api/policies/search?policy_number=P001')
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 1
    assert data[0]['policy_number'] == 'P001'

@patch('app.mongo.db.policies')
def test_get_policy_by_number(mock_policies, client):
    """Test retrieving a policy by number."""
    mock_policies.find_one.return_value = {'_id': '1', 'policy_number': 'P001', 'policy_holder_name': 'John Doe', 'premium_amount': 100, 'status': 'active'}

    response = client.get('/api/policies/P001')
    assert response.status_code == 200
    data = response.get_json()
    assert data['policy_number'] == 'P001'

@patch('app.mongo.db.policies')
def test_get_policy_not_found(mock_policies, client):
    """Test retrieving a policy that does not exist."""
    mock_policies.find_one.return_value = None

    response = client.get('/api/policies/INVALID_POLICY_NUMBER')
    assert response.status_code == 404
    data = response.get_json()
    assert data['message'] == 'Policy not found'

@patch('app.mongo.db.policies')
def test_get_all_policies_db_error(mock_policies, client):
    """Test handling database errors when getting all policies."""
    mock_policies.find.side_effect = Exception("Database error")

    response = client.get('/api/policies')
    assert response.status_code == 500
    data = response.get_json()
    assert data['error'] == 'Database error occurred'

@patch('app.mongo.db.policies')
def test_search_policy_db_error(mock_policies, client):
    """Test handling database errors when searching for a policy."""
    mock_policies.find.side_effect = Exception("Database error")

    response = client.get('/api/policies/search?policy_number=P001')
    assert response.status_code == 500
    data = response.get_json()
    assert data['error'] == 'Database error occurred'

@patch('app.mongo.db.policies')
def test_get_policy_by_number_db_error(mock_policies, client):
    """Test handling database errors when getting a policy by number."""
    mock_policies.find_one.side_effect = Exception("Database error")

    response = client.get('/api/policies/P001')
    assert response.status_code == 500
    data = response.get_json()
    assert data['error'] == 'Database error occurred'
