from flask import Flask, render_template
from flask.globals import request
from backend.youtube import SearchClient
from backend.entity import Video, Channel
from backend.utility import parse_main_arguments, read_file
import sys

app = Flask(__name__)
config = {}


@app.route('/video')
def video():
    return render_template("video.html", title='Video')


@app.route('/video', methods=['POST'])
def video_search():
    keyword = request.form.get("video_keyword")
    json_data = search_client.search_video_by_keyword(keyword=keyword, part='snippet')
    video_list = Video.parse_video_json(json_data=json_data)
    return render_template("video.html", video_list=video_list)


@app.route('/channel')
def channel():
    return render_template("channel.html", title="Channel")


@app.route('/channel', methods=['POST'])
def channel_search():
    keyword = request.form.get("channel_keyword")
    json_data = search_client.search_channel_by_keyword(keyword=keyword, part="snippet")
    channel_list = Channel.parse_channel_json(json_data=json_data)
    return render_template("channel.html", title="Channel", channel_list=channel_list)


if __name__ == '__main__':
    sys.argv.append("--config_path=/Users/kunliu/git/youtubetrends/project/config.yml")
    if len(sys.argv) <= 1:
        print "Need to specify --config_path=<path to yaml config file>"
        exit(1)
    config_path = parse_main_arguments(sys.argv).get("config_path")
    config = read_file(file_path=config_path, is_yml=True)
    search_client = SearchClient(key=config["youtube"]["api_key"])
    app.run(host='0.0.0.0', port=config["flask"]["port"], debug=True)
