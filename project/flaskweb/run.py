from flask import Flask, render_template
from flask.globals import request
from backend.youtube_client import SearchClient
from backend.entity import Video
from backend.test.youtube_client_test import API_KEY


search_client = SearchClient(key=API_KEY)
app = Flask(__name__)


@app.route('/video_live')
def video_live():
    return render_template("video.html", title='Video')


@app.route('/video_history')
def video_history():
    return render_template("video.html", title='Video')


@app.route('/video_history', methods=['POST'])
@app.route('/video_live', methods=['POST'])
def video_search():
    if 'video_keyword' in request.form:
        keyword = request.form.get("video_keyword", "").strip()
        if not keyword:
            keyword = 'youtube'
        print keyword
        videos = search_client.search_video_by_keyword(keyword=keyword, part='snippet', maxResults=True)
        video_list = Video.parse_video_json(videos)
        return render_template("video.html", video_list=video_list)


@app.route('/channel_live')
def channel_live():
    return render_template("channel.html", title='Channel')


@app.route('/channel_history')
def channel_history():
    return render_template("channel.html", title='Channel')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
