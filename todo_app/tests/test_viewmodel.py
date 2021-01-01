#just the ‘to do’ items
#just the ‘doing’ items
#just the ‘done’ items


"""Integration tests for app.py"""
import pytest

from todo_app.data.viewmodel import *
from todo_app.data.task import *





def test_can_get_to_do_tasks():
    items = [Task(1, "1st Task", description = "1st Task to do", status = "To Do"), Task(2, "2nd Task", description = "2nd Task to do", status = "Doing"), Task(3, "3rd Task", description = "3rd Task to do", status = "Done")]
    viewmodel = ViewModel(items)
   
    result = viewmodel.get_to_do_items()

    assert result != None
    assert len(result) == 1
    assert result[0].id == 1

def test_can_get_doing_tasks():
    items = [Task(1, "1st Task", description = "1st Task to do", status = "To Do"), Task(2, "2nd Task", description = "2nd Task to do", status = "Doing"), Task(3, "3rd Task", description = "3rd Task to do", status = "Done")]
    viewmodel = ViewModel(items)
   
    result = viewmodel.get_doing_items()

    assert result != None
    assert len(result) == 1
    assert result[0].id == 2

def test_can_get_done_tasks():
    items = [Task(1, "1st Task", description = "1st Task to do", status = "To Do"), Task(2, "2nd Task", description = "2nd Task to do", status = "Doing"), Task(3, "3rd Task", description = "3rd Task to do", status = "Done")]
    viewmodel = ViewModel(items)
   
    result = viewmodel.get_done_items()

    assert result != None
    assert len(result) == 1
    assert result[0].id == 3
    
