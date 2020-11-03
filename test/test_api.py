import time
from . import client
from src.delayTracker import tracker
from mock import MagicMock
from config import VALID_TRAINS

def test_uptime_invalid_line(client):
    res = client.get('/uptime', query_string = {'line': 'P'})
    assert 'P' not in VALID_TRAINS
    assert res.status_code == 400
    assert res.json == {'error': 'Invalid subway line'}


def test_uptime_valid_line_not_seen_before(client):
    assert 'A' in VALID_TRAINS
    assert 'A' not in tracker.trains
    assert 'A' not in tracker.currently_delayed
    res = client.get('/uptime', query_string = {'line': 'A'})
    assert res.status_code == 200
    assert res.json == {'uptime': 1}

def test_uptime_valid_line_currently_delayed(client):
    tracker.start_time = time.time() - 20
    tracker.trains = {'A': {
        'id': 'A',
        'total_time_delayed': 0,
        'delayed_since': time.time() - 10
    }}
    tracker.currently_delayed = set(['A'])
    res = client.get('/uptime', query_string = {'line': 'A'})
    assert res.status_code == 200
    assert res.json == {'uptime': .5}

def test_uptime_valid_line_currently_and_previously_delayed(client):
    tracker.start_time = time.time() - 100
    tracker.trains = {'A': {
        'id': 'A',
        'total_time_delayed': 20,
        'delayed_since': time.time() - 10
    }}
    tracker.currently_delayed = set(['A'])
    res = client.get('/uptime', query_string = {'line': 'A'})
    assert res.status_code == 200
    assert res.json == {'uptime': .7}

def test_uptime_valid_line_not_currently_delayed(client):
    tracker.start_time = time.time() - 100
    tracker.trains = {'A': {
        'id': 'A',
        'total_time_delayed': 20,
        'delayed_since': None
    }}
    tracker.currently_delayed = set()
    res = client.get('/uptime', query_string = {'line': 'A'})
    assert res.status_code == 200
    assert res.json == {'uptime': .8}

def test_status_invalid_line(client):
    res = client.get('/status', query_string = {'line': 'P'})
    assert 'P' not in VALID_TRAINS
    assert res.status_code == 400
    assert res.json == {'error': 'Invalid subway line'}

def test_status_valid_line_currently_delayed(client):
    tracker.currently_delayed = set(['A'])
    res = client.get('/status', query_string = {'line': 'A'})
    assert res.status_code == 200
    assert res.json == {'status': 'delayed'}

def test_status_valid_line_not_currently_delayed(client):
    tracker.currently_delayed = set()
    res = client.get('/status', query_string = {'line': 'A'})
    assert res.status_code == 200
    assert res.json == {'status': 'not delayed'}
