import os

MTA_API_KEY = os.environ.get("MTA_API_KEY")
MTA_URL = "https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/camsys%2Fsubway-alerts"
PERIOD = 10
VALID_TRAINS = [
    'A', 'C', 'E',
    'B', 'D', 'F', 'M',
    'G',
    'J', 'Z',
    'N', 'Q', 'R', 'W',
    'L',
    '1', '2', '3', '4', '5', '6',
    '7',
    'SI'
]
