# -*- coding: utf-8 -*-
import sys

reload(sys)
sys.setdefaultencoding('utf8')


class Video(object):
    videoId = ""
    publishedAt = ""
    channelId = None
    title = ""
    description = ""
    thumbnails = ""
    channelTitle = ""

    def __init__(self, **kwargs):
        if "videoId" in kwargs:
            self.videoId = kwargs["videoId"]
        if "publishedAt" in kwargs:
            self.publishedAt = kwargs["publishedAt"]
        if "channelId" in kwargs:
            self.channelId = kwargs["channelId"]
        if "title" in kwargs:
            self.title = kwargs["title"]
        if "description" in kwargs:
            self.description = kwargs["description"]
        if "channelTitle" in kwargs:
            self.channelTitle = kwargs["channelTitle"]
        if "thumbnails" in kwargs:
            self.thumbnails = kwargs["thumbnails"]

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
                snippet = item["snippet"]
                video_list.append(Video(
                    videoId=item["id"]["videoId"],
                    publishedAt=snippet["publishedAt"],
                    channelId=snippet["channelId"],
                    title=snippet["title"],
                    description=snippet["description"],
                    thumbnails=snippet["thumbnails"]["default"]["url"],
                    channelTitle=snippet["channelTitle"]))
        return video_list


