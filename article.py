from stew_bot import load_ladle, best_video_quality, send_streamable_request, gallery_links


# Article class for Posts to be either Image, Video, Gallery, YouTube, Streamable, or unrecognized
class Article:
    _url = ""
    _display_html = ""
    div_begin = "<div class = \"content-center spacer\">"
    div_end = "</div>"
    btn_tag = "curated-button"
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
            audio_quality = 128  # Seems to always have 128 sample rate.
            audio_src = f"{self._url}/DASH_AUDIO_{audio_quality}.mp4"
            return f"{self.div_begin}<video id=\"video\" {self.iframe_tags} {self.video_tags}></video> {self.get_video_code(video_src,audio_src)}{self.div_end}"

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
            return f"{self.div_begin}<div class =\"slider content-center\"> {self.get_gallery_code(post_carousel)}</div> <div class=\"spacer\"></div> <button class=\"prevSlide {self.btn_tag}\">Previous</button> <button class=\"nextSlide {self.btn_tag}\">Next</button> {self.div_end}"
        else:
            """
            Tried to implement this, but it added an immense amount of time for rendering.
            html_embed = PyEmbed().embed(url=self._url)
            return f"{self.div_begin} {html_embed} {self.div_end}
            """
            return f"{self.div_begin}<p class=\"smaller-text highlight-orange\"> Open link to view post. </p> {self.div_end}"

    def display(self) -> str:
        return self._display_html

    def get_url(self) -> str:
        return self._url

    def get_video_code(self, video_url: str, audio_url: str) -> str:
        return ("<script>document.addEventListener('DOMContentLoaded', () => {" + f"const videoUrl = '{video_url}'; const audioUrl = '{audio_url}'"
                + """ const videoElement = document.getElementById('video');
      if ('MediaSource' in window && MediaSource.isTypeSupported('video/mp4; codecs="avc1.42E01E, mp4a.40.2"')) {
        const mediaSource = new MediaSource();
        videoElement.src = URL.createObjectURL(mediaSource);
        mediaSource.addEventListener('sourceopen', () => {
          const videoSourceBuffer = mediaSource.addSourceBuffer('video/mp4; codecs="avc1.42E01E"');
          const audioSourceBuffer = mediaSource.addSourceBuffer('audio/mp4; codecs="mp4a.40.2"');
          fetch(videoUrl)
            .then(response => response.arrayBuffer())
            .then(data => videoSourceBuffer.appendBuffer(data));
          fetch(audioUrl)
            .then(response => response.arrayBuffer())
            .then(data => audioSourceBuffer.appendBuffer(data));
        });
      } else { console.error('MSE or required codecs are not supported in browser, or Ladle has encountered a parsing error.'); }
    }); </script>""")

    def get_gallery_code(self, link_carousel: list[str]):
        images = "\n".join([f"<img src={img_link} {self.image_tags}/>" for img_link in link_carousel])
        javascript = """<script>document.addEventListener('DOMContentLoaded', () => {
    const slider = document.querySelector('.slider'); const images = slider.querySelectorAll('img');
    const prevButton = document.querySelector('.prevSlide'); const nextButton = document.querySelector('.nextSlide');
    let slideIndex = 0;
    function showSlide(n)  {
      if (n >= images.length) { slideIndex = 0;  }
      if (n < 0) { slideIndex = images.length - 1; }
      for (let i = 0; i < images.length; i++) {
        images[i].classList.remove('activeSlide');
      }
      images[slideIndex].classList.add('activeSlide'); 
    }
    prevButton.addEventListener('click', () => {
      showSlide(slideIndex -= 1);   });
    nextButton.addEventListener('click', () => {
      showSlide(slideIndex += 1); });
    showSlide(slideIndex); }); </script>"""
        return images + "\n" + javascript
