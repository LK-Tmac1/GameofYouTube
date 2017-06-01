from flask import Flask, render_template
from flask.globals import request
from backend.utility import parse_main_arguments, read_file
from backend.handler import RequestHandler
import sys

app = Flask(__name__)


@app.route('/video')
def video():
    return render_template("video.html", title='Video')


@app.route('/video_stream')
def video_stream():
    return render_template("video.html", title='Video')


@app.route('/video', methods=['POST'])
@app.route('/video_stream', methods=['POST'])
def video_search():
    if "video_keyword" in request.form:
        video_list = RequestHandler.video_search(form=request.form)
        return render_template("video.html", video_list=video_list)
    elif "video_info" in request.form:
        RequestHandler.start_spark_streaming(form=request.form)
        return render_template("video.html")


@app.route('/channel')
@app.route('/channel_stream')
def channel():
    return render_template("channel.html", title="Channel")


@app.route('/channel', methods=['POST'])
@app.route('/channel_stream', methods=['POST'])
def channel_search():
    channel_list = RequestHandler.channel_search(request.form)
    return render_template("channel.html", title="Channel", channel_list=channel_list)


if __name__ == '__main__':
    arguments = sys.argv
    arguments.append("--config_path=/Users/kunliu/git/youtubetrends/project/config.yml")
    if len(sys.argv) <= 1:
        print "Need to specify --config_path=<path to yaml config file>"
        exit(1)
    config_path = parse_main_arguments(sys.argv).get("config_path")
    config = read_file(file_path=config_path, is_yml=True)
    RequestHandler.initialize(config)
    app.run(host='0.0.0.0', port=config["flask"]["port"], debug=True)
