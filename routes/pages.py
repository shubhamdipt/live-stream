#!/usr/bin/env python
from flask import Flask, render_template, Response
from application import app, basic_auth
from routes.utils import Camera
import time


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/history')
def history():
    return render_template('history.html')


@app.route('/feed/live_video_feed')
@basic_auth.required
def live_video_feed():
    def gen(camera):
        while True:
            time.sleep(0.2)
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + camera.get_live_frame() + b'\r\n')
    return Response(gen(Camera()), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/feed/video_feed')
@basic_auth.required
def video_feed():
    def gen(camera):
        while True:
            # time.sleep(0.2)
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + camera.get_frame() + b'\r\n')
    return Response(gen(Camera()), mimetype='multipart/x-mixed-replace; boundary=frame')