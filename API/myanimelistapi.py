import requests
from bs4 import BeautifulSoup

class MyAnimeListAPI:
    def __init__(self, bots):
        self.bot = bots

    def getTopAiring(self, token):
        try:
            link = 'https://myanimelist.net/'
            data = requests.get(link).text
            soup = BeautifulSoup(data, 'lxml')
            img = []
            judul = []
            link = []
            for a in soup.find_all('div', {'class':'ranking-digest'}):
                for b in a.find_all('h2', {'class':'ranking-header'}):
                    if b.text[4:] == 'Top Airing Anime':
                        for c in a.find_all('img'):
                            img.append(c['data-src'].replace('/r/50x70', ''))
                        for c in a.find_all('a', {'class':'title'}):
                            judul.append(c.text)
                            link.append(c['href'])
            TB = []
            for a in range(len(img)):
                isi_TB = {}
                isi_TB['thumbnail'] = img[a]
                isi_TB['title'] = judul[a][:40]
                isi_TB['text'] = 'Rank %s' % (int(a)+1)
                isi_TB['action'] = self.bot.actionBuilder(3, ['postback', 'uri', 'postback'], ['Description', 'MAL Page', 'Promotional Video'], ['anidesc %s' % (link[a]), link[a], 'anipv %s/video' % (link[a])])
                TB.append(isi_TB)
            data = {
                'alt': 'Multi_Bots TopAiringAnime',
                'template': self.bot.templateBuilder(len(img), 'tmp', TB)
            }
            self.bot.replyCarrousel(token, data)
        except Exception as e:
            raise e

    def getTopUpcoming(self, token):
        try:
            link = 'https://myanimelist.net/'
            data = requests.get(link).text
            soup = BeautifulSoup(data, 'lxml')
            img = []
            judul = []
            link = []
            for a in soup.find_all('div', {'class':'ranking-digest'}):
                for b in a.find_all('h2', {'class':'ranking-header'}):
                    if b.text[4:] == 'Top Upcoming Anime':
                        for c in a.find_all('img'):
                            img.append(c['data-src'].replace('/r/50x70', ''))
                        for c in a.find_all('a', {'class':'title'}):
                            judul.append(c.text)
                            link.append(c['href'])
            TB = []
            for a in range(len(img)):
                isi_TB = {}
                isi_TB['thumbnail'] = img[a]
                isi_TB['title'] = judul[a][:40]
                isi_TB['text'] = 'Rank %s' % (int(a)+1)
                isi_TB['action'] = self.bot.actionBuilder(3, ['postback', 'uri', 'postback'], ['Description', 'MAL Page', 'Promotional Video'], ['anidesc %s' % (link[a]), link[a], 'anipv %s/video' % (link[a])])
                TB.append(isi_TB)
            data = {
                'alt': 'Multi_Bots TopUpcomingAnime',
                'template': self.bot.templateBuilder(len(img), 'tmp', TB)
            }
            self.bot.replyCarrousel(token, data)
        except Exception as e:
            raise e
        

    def getMostPopular(self, token):
        try:
            link = 'https://myanimelist.net/'
            data = requests.get(link).text
            soup = BeautifulSoup(data, 'lxml')
            img = []
            judul = []
            link = []
            for a in soup.find_all('div', {'class':'ranking-digest'}):
                for b in a.find_all('h2', {'class':'ranking-header'}):
                    if b.text[4:] == 'Most Popular Anime':
                        for c in a.find_all('img'):
                            img.append(c['data-src'].replace('/r/50x70', ''))
                        for c in a.find_all('a', {'class':'title'}):
                            judul.append(c.text)
                            link.append(c['href'])
            TB = []
            for a in range(len(img)):
                isi_TB = {}
                isi_TB['thumbnail'] = img[a]
                isi_TB['title'] = judul[a][:40]
                isi_TB['text'] = 'Rank %s' % (int(a)+1)
                isi_TB['action'] = self.bot.actionBuilder(3, ['postback', 'uri', 'postback'], ['Description', 'MAL Page', 'Promotional Video'], ['anidesc %s' % (link[a]), link[a], 'anipv %s/video' % (link[a])])
                TB.append(isi_TB)
            data = {
                'alt': 'Multi_Bots MostPopularAnime',
                'template': self.bot.templateBuilder(len(img), 'tmp', TB)
            }
            self.bot.replyCarrousel(token, data)
        except Exception as e:
            raise e
        

    def detailAnime(self, token, link):
        try:
            kembali = {}
            data = requests.get(link).text
            soup = BeautifulSoup(data, 'lxml')
            custom = []
            kembali['judul'] = soup.find('span', {'itemprop':'name'}).text
            custom.append(self.bot.imageMessage(soup.find('img', {'class':'ac'})['src']))
            kembali['score'] = soup.find('div', {'data-title':'score'}).text[9:-7]
            kembali['rank'] = soup.find('span', {'class':'numbers ranked'}).text
            kembali['popularity'] = soup.find('span', {'class':'numbers popularity'}).text
            kembali['description'] = soup.find('span', {'itemprop':'description'}).text
            teks = '%s\n\nScore %s\n%s\n%s\n\n%s' % (kembali['judul'], kembali['score'], kembali['rank'], kembali['popularity'], kembali['description'])
            custom.append(self.bot.textMessage(teks))
            self.replyCustom(token, custom)
        except Exception as e:
            raise e

    def videoAnime(self, token, link):
        try:
            kembali = []
            ytid = []
            judul = []
            TB = []
            data = requests.get(link).text
            soup = BeautifulSoup(data, 'lxml')
            for a in soup.find_all('div', {'class':'video-list-outer po-r pv'}):
                text = a.find('a')['href']
                text = text[:text.find('?enablejsapi')]
                text = text.replace('embed/', 'watch?v=')
                judul.append(a.find('span', {'class':'title'}).text)
                kembali.append(text)
                ytid.append(text[text.find('?v=')+3:])
            if len(kembali) == 0:
                self.bot.replyText(token, '0 promotional video')
            else:
                for a in range(len(kembali)):
                    isi_TB = {}
                    isi_TB['thumbnail'] = 'https://img.youtube.com/vi/%s/hqdefault.jpg' % ytid[a]
                    isi_TB['title'] = None
                    isi_TB['text'] = judul[a][:60]
                    isi_TB['action'] = self.bot.actionBuilder(3, ['msg', 'msg', 'msg'], ['send Video', 'send Audio', 'download'], ['/youtube-video: %s' % (kembali[a]), '/youtube-audio: %s' % (kembali[a]), '/youtube-download: %s' % (kembali[a])])
                    TB.append(isi_TB)
                    if len(TB) >= 50:
                        break
                TB = [TB[i:i+10] for i in range(0, len(TB), 10)]
                custom = []
                for a in TB:
                    custom.append(TemplateSendMessage(alt_text = 'Multi_Bots MAL Promotional Video', template = templateBuilder(len(a), 'tmp', a)))
                self.bot.replyCustom(token, custom)
        except Exception as e:
            raise e

    def searchAnime(self, token, query):
        try:
            query = requests.utils.requote_uri(query)
            link =  'https://myanimelist.net/search/all?q=%s' % (query)
            data = requests.get(link).text
            soup = BeautifulSoup(data, 'lxml')
            image = []
            judul = []
            link = []
            for a in soup.find_all('div', {'class':'list di-t w100'}):
                img = a.find('img')
                if '/anime/' in img['src']:
                    image.append(img['src'].replace('/r/100x140', ''))
                    judul.append(img['alt'])
                    link.append(a.find('a')['href'])
            TB = []
            for a in range(len(img)):
                isi_TB = {}
                isi_TB['thumbnail'] = image[a]
                isi_TB['title'] = None
                isi_TB['text'] = judul[a][:60]
                isi_TB['action'] = self.bot.actionBuilder(3, ['postback', 'uri', 'postback'], ['Description', 'MAL Page', 'Promotional Video'], ['anidesc %s' % (link[a]), link[a], 'anipv %s/video' % (link[a])])
                TB.append(isi_TB)
            data = {
                'alt' : 'Multi_Bots AnimeSearch',
                'template' : self.bot.templateBuilder(len(img), 'tmp', TB)
            }
            self.bot.replyCarrousel(token, data)
        except Exception as e:
            raise e