from random import randint
from kafka.client import KafkaClient
from kafka.producer import SimpleProducer
from utility import parse_main_arguments, prepare_field, is_path_existed, get_current_time
import time, sys, os

random_placeholder = "?"
default_rnd_seed_channel = 3
default_rnd_seed_video = 2
default_activity = "view"
default_produce_tempo = 1


class ActivityProducer(object):
    def __init__(self, **kwargs):
        self.produce_tempo = float(prepare_field("tempo", kwargs, default_produce_tempo))
        self.source = kwargs["source"]

    def __repr__(self):
        return "%s, tempo=%s, source=%s" % (self.__class__.__name__, self.produce_tempo, self.source)

    @staticmethod
    def build_producer(source, **kwargs):
        mode = kwargs.get("producer", "file")
        if mode == "file":
            return ActivityFileProducer(source=source, **kwargs)
        elif mode == "kafka":
            return ActivityKafkaProducer(source=source, **kwargs)
        return None

    def produce(self):
        self.new_message()
        if self.produce_tempo:
            time.sleep(self.produce_tempo)


class ActivityKafkaProducer(ActivityProducer):
    def __init__(self, **kwargs):
        ActivityProducer.__init__(self, **kwargs)
        self.kafka_client = KafkaClient(**kwargs)
        self.producer = SimpleProducer(self.kafka_client)

    def new_message(self):
        while True:
            message = self.source.new_activity()
            self.producer.send_messages(self.source.activity, message)


class ActivityFileProducer(ActivityProducer):
    def __init__(self, **kwargs):
        ActivityProducer.__init__(self, **kwargs)
        self.output_path = kwargs["output_path"]
        self.write_mode = prepare_field("write_mode", kwargs, "w")
        self.output_mode = prepare_field("output_mode", kwargs, "d")

    @staticmethod
    def write_local_file(output_path, content, write_mode):
        parent_dir = output_path[0:output_path.rfind("/")]
        # If output parent dir does not exist, create it
        if not is_path_existed(parent_dir):
            os.makedirs(parent_dir)
        with open(output_path, write_mode) as output:
            output.write(content+"\n")
            output.close()

    @staticmethod
    def write_local_path(output_dir, content, file_name, write_mode):
        if output_dir[-1] != "/":
            output_dir += "/"
        output_path = output_dir + file_name
        ActivityFileProducer.write_local_file(output_path, content, write_mode)

    def new_message(self):
        while True:
            message = self.source.new_activity()
            if self.output_mode == "d":
                file_name = get_current_time()
                ActivityFileProducer.write_local_path(self.output_path, message, file_name, self.write_mode)
            else:
                ActivityFileProducer.write_local_file(self.output_path, message, self.write_mode)


class ActivitySource(object):
    def __init__(self, **kwargs):
        self.activity = prepare_field("activity", kwargs, default_activity)
        self.videos_list = prepare_field("videos", kwargs, [])
        if self.videos_list:
            self.videos_list = self.videos_list.split(",")
        self.rnd_seed_video = prepare_field("rnd_seed_video", kwargs, default_rnd_seed_video)
        self.rnd_seed_video = len(self.videos_list) * self.rnd_seed_video + 1

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
    def format_activity(channel=None, video=None, activity=None):
        channel = channel if channel else random_placeholder
        video = video if video else random_placeholder
        activity = activity if activity else default_activity
        return "%s,%s,%s,%s" % (channel, video, activity, get_current_time())

    @staticmethod
    def build_source(**kwargs):
        mode = kwargs.get("mode", "video")
        if mode == "video":
            return VideoSource(**kwargs)
        elif mode == "channel_video":
            return ChannelVideoSource(**kwargs)
        elif mode == "channel":
            return ChannelSource(**kwargs)
        return None

    def new_activity(self):
        return ""


class ChannelVideoSource(ActivitySource):
    # Only videos belong to a given channel
    def __init__(self, **kwargs):
        ActivitySource.__init__(self, **kwargs)
        self.channel_id = prepare_field("channelId", kwargs, None)
        self.rnd_range_channel = prepare_field("rnd_seed_channel", kwargs, default_rnd_seed_channel)

    def __repr__(self):
        return "%s\nChannelId=%s %s" % (ActivitySource.__repr__(self), self.channel_id, self.rnd_range_channel)

    def new_activity(self):
        channel = video = None
        if self.channel_id:
            channel = ActivitySource.get_random_item(self.channel_id, self.rnd_range_channel)
            if channel:  # Random videos belong to this channel
                video = ActivitySource.get_random_item(self.videos_list)
        return ActivitySource.format_activity(channel, video, self.activity)


class VideoSource(ActivitySource):
    # Only video user activity, no channel info
    def __init__(self, **kwargs):
        ActivitySource.__init__(self, **kwargs)

    def new_activity(self):
        video = ActivitySource.get_random_item(self.videos_list, self.rnd_seed_video)
        return ActivitySource.format_activity(None, video, self.activity)


class ChannelSource(ActivitySource):
    # Only channel user activity, no video info
    def __init__(self, **kwargs):
        ActivitySource.__init__(self, **kwargs)
        self.channel_list = prepare_field("channels", kwargs, [])
        if self.channel_list:
            self.channel_list = self.channel_list.split(",")
        self.rnd_seed_channel = prepare_field("rnd_seed_channel", kwargs, default_rnd_seed_channel)

    def new_activity(self):
        channel = ActivitySource.get_random_item(self.channel_list, self.rnd_seed_channel)
        return ActivitySource.format_activity(None, channel, self.activity)


if __name__ == '__main__':
    config = parse_main_arguments(sys.argv)
    activity_source = ActivitySource.build_source(**config)
    producer = ActivityProducer.build_producer(source=activity_source, **config)
    producer.produce()
