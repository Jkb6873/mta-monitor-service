import requests
import time
from src.delayTracker import tracker
from . import setup_tracker
from mock import MagicMock
from test.sample_gtfs import SAMPLE

def test_given_feed_find_delays(setup_tracker):
    tracker.feed.ParseFromString(SAMPLE)
    output = tracker.filter_feed_for_delays()
    assert len(output) == 2
    assert 'C' in output
    assert 'E' in output

def test_given_feed_update_current_delays_and_trains(setup_tracker):
    requests.get = MagicMock(return_value=MockResponse(SAMPLE))
    tracker.update()
    assert len(tracker.currently_delayed) == 2
    assert 'C' in tracker.currently_delayed
    assert 'E' in tracker.currently_delayed
    assert len(tracker.trains) == 2
    assert 'C' in tracker.trains
    assert 'E' in tracker.trains
    assert time.time() - tracker.trains['C']['delayed_since'] < 2
    assert time.time() - tracker.trains['E']['delayed_since'] < 2
    assert tracker.trains['C']['total_time_delayed'] == 0
    assert tracker.trains['E']['total_time_delayed'] == 0

class MockResponse():
    def __init__(self, content):
        self.content = content
