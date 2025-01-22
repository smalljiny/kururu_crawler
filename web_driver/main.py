from flask import Flask, send_from_directory, jsonify, request
from flask_socketio import SocketIO, emit
from seleniumwire import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

import ssl

"""
selenium 초기화
"""
def init_selenium():
    ssl._create_default_https_context = ssl._create_unverified_context
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)
    chrome_options.add_argument("User-Agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36")
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    service = Service(executable_path="../chromedriver-mac-arm64/chromedriver")
    
    options = {
        'request_storage_base_dir': '/Users/jinchuljung/Workspace/kimg/kururu_crawler/web_driver/temp',  # .seleniumwire will get created here
        'exclude_hosts': ['google-analytics.com', 'update.googleapis.com', 'optimizationguide-pa.googleapis.com', 'edgedl.me.gvt1.com', 'accounts.google.com']
    }
    
    driver = webdriver.Chrome(service=service, options=chrome_options, seleniumwire_options=options)
    
    return driver

driver = init_selenium()

"""
Web Server initialize
"""
app = Flask(__name__, static_folder='public')
socketio = SocketIO(app)

"""
Static File Serve
"""
@app.route('/')
def serve_index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/favicon.ico')
def serve_favicon():
    return send_from_directory(app.static_folder, 'favicon.ico')

@socketio.on('test')
def test(data):
    
    emit('test', data)

if __name__ == '__main__':
    socketio.run(app, port=9001, host='0.0.0.0')