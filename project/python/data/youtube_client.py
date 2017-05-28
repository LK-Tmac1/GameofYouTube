import requests, json, urllib


class YoutubeClient(object):

    API_ENDPOINT = "https://www.googleapis.com/youtube/v3/"
    API_KEY = ""

    def __init__(self, resource, key=None):
        if not key:
            self.key = YoutubeClient.API_KEY
        self.BASE_URL = "%s%s?key=%s" % (YoutubeClient.API_ENDPOINT, resource, self.key)
        self.data = ""

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
    def get_field_recursively(field_list, data):
        for field in field_list:
            if field in data:
                data = data[field]
            else:
                break
        return data

    def query(self, part="id", max_results=False, page_token=None, **kwargs):
        filters = YoutubeClient.build_filters(**kwargs)
        target_url = YoutubeClient.build_url(self.BASE_URL, filters, part, max_results, page_token)
        req = requests.get(target_url)
        if req.status_code == 200:
            return json.loads(req.text)
        return None


class SearchClient(YoutubeClient):
    def __init__(self):
        YoutubeClient.__init__(self, "search")

    def search_keyword(self, q, resource_type, part="id", max_results=False, page_token=None):
        return super(SearchClient, self).query(part, max_results, page_token, q=q, resource_type=resource_type)

    def search_by_channel(self, channel_id, part="id", max_results=False, page_token=None):
        return super(SearchClient, self).query(part, max_results, page_token, channelId=channel_id)


class ChannelClient(YoutubeClient):
    def __init__(self):
        YoutubeClient.__init__(self, "channels")

    def get_uploads_id(self, channel_id):
        data = self.query(part="contentDetails", id=channel_id)
        field_list = ["items", "contentDetails", "relatedPlaylists", "uploads"]
        uploads_id = YoutubeClient.get_field_recursively(field_list, data)
        return uploads_id


class VideoClient(YoutubeClient):
    def __init__(self):
        YoutubeClient.__init__(self, "videos")


def test_channel():
    filters = {"id": "UC-EnprmCZ3OXyAoG7vjVNCA"}
    part = "id,statistics"
    channel_client = ChannelClient()

    channel_client.query(filters=filters, part=part)
    print channel_client.data
    print channel_client.data_count()


def test_search():
    search_client = SearchClient()

    search_client.query('ps4 nier automata', 'channel')
    print search_client.data
    print search_client.data_count()


def test_video():
    data = VideoClient().query(filters={"channelId": "UC-EnprmCZ3OXyAoG7vjVNCA"})
    print data


if __name__ == "__main__":
    search_client = SearchClient()
    data = search_client.search_by_channel(channel_id="UC-EnprmCZ3OXyAoG7vjVNCA")
    print data