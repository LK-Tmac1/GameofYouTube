from flask import Flask, render_template
from flask.globals import request
from backend.youtube import SearchClient
from backend.entity import Video, Channel
from backend.utility import parse_main_arguments, read_file
from backend.service import ProducerService, SparkService
import sys

app = Flask(__name__)
config_path = None
search_client = None


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
        keyword = request.form.get("video_keyword")
        json_data = search_client.search_video_by_keyword(keyword=keyword, part='snippet')
        video_list = Video.parse_video_json(json_data=json_data)
        return render_template("video.html", video_list=video_list)
    elif "video_info" in request.form:
        video_info = request.form.getlist("video_info")[0]
        video_info = video_info.split(":")
        video_id = video_info[0]
        channel_id = video_info[1]
        activity = request.form["activity"]
        spark_service = SparkService()
        #producer_service = ProducerService(channelId=channel_id, mode="video", videos=video_id, activity=activity)
        producer_service = ProducerService()
        producer_service.add_argument_pair(producer="file", output_path="/Users/kunliu/Desktop/test")
        producer_service.add_argument_pair(channelId=channel_id, mode="channel_video")
        producer_service.add_argument_pair(videos=video_id+",1,2,3,4,5")
        producer_service.add_argument_pair(activity=activity, write_mode="a",output_mode="d")
        producer_service.start()
        print producer_service.PID
        return render_template("video.html")


@app.route('/channel')
@app.route('/channel_stream')
def channel():
    return render_template("channel.html", title="Channel")


@app.route('/channel', methods=['POST'])
@app.route('/channel_stream', methods=['POST'])
def channel_search():
    keyword = request.form.get("channel_keyword")
    json_data = search_client.search_channel_by_keyword(keyword=keyword, part="snippet")
    channel_list = Channel.parse_channel_json(json_data=json_data)
    return render_template("channel.html", title="Channel", channel_list=channel_list)


if __name__ == '__main__':
    arguments = sys.argv
    arguments.append("--config_path=/Users/kunliu/git/youtubetrends/project/config.yml")
    if len(sys.argv) <= 1:
        print "Need to specify --config_path=<path to yaml config file>"
        exit(1)
    config_path = parse_main_arguments(sys.argv).get("config_path")
    config = read_file(file_path=config_path, is_yml=True)
    search_client = SearchClient(key=config["youtube"]["api_key"])
    app.run(host='0.0.0.0', port=config["flask"]["port"], debug=True)
