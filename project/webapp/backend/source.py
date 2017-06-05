from random import randint
from utility import pop_argument, get_current_time


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

