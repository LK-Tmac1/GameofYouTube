from random import randint
from kafka import KafkaProducer
from utility import parse_main_arguments, pop_argument, is_path_existed, get_current_time
import time, sys, os


class ActivityProducer(object):
    default_produce_tempo = 1

    def __init__(self, **kwargs):
        self.produce_tempo = float(pop_argument("tempo", kwargs, ActivityProducer.default_produce_tempo))
        self.source = pop_argument("source", kwargs, None)

    def __repr__(self):
        return "%s, tempo=%s, source=%s" % (self.__class__.__name__, self.produce_tempo, self.source)

    @staticmethod
    def build_producer(**kwargs):
        source = ActivitySource.build_source(**kwargs)
        producer = pop_argument("producer", kwargs, "file")
        if producer == "file":
            return ActivityFileProducer(source=source, **kwargs)
        elif producer == "kafka":
            return ActivityKafkaProducer(source=source, **kwargs)
        return None

    def produce(self):
        if self.source is None:
            print "Not able to build an activity source by parameters provided."
            sys.exit(-1)
        self.new_message()
        if self.produce_tempo:
            time.sleep(self.produce_tempo)


class ActivityKafkaProducer(ActivityProducer):
    def __init__(self, **kwargs):
        ActivityProducer.__init__(self, **kwargs)
        pop_config_list = list([])
        for k in kwargs:
            if k not in KafkaProducer.DEFAULT_CONFIG:
                pop_config_list.append(k)
        for k in pop_config_list:
            kwargs.pop(k)
        kwargs["api_version"]=(0, 10)
        self.producer = KafkaProducer(**kwargs)

    def new_message(self):
        while True:
            message = self.source.new_activity()
            self.producer.send(topic=self.source.activity, value=message)


class ActivityFileProducer(ActivityProducer):
    def __init__(self, **kwargs):
        ActivityProducer.__init__(self, **kwargs)
        self.output_path = pop_argument("output_path", kwargs, "./test-output")
        self.write_mode = pop_argument("write_mode", kwargs, "w")
        self.output_mode = pop_argument("output_mode", kwargs, "d")

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
    random_placeholder = "?"
    default_rnd_seed_channel = 3
    default_rnd_seed_video = 2
    default_activity = "view"

    def __init__(self, **kwargs):
        self.activity = pop_argument("activity", kwargs, ActivitySource.default_activity)
        self.videos_list = pop_argument("videos", kwargs, [])
        if self.videos_list:
            self.videos_list = self.videos_list.split(",")
        self.rnd_seed_video = pop_argument("rnd_seed_video", kwargs, ActivitySource.default_rnd_seed_video)
        self.rnd_seed_video = len(self.videos_list) * self.rnd_seed_video + 1

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
        channel = channel if channel else ActivitySource.random_placeholder
        video = video if video else ActivitySource.random_placeholder
        activity = activity if activity else ActivitySource.default_activity
        return "%s,%s,%s,%s" % (channel, video, activity, get_current_time())

    @staticmethod
    def build_source(**kwargs):
        mode = pop_argument("source_mode", kwargs, "video")
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
        self.channel_id = pop_argument("channelId", kwargs, None)
        self.rnd_range_channel = pop_argument("rnd_seed_channel", kwargs, ActivitySource.default_rnd_seed_channel)

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
        self.channel_list = pop_argument("channels", kwargs, [])
        if self.channel_list:
            self.channel_list = self.channel_list.split(",")
        self.rnd_seed_channel = pop_argument("rnd_seed_channel", kwargs, ActivitySource.default_rnd_seed_channel)

    def new_activity(self):
        channel = ActivitySource.get_random_item(self.channel_list, self.rnd_seed_channel)
        return ActivitySource.format_activity(None, channel, self.activity)


if __name__ == '__main__':
    config = parse_main_arguments(sys.argv)
    producer = ActivityProducer.build_producer(**config)
    producer.produce()
