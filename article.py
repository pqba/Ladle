from stew_bot import load_ladle, best_video_quality, send_streamable_request, gallery_links


# Article class for Posts to be either Image, Video, YouTube, Streamable, or unrecognized
class Article:
    _url = ""
    _display_html = ""
    div_begin = "<div class = \"content-center spacer\">"
    div_end = "</div>"
    image_tags = "class=\"post-image\" crossorigin=\"anonymous\" referrerpolicy=\"no-referrer\""
    iframe_tags = "referrerpolicy=\"no-referrer\" allow=\"accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture\" frameborder=\"0\" allowfullscreen"
    video_tags = "class=\"normal-vid\" type=\"video/mp4\" controls"

    def __init__(self, raw_url: str):
        self._url = raw_url
        self._display_html = self._determine_display()

    # Returns appropriately escaped HTML for article type. Polls and Galleries not implemented yet.
    def _determine_display(self) -> str:
        if 'reddit.com/r/' in self._url:
            return ""
        elif 'i.redd.it' in self._url:
            return f"{self.div_begin} <img src=\"{self._url}\" {self.image_tags}/> {self.div_end}"

        elif 'v.redd.it' in self._url:
            video_quality = best_video_quality(f"{self._url}/DASHPlaylist.mpd")
            if video_quality == "N/A":
                return ""

            video_src = f"{self._url}/DASH_{video_quality}.mp4"
            """While receiving the audio works and rate is always 128p, there's no free or quick way to reference the 
            video without downloading and combining the sources on the backend. 
            audio_quality = 128 
            audio_src = f"{self._url}/DASH_AUDIO_{audio_quality}.mp4 """
            return f"{self.div_begin}<video src={video_src} {self.iframe_tags} {self.video_tags}></video> {self.div_end}"

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
        elif 'reddit.com/gallery/' in self._url:
            gallery_model = load_ladle().submission(url=self._url)
            post_carousel = gallery_links(gallery_model.media_metadata)
            # TODO: figure out post carousels
            print(post_carousel)
            gallery_script = f"<script>console.log(\"Hello, gallery\");</script>"
            return f"{self.div_begin} <button>< <img src={post_carousel[0]} {self.image_tags}/> {self.div_end} {gallery_script}"
        else:
            """
            Tried to implement this, but it added an immense amount of time to rendering.
            html_embed = PyEmbed().embed(url=self._url)
            return f"{self.div_begin} {html_embed} {self.div_end}
            """
            return f"{self.div_begin}<p class=\"smaller-text highlight-orange\"> Open link to view post. </p> {self.div_end}"

    def display(self) -> str:
        return self._display_html

    def get_url(self) -> str:
        return self._url
