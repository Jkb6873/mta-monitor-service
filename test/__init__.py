import pytest
import time
import json
from mock import MagicMock
from src import create_app
from src.delayTracker import tracker

@pytest.fixture(scope="module", autouse=True)
def client():
    tracker.start = MagicMock()
    app = create_app()
    with app.app_context():
        yield app.test_client()

@pytest.fixture(scope="function", autouse=True)
def setup_tracker():
    tracker.currently_delayed = set()
    tracker.trains = {}
    tracker.start_time = time.time()
    yield tracker
