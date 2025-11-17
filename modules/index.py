import flask
import secrets
from flask import Flask, request, jsonify, abort
from flask_socketio import SocketIO
import time
import threading
from queue import Queue
# from modules import camera
# from db import connection as conn


# from sensors import sensors

class MainIndex:


    def __init__(self):
        self.app = Flask(__name__)
        self.socket_io = SocketIO(self.app)
        self.app.config['JSON_SORT_KEYS'] = False 

        self.app.add_url_rule("/api/sensors", "sensors", self.sensor, methods=["POST"])
        # self.socket_io.on_event('connect', self.handle_connect)
        self.app.add_url_rule("/", "index", self.index)
        # self.app.add_url_rule(
        #         "/api/video", "video", self.video
        #     )
        # self.app.add_url_rule("/api/login", "api_key_login", self.api_key_login, methods=["POST"])
        # self.app.add_url_rule("/api/register", "api_register", self.api_register, methods=["POST"])


        self.all_data = {}
        self.data_queue = Queue()


    def run(self, host="0.0.0.0", port=5000):
        self.sender_thread = threading.Thread(target=self.send_data)
        self.sender_thread.daemon = True
        self.sender_thread.start()
       
        self.socket_io.run(self.app, host=host, port=port, debug=True)

    def index(self):
        return flask.render_template("index.html")

        

    def send_data(self):
        while True:
            data = self.data_queue.get()
            self.socket_io.emit('sensor_update', data)



    def sensor(self):
        # print(self.all_data)
        return jsonify(self.all_data)
    

    
        
   