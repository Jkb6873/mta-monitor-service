from flask import Flask
from src.routes.controller import api
from src.delayTracker import tracker

def create_app():
    app = Flask(__name__)
    app.register_blueprint(api)
    tracker.start()
    return app
