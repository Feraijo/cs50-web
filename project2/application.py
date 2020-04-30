import os
import requests

from flask import Flask, jsonify, render_template, request
from flask_socketio import SocketIO, emit
from helpers import *

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
socketio = SocketIO(app)

names = ['Default channel', 'Chan1']
chans = [Chat(n) for n in names]

for i in range(123):
    m = Message(f'sdfsdf {i}', 'Eli')
    chans[0].add_message(m)



def get_channel_names():
    return {ch.id: ch.name for ch in chans}

@app.route("/")
def index():
    return render_template('index.html')

@socketio.on("get_chans")
def emit_channels():
    emit("channel list", get_channel_names(), broadcast=True)

@socketio.on("add channel")
def add_channel(data):
    name = data["name"]
    if name not in names:           
        names.append(name)
        chans.append(Chat(name))
    emit("channel list", get_channel_names(), broadcast=True)

@socketio.on('load_history')
def load_history(data):
    iid = data["id"]
    hist = [list(ch.history) for ch in chans if ch.id == iid][0]
    emit("history", [iid, hist], broadcast=True)

@socketio.on("new message")
def new_message():
    name = data["name"]
    text = data["text"]
    m = Message(text, name)
    #emit("chat", get_channels(names), broadcast=True)




