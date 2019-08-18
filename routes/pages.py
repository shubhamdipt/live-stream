#!/usr/bin/env python
from flask import Flask, render_template, Response
from application import app, basic_auth
from routes.utils import get_last_frame, Camera
import time


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/video_feed')
@basic_auth.required
def video_feed():
    def gen(camera):
        while True:
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + camera.get_frame() + b'\r\n')
    return Response(gen(Camera()), mimetype='multipart/x-mixed-replace; boundary=frame')