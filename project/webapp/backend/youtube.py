import requests, json, urllib


class YoutubeClient(object):

    API_ENDPOINT = "https://www.googleapis.com/youtube/v3/"

    def __init__(self, resource, key):
        self.BASE_URL = "%s%s?key=%s" % (YoutubeClient.API_ENDPOINT, resource, key)

    def __repr__(self):
        return self.BASE_URL

    @staticmethod
    def build_url(base_url, **kwargs):
        target_url = "%s&part=%s" % (base_url, kwargs.pop("part", "id"))
        if kwargs.pop("max_results", False):
            target_url += "&max_results=50"
        if kwargs.get("page_token"):
            target_url += "&page_token=" + kwargs.pop("page_token")
        if kwargs:
            target_url += "&" + str(urllib.urlencode(kwargs))
        return target_url

    @staticmethod
    def get_field_recursively(target_field_list, dict_data):
        for field in target_field_list:
            if field in dict_data:
                dict_data = dict_data[field]
            else:
                return None
        return dict_data

    def query(self, **kwargs):
        target_url = YoutubeClient.build_url(self.BASE_URL, **kwargs)
        req = requests.get(target_url)
        if req.status_code == 200:
            return json.loads(req.text)
        return None


class SearchClient(YoutubeClient):
    def __init__(self, key):
        YoutubeClient.__init__(self, "search", key=key)

    def search_keyword(self, q, type, **kwargs):
        if q and str(q).strip():
            return super(SearchClient, self).query(q=str(q).strip(), type=type, **kwargs)
        return None

    def search_by_channel(self, channel_id, **kwargs):
        return super(SearchClient, self).query(channelId=channel_id, **kwargs)

    def search_video_by_keyword(self, keyword, **kwargs):
        return self.search_keyword(q=keyword, type="video", **kwargs)

    def search_channel_by_keyword(self, keyword, **kwargs):
        return self.search_keyword(q=keyword, type="channel", **kwargs)


class ChannelClient(YoutubeClient):
    def __init__(self, key):
        YoutubeClient.__init__(self, "channels", key=key)

    def get_uploads_id(self, channel_id):
        channel = self.query(part="contentDetails", id=channel_id)
        field_list = ["items", "contentDetails", "relatedPlaylists", "uploads"]
        uploads_id = YoutubeClient.get_field_recursively(field_list, channel)
        return uploads_id


class VideoClient(YoutubeClient):
    def __init__(self, key):
        YoutubeClient.__init__(self, "videos", key=key)
