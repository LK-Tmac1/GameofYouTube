from flask import render_template
from flask.globals import request
from app import app


@app.route('/video')
def video_home():
    return render_template("video.html", title='Video')
