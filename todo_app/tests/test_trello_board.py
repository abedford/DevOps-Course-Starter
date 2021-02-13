
from dotenv.main import find_dotenv, load_dotenv
from todo_app.data.trello_board import TrelloBoard


import pytest
import os

def test_can_create_and_delete_a_trello_board():
    file_path = find_dotenv('.env')
    load_dotenv(file_path, override=True)
    api_key = os.getenv('API_KEY')
    server_token = os.getenv('SERVER_TOKEN')

    trello_board_id = TrelloBoard.create_new_board(api_key, server_token, "Test board")
    assert trello_board_id is not None

    assert TrelloBoard.delete_board(api_key, server_token, trello_board_id)



