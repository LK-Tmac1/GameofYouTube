from random import randint
from datetime import datetime
from kafka.client import KafkaClient
from kafka.producer import SimpleProducer
import sys


class ActivitySource(object):
    random_placeholder = "?"
    default_rnd_range_channel = 3
    default_rnd_range_videos = 2
    default_activity = "view"

    def __init__(self, **kwargs):
        self.args = {k: kwargs[k] for k in kwargs}
        self.activity = self.args.get("activity", ActivitySource.default_activity)
        self.videos_list = self.args.get("videos_list", [])
        if not self.videos_list:
            self.videos_list = self.args.get("videos", "").split(",")
        self.rnd_range_videos = self.args.get("rnd_range_videos", ActivitySource.default_rnd_range_videos)
        self.rnd_range_videos = (len(self.videos_list) + 1) * self.rnd_range_videos
        #self.kafka_client = KafkaClient(**kwargs)
        #self.produce = SimpleProducer(self.kafka_client)

    @staticmethod
    def get_random_item(items, rnd_range=None):
        # Given a list of items, and a random seed, randomly pick one item
        if type(items) is not list:
            items = list([items])
        if not rnd_range:
            rnd_range = len(items) - 1
        rnd_idx = randint(0, rnd_range)
        return items[rnd_idx] if rnd_idx < len(items) else None

    @staticmethod
    def get_current_time():
        return str(datetime.now())[:-7]

    @staticmethod
    def parse_arguments(arguments):
        config = {}
        if arguments and len(arguments) > 1:
            for arg in arguments[1:]:
                args = arg.split("=")
                config[args[0][2:-1]] = args[1]
        return config

    @staticmethod
    def new_activity(channel=None, video=None, activity=None):
        channel = channel if channel else ActivitySource.random_placeholder
        video = video if video else ActivitySource.random_placeholder
        activity = activity if activity else ActivitySource.default_activity
        return "%s,%s,%s,%s" % (channel, video, activity, ActivitySource.get_current_time())

    def generate(self):
        pass

    def produce(self, message):
        self.producer.send_messages(self.activity, str(message).encode('utf-8'))


class ChannelSource(ActivitySource):

    def __init__(self, **kwargs):
        ActivitySource.__init__(self, **kwargs)
        self.channel_list = self.args.get("channels", "").split(",")
        self.rnd_range_channel = self.args.get("rnd_range_channel", ActivitySource.default_rnd_range_channel)


class ChannelVideoSource(ActivitySource):

    def __init__(self, **kwargs):
        ActivitySource.__init__(self, **kwargs)
        self.channel_id = self.args.get("channelId", None)
        self.rnd_range_channel = self.args.get("rnd_range_channel", ActivitySource.default_rnd_range_channel)

    def generate(self):
        channel = video = None
        if self.channel_id:
            channel = ActivitySource.get_random_item(self.channel_id, self.rnd_range_channel)
            if channel:  # Random videos belong to this channel
                video = ActivitySource.get_random_item(self.videos_list)
        return ActivitySource.new_activity(channel, video, self.activity)


class VideoSource(ActivitySource):

    def __init__(self, **kwargs):
        ActivitySource.__init__(self, **kwargs)

    def generate(self):
        video = None
        if len(self.videos_list) > 0:
            video = ActivitySource.get_random_item(self.videos_list, self.rnd_range_videos)
        return ActivitySource.new_activity(None, video, self.activity)


def test_channel_videos():
    channelId = "1"
    videos_list = range(10)
    batch = 100
    cs = ChannelVideoSource(channelId=channelId, videos_list=videos_list)
    for i in xrange(batch):
        print cs.generate()


def test_videos():
    videos_list = range(10)
    batch = 100
    video = VideoSource(videos_list=videos_list, activity="like")
    for i in xrange(batch):
        print video.generate()


def main():
    arg_list = ['--channelId=', '--activity=', "--rnd_range_channel=", "--rnd_range_videos=", "--videos="]
    config = ActivitySource.parse_config(arguments=sys.argv)
    channelId = config.get('channelId', None)
    activity = config.get('activity', 'view')
    rnd_range_channel = config.get('rnd_range_channel', ActivitySource.default_rnd_range_channel)
    rnd_range_videos = config.get('rnd_range_videos', ActivitySource.default_rnd_range_videos)

if __name__ == '__main__':
    test_videos()
    test_channel_videos()