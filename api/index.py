from flask import Flask,request
#from gradio_client import Client

app = Flask(__name__)

@app.route('/')
def home():
    return 'Hello, World!'

@app.route('/generate')
def about():  
    return 'Hello, World!'


@app.route('/roop', methods = ['GET','POST'])
def roop():
    return 'Hello, World!'
    
@app.route('/test')
def tst():
    return 'testlog123'