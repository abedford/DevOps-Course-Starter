
""" Unit tests for app.py """
import pytest

from todo_app.data.viewmodel import *
from todo_app.data.task import *
from datetime import timedelta


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
    items = [Task(1, "1st Task", description = "1st Task to do", status = "To Do"),
    Task(2, "2nd Task", description = "2nd Task to do", status = "Doing"),
    Task(3, "3rd Task", description = "3rd Task to do", status = "Done")]
    viewmodel = ViewModel(items)
   
    result = viewmodel.get_done_items()

    assert result != None
    assert len(result) == 1
    assert result[0].id == 3

def test_can_get_just_todays_done_tasks():
    items = [Task(1, "1st Task", description = "1st Task to do", status = "To Do"),
     Task(2, "2nd Task", description = "2nd Task to do", status = "Doing"),
      Task(3, "3rd Task", description = "3rd Task to do", status = "Done")]
    viewmodel = ViewModel(items)
   
    result = viewmodel.get_recent_done_items()

    assert result != None
    assert len(result) < len(items)

def test_when_less_than_5_done_tasks_we_get_them_all():
    items = [Task(1, "1st Task", description = "1st Task to do", status = "Done"),
     Task(2, "2nd Task", description = "2nd Task to do", status = "Done"),
      Task(3, "3rd Task", description = "3rd Task to do", status = "Done")]
    timenow = datetime.datetime.now()
    onehourago = timenow.replace(hour=timenow.hour-1)
    fivehoursago = timenow.replace(hour=timenow.hour-5)
    onedayago = timenow.replace(day=timenow.day-1)
    items[0].modified_date = onehourago
    items[1].modified_date = fivehoursago
    items[2].modified_date = onedayago
    

    viewmodel = ViewModel(items)
   
    result = viewmodel.get_recent_done_items()

    assert result != None
    assert len(result) == 3


def test_when_more_than_5_done_tasks_we_only_get_recent_ones():
    items = [Task(1, "1st Task", description = "1st Task to do", status = "Done"), 
    Task(2, "2nd Task", description = "2nd Task to do", status = "Done"), 
    Task(3, "3rd Task", description = "3rd Task to do", status = "Done"),
    Task(4, "4th Task", description = "4th Task to do", status = "Done"), 
    Task(5, "5th Task", description = "5th Task to do", status = "Done"), 
    Task(6, "6th Task", description = "6th Task to do", status = "Done")]
    timenow = datetime.datetime.now()
    onehourago = timenow.replace(hour=timenow.hour-1)
    fivehoursago = timenow.replace(hour=timenow.hour-5)
    
    onedayago = timenow - timedelta(days=1)
    threedaysago = timenow - timedelta(days=3)
    fivedaysago = timenow - timedelta(days=5)
    sixdaysago = timenow - timedelta(days=6)
    items[0].modified_date = onehourago
    items[1].modified_date = fivehoursago
    items[2].modified_date = onedayago
    items[3].modified_date = threedaysago
    items[4].modified_date = fivedaysago
    items[5].modified_date = sixdaysago
    

    viewmodel = ViewModel(items)
   
    result = viewmodel.get_recent_done_items()

    assert result != None
    assert len(result) == 2
    assert result[0].id == 1
    assert result[1].id == 2

def test_can_get_older_completed_items():
    items = [Task(1, "1st Task", description = "1st Task to do", status = "Done"), 
    Task(2, "2nd Task", description = "2nd Task to do", status = "Done"), 
    Task(3, "3rd Task", description = "3rd Task to do", status = "Done"),
    Task(4, "4th Task", description = "4th Task to do", status = "Done"), 
    Task(5, "5th Task", description = "5th Task to do", status = "Done"), 
    Task(6, "6th Task", description = "6th Task to do", status = "Done")]
    timenow = datetime.datetime.now()
    onehourago = timenow.replace(hour=timenow.hour-1)
    fivehoursago = timenow.replace(hour=timenow.hour-5)
    
    onedayago = timenow - timedelta(days=1)
    threedaysago = timenow - timedelta(days=3)
    fivedaysago = timenow - timedelta(days=5)
    sixdaysago = timenow - timedelta(days=6)
    items[0].modified_date = onehourago
    items[1].modified_date = fivehoursago
    items[2].modified_date = onedayago
    items[3].modified_date = threedaysago
    items[4].modified_date = fivedaysago
    items[5].modified_date = sixdaysago
    

    viewmodel = ViewModel(items)
   
    result = viewmodel.get_older_done_items()

    assert result != None
    assert len(result) == 4
    assert result[0].id == 3
    assert result[1].id == 4


def test_when_more_than_5_recently_done_tasks_we_get_all_recently_done_tasks():
    items = [Task(1, "1st Task", description = "1st Task to do", status = "Done"), 
    Task(2, "2nd Task", description = "2nd Task to do", status = "Done"), 
    Task(3, "3rd Task", description = "3rd Task to do", status = "Done"),
    Task(4, "4th Task", description = "4th Task to do", status = "Done"), 
    Task(5, "5th Task", description = "5th Task to do", status = "Done"), 
    Task(6, "6th Task", description = "6th Task to do", status = "Done")]
    timenow = datetime.datetime.now()
    onehourago = timenow.replace(hour=timenow.hour-1)
    fivehoursago = timenow.replace(hour=timenow.hour-5)
    
    sixhoursago = timenow - timedelta(hours=6)
    twohoursago = timenow - timedelta(hours=2)
    sevenhoursago = timenow - timedelta(hours=7)
    threehoursago = timenow - timedelta(hours=3)
    items[0].modified_date = onehourago
    items[1].modified_date = fivehoursago
    items[2].modified_date = sixhoursago
    items[3].modified_date = twohoursago
    items[4].modified_date = sevenhoursago
    items[5].modified_date = threehoursago
    

    viewmodel = ViewModel(items)
    result = viewmodel.get_recent_done_items()

    assert result != None
    assert len(result) == 6
    assert result[0].id == 1
    assert result[1].id == 2
    assert result[5].id == 6
    
