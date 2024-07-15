from stew_bot import send_streamable_request
# Article class for Posts to be either Image, Video, Youtube, Streamable, or unrecognized
class Article:
    _url = ""
    _display_html = ""
    def  __init__(self,raw_url: str):
        self._url = raw_url.lower()
        self._display_html = self._determine_display()

    # Returns appropriately escaped HTML for article type
    # TODO: add gallery photo functionality and poll functionality
    def _determine_display(self) -> str:
        if 'i.reddit' in self._url:
            return f"<div class=\"content-center spacer\"><img src=\"{self._url}\"  class=\"post-image\" crossorigin=\"anonymous\" referrerpolicy=\"no-referrer\"/></div>"
        elif 'v.reddit' in self._url:
            return "hi"
        elif 'streamable' in self._url:
            streamy_info = send_streamable_request(self._url.split(".com/")[1])
            source = streamy_info["embed_code"].replace("\\","")
            subtitle = streamy_info["title"]
            return "streamable lol"
        elif 'youtube' in self._url:
            return "youtube lol"
        else:
            return ""

    def display(self) -> str:
        return self._display_html

    def get_url(self) -> str:
        return self._url
        