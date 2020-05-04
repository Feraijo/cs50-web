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

for i in range(3):
    m = Message(f'sdfsdf {i}', 'Eli', '30.04.2020, 17:41:23')
    chans[0].add_message(m)
m = Message(f'sdfsdfxcvxcvxv', 'Varajo', '30.04.2020, 17:42:53')
chans[0].add_message(m)

def get_chat_by_id(iid):
    return [ch for ch in chans if ch.id == iid][0]

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
    emit("history", get_chat_by_id(iid).get_history())

@socketio.on("new message")
def new_message(data):
    name = data["name"]
    text = data["text"]
    timestamp = data["timestamp"]
    m = Message(text, name, timestamp)
    iid = data["id"]
    chat = get_chat_by_id(iid)
    chat.add_message(m)
    emit("chat", [iid, str(m)], broadcast=True)    

@socketio.on("remove msg")
def rem_msg(data):
    chat_id = data["chat_id"]
    msg_id = data["msg_id"]    
    chat = get_chat_by_id(chat_id)    
    msg = chat.get_msg_by_id(msg_id)
    chat.delete_message(msg)
    emit("deleted msg", [chat_id, msg_id], broadcast=True)
