from youtube_client import ChannelClient, VideoClient, SearchClient
from utility import Utility
from random import randint


class ActivitySource(object):
    ACTIVITY_FORMAT = "channelID:videoID:activity:timestamp"
    random_placeholder = "?"
    default_rnd_range_channel = 3
    default_rnd_range_videos = 2
    channel_client = ChannelClient()
    video_client = VideoClient()
    search_client = SearchClient()

    @staticmethod
    def get_random_item(target_list, rnd_range=None):
        # Given a list of items, and a random seed total, randomly pick one item
        if not rnd_range:
            rnd_range = len(target_list)-1
        rnd_idx = randint(0, rnd_range)
        if rnd_idx < len(target_list):
            return target_list[rnd_idx]
        else:
            return ActivitySource.random_placeholder

    @staticmethod
    def channel_videos(channel_id, videos_list, rnd_range_videos=None, rnd_range_channel=None, activity_list=None):
        activity = ActivitySource.get_random_item(activity_list) if activity_list else "view"
        if rnd_range_channel is None:
            rnd_range_channel = ActivitySource.default_rnd_range_channel
        if rnd_range_videos is None:
            rnd_range_videos = len(videos_list) * ActivitySource.default_rnd_range_videos
        channel = ActivitySource.get_random_item([channel_id], rnd_range_channel)
        video = ActivitySource.random_placeholder
        if channel != ActivitySource.random_placeholder:
            video = ActivitySource.get_random_item(videos_list, rnd_range_videos)
        return "%s,%s,%s,%s" % (channel, video, activity, Utility.get_current_time())


def test():
    channel_id = "1"
    videos_list = range(10)
    batch = 100
    for i in xrange(batch):
        print ActivitySource.channel_videos(channel_id, videos_list)
