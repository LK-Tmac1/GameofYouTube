from random import randint
from datetime import datetime
from kafka.client import KafkaClient
from kafka.producer import SimpleProducer
import time

random_placeholder = "?"
default_rnd_seed_channel = 3
default_rnd_seed_video = 2
default_activity = "view"
default_produce_tempo = 0


class ActivityProducer(object):
    def __init__(self, **kwargs):
        self.activity = ActivityProducer.prepare_field("activity", kwargs, default_activity)
        self.videos_list = ActivityProducer.prepare_field("videos", kwargs, [])
        if self.videos_list:
            self.videos_list = self.videos_list.split(",")
        self.rnd_seed_video = ActivityProducer.prepare_field("rnd_seed_video", kwargs, default_rnd_seed_video)
        self.rnd_seed_video = len(self.videos_list) * self.rnd_seed_video + 1
        self.produce_tempo = float(ActivityProducer.prepare_field("tempo", kwargs, default_produce_tempo))
        #self.kafka_client = KafkaClient(**kwargs)
        #self.produce = SimpleProducer(self.kafka_client)

    def __repr__(self):
        class_name = self.__class__.__name__
        videos = ",".join(self.videos_list)
        return "%s %s %s %s %s %s" % (class_name, self.activity, videos, self.rnd_seed_video, self.produce_tempo)

    @staticmethod
    def get_random_item(items, rnd_seed=None):
        # Given a list of items, and a random seed, randomly pick one item
        if type(items) is not list:
            items = list([items])
        if not rnd_seed:
            rnd_seed = len(items) - 1
        rnd_idx = randint(0, rnd_seed)
        if items and rnd_idx < len(items):
            return items[rnd_idx]
        return None

    @staticmethod
    def get_current_time():
        return str(datetime.now())[:-7]

    @staticmethod
    def format_activity(channel=None, video=None, activity=None):
        channel = channel if channel else random_placeholder
        video = video if video else random_placeholder
        activity = activity if activity else default_activity
        return "%s,%s,%s,%s" % (channel, video, activity, ActivityProducer.get_current_time())

    @staticmethod
    def build_producer(config):
        mode = ActivityProducer.prepare_field("mode", config, "video")
        c = config.get('channelId')
        a = config.get('activity')
        rc = config.get('rnd_seed_channel')
        rv = config.get('rnd_seed_video')
        v = config.get("videos")
        t = config.get("tempo")
        if mode == "video":
            return VideoProducer(activity=a, rnd_range_videos=rv, videos=v, tempo=t)
        if mode == "channel_video":
            return ChannelVideoProducer(channelId=c, activity=a, rnd_range_channel=rc, rnd_range_videos=rv, videos=v, tempo=t)
        return None

    @staticmethod
    def prepare_field(arg, arguments, default=None):
        if arg in arguments and arguments.get(arg):
            return arguments.pop(arg)
        return default

    def new_activity(self):
        return ""

    def produce(self):
        while True:
            message = self.new_activity()
            # self.producer.send_messages(self.activity, message)
            print message
            if self.produce_tempo:
                time.sleep(self.produce_tempo)


class ChannelVideoProducer(ActivityProducer):
    # Only videos belong to a given channel
    def __init__(self, **kwargs):
        ActivityProducer.__init__(self, **kwargs)
        self.channel_id = ActivityProducer.prepare_field("channelId", kwargs, None)
        self.rnd_range_channel = ActivityProducer.prepare_field("rnd_seed_channel", kwargs, default_rnd_seed_channel)

    def new_activity(self):
        channel = video = None
        if self.channel_id:
            channel = ActivityProducer.get_random_item(self.channel_id, self.rnd_range_channel)
            if channel:  # Random videos belong to this channel
                video = ActivityProducer.get_random_item(self.videos_list)
        return ActivityProducer.format_activity(channel, video, self.activity)


class VideoProducer(ActivityProducer):
    # Only video user activity, no channel info
    def __init__(self, **kwargs):
        ActivityProducer.__init__(self, **kwargs)

    def new_activity(self):
        video = ActivityProducer.get_random_item(self.videos_list, self.rnd_seed_video)
        return ActivityProducer.format_activity(None, video, self.activity)


class ChannelProducer(ActivityProducer):
    # Only channel user activity, no video info
    def __init__(self, **kwargs):
        ActivityProducer.__init__(self, **kwargs)
        self.channel_list = ActivityProducer.prepare_field("channels", kwargs, [])
        if self.channel_list:
            self.channel_list = self.channel_list.split(",")
        self.rnd_seed_channel =  ActivityProducer.prepare_field("rnd_seed_channel", kwargs, default_rnd_seed_channel)

    def new_activity(self):
        channel = ActivityProducer.get_random_item(self.channel_list, self.rnd_seed_channel)
        return ActivityProducer.format_activity(None, channel, self.activity)
