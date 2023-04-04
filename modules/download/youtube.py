from pytube import YouTube

class YoutubeDownloader:
    def __init__(self,Link):
      self.url = Link

    async def youtube_download(self):
        try:
            return YouTube(self.url).streaming_data
        except Exception as ex:
            print(ex)
            return False
      
