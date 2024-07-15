from stew_bot import send_streamable_request


# Article class for Posts to be either Image, Video, YouTube, Streamable, or unrecognized
class Article:
    _url = ""
    _display_html = ""
    div_begin = "<div class = \"content-center spacer\">"
    div_end = "</div>"
    iframe_tags = "referrerpolicy=\"no-referrer\" allow=\"accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture\" frameborder=\"0\" allowfullscreen"

    def __init__(self, raw_url: str):
        self._url = raw_url
        self._display_html = self._determine_display()

    # Returns appropriately escaped HTML for article type. Polls and Galleries not implemented yet.
    def _determine_display(self) -> str:
        if 'reddit.com/r/' in self._url:
            return ""
        elif 'i.redd.it' in self._url:
            return f"{self.div_begin} <img src=\"{self._url}\" class=\"post-image\" crossorigin=\"anonymous\" referrerpolicy=\"no-referrer\"/> {self.div_end}"

        elif 'v.redd.it' in self._url:
            return f"{self.div_begin} THIS IS A VIDEO OR SOMETHING {self.div_end}"

        elif 'streamable' in self._url:
            streamy_info = send_streamable_request(self._url.split(".com/")[1])
            if 'error' in streamy_info or streamy_info['status'] != 2:
                return ""

            source = streamy_info["embed_code"].replace("\\", "").split("src=")[1].split(" ")[0]  # get embed url
            subtitle = streamy_info["title"]
            return f"{self.div_begin}<iframe src={source} class=\"streamy streamable-embed\" {self.iframe_tags}></iframe> <p class=\"smaller-text\">{subtitle}</p> {self.div_end}"

        elif 'youtube' in self._url:
            yt_embed = f"https://www.youtube-nocookie.com/embed/{self._url.split("v=")[-1]}"
            return f"{self.div_begin} <iframe src=\"{yt_embed}\" {self.iframe_tags} class=\"yt-embed\"></iframe>{self.div_end}"
        else:
            return "<p class=\"smaller-text highlight-red\"Content type not recognized.</p>"

    def display(self) -> str:
        return self._display_html

    def get_url(self) -> str:
        return self._url
