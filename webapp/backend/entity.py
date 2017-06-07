
class BaseEntity(object):
    publishedAt = ""
    channelId = ""
    description = ""
    thumbnails = ""
    channelTitle = ""
    title = ""

    def __init__(self, **kwargs):
        if "publishedAt" in kwargs:
            self.publishedAt = kwargs["publishedAt"]
        if "channelId" in kwargs:
            self.channelId = kwargs["channelId"]
        if "description" in kwargs:
            self.description = kwargs["description"]
        if "channelTitle" in kwargs:
            self.channelTitle = kwargs["channelTitle"]
        if "thumbnails" in kwargs:
            self.thumbnails = kwargs["thumbnails"]
        if "title" in kwargs:
            self.thumbnails = kwargs["title"]

    @staticmethod
    def parse_item(item, entity):
        if "snippet" in item:
            entity.publishedAt = item["snippet"]["publishedAt"]
            entity.channelId = item["snippet"]["channelId"]
            entity.description = item["snippet"]["description"]
            entity.thumbnails = item["snippet"]["thumbnails"]["default"]["url"]
            entity.channelTitle = item["snippet"]["channelTitle"]
            entity.title = item["snippet"]["title"]


class Video(BaseEntity):
    videoId = ""
    title = ""

    def __init__(self, **kwargs):
        BaseEntity.__init__(self, **kwargs)
        if "videoId" in kwargs:
            self.videoId = kwargs["videoId"]

    def __repr__(self):
        return "Video: %s, %s Channel: %s" % (self.videoId, self.title, self.channelId)

    def __cmp__(self, other):
        if self.publishedAt > other.publishedAt:
            return 1
        elif self.publishedAt == other.publishedAt:
            return 0
        return -1

    @staticmethod
    def parse_video_json(json_data):
        video_list = []
        if json_data:
            for item in json_data.get("items", []):
                if "id" in item and "videoId" in item["id"]:
                    video = Video(videoId=item["id"]["videoId"])
                    BaseEntity.parse_item(item, video)
                    video_list.append(video)
        return video_list


class Channel(BaseEntity):
    viewCount = 0
    commentCount = 0
    subscriberCount = 0
    videoCount = 0
    uploads = ""

    def __init__(self, **kwargs):
        BaseEntity.__init__(self, **kwargs)
        if "statistics" in kwargs:
            self.update_stat(kwargs["statistics"])
        self.uploads = kwargs.get("uploads", "")

    def update_stat(self, stat):
        if stat:
            self.viewCount = stat.get("viewCount", 0)
            self.commentCount = stat.get("commentCount", 0)
            self.subscriberCount = stat.get("subscriberCount", 0)
            self.videoCount = stat.get("videoCount", 0)

    def __cmp__(self, other):
        total1 = self.videoCount + self.videoCount + self.commentCount + self.videoCount
        total2 = other.videoCount + other.videoCount + other.commentCount + other.videoCount
        return cmp(total1, total2)

    def __repr__(self):
        return "Channel: %s, %s" % (self.channelId, self.channelTitle)

    @staticmethod
    def parse_channel_json(json_data):
        channel_list = []
        if json_data:
            for item in json_data.get("items", []):
                if "id" in item and "channelId" in item["id"]:
                    channel = Channel()
                    channel.update_stat(item.get("statistics"))
                    if "contentDetails" in item and "relatedPlaylists" in item["contentDetails"]:
                        channel.uploads = item["contentDetails"]["relatedPlaylists"]["uploads"]
                    BaseEntity.parse_item(item, channel)
                    channel_list.append(channel)
        return channel_list
