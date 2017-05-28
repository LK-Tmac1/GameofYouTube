from flask import render_template
from flask.globals import request
from app import app


@app.route('/channel')
def channel():
    return render_template("channel.html", title='Channel')
