from todo_app.app import *
from dotenv.main import find_dotenv, load_dotenv


import pytest
from unittest.mock import patch, Mock
import os


add_card_data = {'title': 'new card', 'description': 'new card desc', 'duedate': '2020-12-31T00:00:00.000Z'}

@pytest.fixture
def client():
    # Use our test integration config instead of the 'real' version
    file_path = find_dotenv('.env.test')
    load_dotenv(file_path, override=True)
    board_id = os.getenv('BOARD_ID')
    api_key = os.getenv('API_KEY')
    server_token = os.getenv('SERVER_TOKEN')
    trello_board = TrelloBoard(board_id = board_id, api_key = api_key, server_token = server_token, name=None)

    # Create the new app.
    test_app = create_app(trello_board)
    # Use the app to create a test_client that can be used in our tests.
    with test_app.test_client() as client:
        yield client

@patch('requests.get')
def test_index_page(mock_get_requests, client):
    mock_get_requests.side_effect = mock_get_cards
    response = client.get('/')

    assert response.status_code == 200

    string = response.data.decode('utf-8')
    assert "Todo name" in string
    assert "Todo name 2" in string
    assert "Todo name 3" in string

@patch('requests.get')
@patch('requests.post')
def test_add_task(mock_post_requests, mock_get_requests, client):
    mock_get_requests.side_effect = mock_get_lists
    mock_post_requests.side_effect = mock_add_card

    response = client.post('/items/add', data=add_card_data)

    assert response.status_code == 302

@patch('requests.get')
@patch('requests.put')
def test_complete_task(mock_put_requests, mock_get_requests, client):
    mock_get_requests.side_effect = mock_get_lists
    mock_put_requests.side_effect = mock_complete_card
    
    data = {'id': 'f1'}
    response = client.post('/items/complete', data=data)

    assert response.status_code == 302

    
@patch('requests.delete')
def test_remove_task(mock_post_requests, client):

    mock_post_requests.side_effect = mock_delete_card

    data = {'id': 'f1'}
    response = client.post('/items/remove', data=data)

    assert response.status_code == 302


@patch('requests.get')
@patch('requests.put')
def test_start_task(mock_put_requests, mock_get_requests, client):
    mock_get_requests.side_effect = mock_get_lists
    mock_put_requests.side_effect = mock_start_card
    
    data = {'id': 'f1'}
    response = client.post('/items/start', data=data)

    assert response.status_code == 302
 

@patch('requests.get')
@patch('requests.put')
def test_restart_task(mock_put_requests, mock_get_requests, client):
    mock_get_requests.side_effect = mock_get_lists
    mock_put_requests.side_effect = mock_restart_card

    data = {'id': 'f1'}
    response = client.post('/items/restart', data=data)

    assert response.status_code == 302

def mock_add_card(url):
    api_key = os.getenv('API_KEY')
    server_token = os.getenv('SERVER_TOKEN')
    if url ==  f"https://api.trello.com/1/cards?key={api_key}&token={server_token}&name={add_card_data['title']}&desc={add_card_data['description']}&due={add_card_data['duedate']}&idList=l1":
        response = Mock(ok=True)
        response.status_code = 200
        response.json.return_value = sample_trello_cards_response
        return response

def mock_delete_card(url):
    api_key = os.getenv('API_KEY')
    server_token = os.getenv('SERVER_TOKEN')
    if url ==  f"https://api.trello.com/1/cards/f1?key={api_key}&token={server_token}":
        response = Mock(ok=True)
        response.status_code = 200
        response.json.return_value = sample_trello_cards_response
        return response

def mock_delete_board(url):
    api_key = os.getenv('API_KEY')
    server_token = os.getenv('SERVER_TOKEN')
    if url ==  f"https://api.trello.com/1/boards/b1?key={api_key}&token={server_token}":
        response = Mock(ok=True)
        response.status_code = 400
        response.json.return_value = None
        return response

def mock_get_lists(url):
    api_key = os.getenv('API_KEY')
    server_token = os.getenv('SERVER_TOKEN')
    board_id = os.getenv('BOARD_ID')
    
    if url ==  f"https://api.trello.com/1/boards/{board_id}/lists?key={api_key}&token={server_token}":
        response = Mock(ok=True)
        response.status_code = 200
        response.json.return_value = sample_trello_lists_response
        return response

def mock_start_card(url):
    api_key = os.getenv('API_KEY')
    server_token = os.getenv('SERVER_TOKEN')
    
    if url == f"https://api.trello.com/1/cards/f1?key={api_key}&token={server_token}&idList=l2":
        response = Mock(ok=True)
        response.status_code = 200
        return response

def mock_restart_card(url):
    api_key = os.getenv('API_KEY')
    server_token = os.getenv('SERVER_TOKEN')
    
    if url == f"https://api.trello.com/1/cards/f1?key={api_key}&token={server_token}&idList=l1":
        response = Mock(ok=True)
        response.status_code = 200
        return response

def mock_complete_card(url):
    api_key = os.getenv('API_KEY')
    server_token = os.getenv('SERVER_TOKEN')
    
    if url == f"https://api.trello.com/1/cards/f1?key={api_key}&token={server_token}&idList=l3":
        response = Mock(ok=True)
        response.status_code = 200
        return response

def mock_get_cards(url):
    board_id = os.getenv('BOARD_ID')
    api_key = os.getenv('API_KEY')
    server_token = os.getenv('SERVER_TOKEN')
    if url == f"https://api.trello.com/1/boards/{board_id}/cards?key={api_key}&token={server_token}":
        response = Mock(ok=True)
        response.status_code = 200
        response.json.return_value = sample_trello_cards_response
        return response
    if url == f"https://api.trello.com/1/cards/f1/list?key={api_key}&token={server_token}":
        response = Mock(ok=True)
        response.status_code = 200
        response.json.return_value = sample_trello_list_l1_response
        return response
    if url == f"https://api.trello.com/1/cards/f2/list?key={api_key}&token={server_token}":
        response = Mock(ok=True)
        response.status_code = 200
        response.json.return_value = sample_trello_list_l2_response
        return response
    if url == f"https://api.trello.com/1/cards/f3/list?key={api_key}&token={server_token}":
        response = Mock(ok=True)
        response.status_code = 200
        response.json.return_value = sample_trello_list_l3_response
        return response

sample_trello_lists_response = [
    {   "name": "To Do",
        "id": "l1"
    },
    {
        "name": "Doing",
        "id": "l2"
    }, 
    {
        "name": "Done",
        "id": "l3"
    }

]
sample_trello_cards_response = [
    {
        "name": "Todo name",
        "id": "f1",
        "desc": "Todo description",
        "list_id": "l1",
        "due": "2020-12-31T00:00:00.000Z",
        "dateLastActivity": "2021-01-03T10:11:02.051Z"
    },
    {
        "name": "Todo name 2",
        "id": "f3",
        "desc": "Todo description",
        "list_id": "l2",
        "due": "2020-12-31T00:00:00.000Z",
        "dateLastActivity": "2021-01-03T10:11:02.051Z"
    },
    {
        "name": "Todo name 3",
        "id": "f3",
        "desc": "Todo description",
        "list_id": "l3",
        "due": "2020-12-31T00:00:00.000Z",
        "dateLastActivity": "2021-01-03T10:11:02.051Z"
    }
]

sample_trello_list_l1_response = {
    "name": "Todo",
    "id": "L1",
    
}

sample_trello_list_l2_response = {
    "name": "Doing",
    "id": "l2",
        
}

sample_trello_list_l3_response = {
    "name": "Done",
    "id": "l3",
        
}
