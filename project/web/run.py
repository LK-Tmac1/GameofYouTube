from flask import Flask, render_template
from flask.globals import request
from backend.youtube_client import SearchClient
from backend.entity import Video, Channel
from backend.test.youtube_client_test import API_KEY


search_client = SearchClient(key=API_KEY)
app = Flask(__name__)


@app.route('/video')
def video():
    return render_template("video.html", title='Video')


@app.route('/video', methods=['POST'])
def video_search():
    keyword = request.form.get("video_keyword")
    json_data = search_client.search_video_by_keyword(keyword=keyword, part='snippet', max_results=False)
    video_list = Video.parse_video_json(json_data=json_data)
    return render_template("video.html", video_list=video_list)


@app.route('/channel')
def channel():
    return render_template("channel.html", title="Channel")


@app.route('/channel', methods=['POST'])
def channel_search():
    keyword = request.form.get("channel_keyword")
    json_data = search_client.search_channel_by_keyword(keyword=keyword, part="snippet", max_results=False)
    channel_list = Channel.parse_channel_json(json_data=json_data)
    return render_template("channel.html", title="Channel", channel_list=channel_list)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
