from src.routes import api
from src.delayTracker import tracker
from config import VALID_TRAINS
from flask import request

@api.route('/uptime', methods=['GET'])
def uptime():
    line = request.args.get('line')
    if not line or line.upper() not in VALID_TRAINS:
        return {'error': 'Invalid subway line'}, 400
    uptime = tracker.uptime(line.upper())
    return {'uptime': round(uptime, 2)}, 200

@api.route('/status', methods=['GET'])
def status():
    line = request.args.get('line')
    if not line or line.upper() not in VALID_TRAINS:
        return {'error': 'Invalid subway line'}, 400
    status = tracker.status(line.upper())
    return {'status': 'delayed' if status else 'not delayed'}, 200
