import requests, json, urllib


class YoutubeClient(object):

    API_ENDPOINT = "https://www.googleapis.com/youtube/v3/"

    def __init__(self, resource, key):
        self.BASE_URL = "%s%s?key=%s" % (YoutubeClient.API_ENDPOINT, resource, key)
        self.data = None

    def __repr__(self):
        return self.BASE_URL

    @staticmethod
    def build_url(base_url, filters, part, max_results, page_token):
        target_url = "%s&part=%s" % (base_url, part)
        if filters and type(filters) is dict:
            target_url += "&" + str(urllib.urlencode(filters))
        if max_results:
            target_url = target_url + "&max_results=50"
        if page_token:
            target_url = target_url + "&page_token=" + page_token
        return target_url

    @staticmethod
    def build_filters(**kwargs):
        return {k: kwargs[k] for k in kwargs}

    @staticmethod
    def get_field_recursively(target_field_list, dict_data):
        for field in target_field_list:
            if field in dict_data:
                dict_data = dict_data[field]
            else:
                return None
        return dict_data

    def query(self, **kwargs):
        filters = YoutubeClient.build_filters(**kwargs)
        part = filters.pop("part") if "part" in filters else "id"
        max_results = filters.pop("max_results") if "max_results" in filters else False
        page_token = filters.pop("page_token") if "page_token" in filters else None
        target_url = YoutubeClient.build_url(self.BASE_URL, filters, part, max_results, page_token)
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
