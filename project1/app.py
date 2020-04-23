from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    s = 'xcvxcv'
    q = False
    w = ('qwe','asd','zxc')
    return render_template('index.html', s=s, q=q, w=w)

@app.route('/moarxcvxcv')
def more():
    return render_template('more.html')

@app.route('/<string:name>')
def name(name):
    return f'Hello {name}!'
