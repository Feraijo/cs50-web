import os
import requests

from flask import Flask, jsonify, render_template, request
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
socketio = SocketIO(app)

channels = {'ch0':'Default channel', 'ch1':"Channel 1"}

@app.route("/")
def index():
    return render_template('index.html', channels=channels)
