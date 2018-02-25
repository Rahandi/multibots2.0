import requests, pafy
from bs4 import BeautifulSoup, SoupStrainer

class YoutubeApi():
    def __init__(self, bots):
        self.bot = bots

    def Search(self, token, query):
        try:
            query = query.replace(' ', '+')
            link = 'https://www.youtube.com/results?search_query=' + query
            page = requests.get(link).text
            prefered = SoupStrainer('a', {'rel':'spf-prefetch'})
            soup = BeautifulSoup(page, 'lxml', parse_only=prefered)
            url, title, videoid = [], [], []
            for a in soup.find_all('a', {'rel':'spf-prefetch'}):
                if '/watch?' in a['href']:
                    hitung += 1
                    title.append(a['title'])
                    url.append('https://youtube.com' + str(a['href']) + '&t')
                    videoid.append(a['href'].replace('/watch?v=', ''))
                    if len(videoid) >= 10:
                        break
            TB = []
            for a in range(0, 10):
                isi_TB = {
                    'thumbnail': 'https://img.youtube.com/vi/%s/hqdefault.jpg' % videoid[a],
                    'title': None,
                    'text': str(title[a])[:60],
                    'action': self.bot.actionBuilder(3, ['msg', 'msg', 'msg'], ['send Video', 'send Audio', 'download'], ['/youtube-video: %s' % (url[a]), '/youtube-audio: %s' % (url[a]), '/youtube-download: %s' % (url[a])])
                }
                TB.append(isi_TB)
            data = {
                'alt': 'Multi_Bots YoutubeSearch',
                'template': self.bot.templateBuilder(10, 'tmp', TB)
            }
            self.bot.replyCarrousel(token, data)
        except Exception as e:
            raise e

    def VideoBest(self, token, link):
        try:
            pafyObj = pafy.new(link)
            video = pafyObj.getbest(preftype='mp4')
            url = video.url
            thumbnail = 'https://img.youtube.com/vi/%s/mqdefault.jpg' % (pafyObj.videoid)
            self.bot.replyVideo(token, url, thumbnail)
        except Exception as e:
            raise e

    def AudioBest(self, token, link):
        try:
            pafyObj = pafy.new(link)
            audio = pafyObj.getbestaudio(preftype='m4a')
            self.bot.replyAudio(token, audio.url)
        except Exception as e:
            raise e

    def Download(self, token, link):
        try:
            pafyObj = pafy.new(link)
            data = {
                'alt': 'Multi_Bots YoutubeDownload',
                'thumbnail': 'https://img.youtube.com/vi/%s/hqdefault.jpg' % pafyObj.videoid,
                'title': None,
                'text': str(pafyObj.title)[:60],
                'action': self.bot.actionBuilder(2, ['msg', 'msg'], ['download Video', 'download Audio'], ['/youtube-download-video: %s' % (link), '/youtube-download-audio: %s' % (link)])
            }
            self.bot.replyButtons(token, data)
        except Exception as e:
            raise e

    def VideoDownloadLink(self, token, link):
        try:
            pafyObj = pafy.new(link)
            thumbnail = 'https://img.youtube.com/vi/%s/mqdefault.jpg' % (pafyObj.videoid)
            videolist = pafyObj.streams
            text = '『Youtube Download Video』\n'
            for obj in videolist:
                text += '\n%s' % (str(obj.resolution.split('x')[1]) + 'p')
                text += ' %s' % (obj.extensions)
                text += ' %s' % (humansize(obj.get_filesize()))
                text += '\n%s\n' % (shorten(obj.url))
            custom = [
                self.bot.imageMessage(thumbnail),
                self.bot.textMessage(str(text))
            ]
            self.bot.replyCustom(token, custom)
        except Exception as e:
            raise e

    def AudioDownloadLink(self, token, link):
        try:
            pafyObj = pafy.new(link)
            thumbnail = 'https://img.youtube.com/vi/%s/mqdefault.jpg' % (pafyObj.videoid)
            audiolist = pafyObj.audiostreams
            text = '『Youtube Download Audio』\n'
            for obj in audiolist:
                text += '\n%s' % (obj.extension)
                text += ' %s' % (obj.bitrate)
                text += ' %s' % (humansize(obj.get_filesize()))
                text += '\n%s\n' % (shorten(obj.url))
            custom = [
                self.bot.imageMessage(thumbnail),
                self.bot.textMessage(str(text))
            ]
            self.bot.replyCustom(token, custom)
        except Exception as e:
            raise e

    def humansize(self, nbytes):
        try:
            i = 0
            suffixes = ['B', 'KB', 'MB', 'GB', 'TB', 'PB']
            while nbytes >= 1024 and i < len(suffixes)-1:
                nbytes /= 1024.
                i += 1
            f = ('%.2f' % nbytes).rstrip('0').rstrip('.')
            return '%s %s' % (f, suffixes[i])
        except Exception as e:
            raise e

    def shorten(url):
        api_key = 'AIzaSyB2JuzKCAquSRSeO9eiY6iNE9RMoZXbrjo'
        req_url = 'https://www.googleapis.com/urlshortener/v1/url?key=' + api_key
        payload = {'longUrl': url}
        headers = {'content-type': 'application/json'}
        r = requests.post(req_url, data=json.dumps(payload), headers=headers)
        resp = json.loads(r.text)
        return resp['id']