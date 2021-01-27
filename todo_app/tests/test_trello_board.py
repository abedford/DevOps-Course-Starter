from todo_app.app import *
from dotenv.main import find_dotenv, load_dotenv


import pytest
import os

def test_can_create_and_delete_a_trello_board():
    file_path = find_dotenv('.env')
    load_dotenv(file_path, override=True)
    api_key = os.getenv('API_KEY')
    server_token = os.getenv('SERVER_TOKEN')
 
    print(f"the api key is {api_key}")
    print(f"The server token is {server_token}")


    trello_board = TrelloBoard(board_id = None, api_key = api_key, server_token = server_token, name="Test board")
    assert trello_board.board_id is not None

    assert trello_board.delete_board(trello_board.board_id)

def test_error_shown_if_creating_trello_board_with_id_and_name():
    
    api_key = os.getenv('API_KEY')
    server_token = os.getenv('SERVER_TOKEN')
 
    print(f"the api key is {api_key}")
    print(f"The server token is {server_token}")


    trello_board = TrelloBoard(board_id = "test_id", api_key = api_key, server_token = server_token, name="Test board")
    assert trello_board.board_id == "test_id"



