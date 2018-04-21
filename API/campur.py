#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests, json, random, wikipedia
from bs4 import BeautifulSoup, SoupStrainer

class Campur():
    def __init__(self, bots):
        self.bot = bots

    def sholat(self, token, posisi=None, lat=None, lng=None):
        try:
            if posisi != None:
                link = 'http://time.siswadi.com/pray/' + str(requests.utils.requote_uri(posisi))
                data = requests.get(link).json()
                kata = '『Jadwal Sholat』\n'
                kata += '\nShubuh: %s\nAshar: %s\nMaghrib: %s\nIsya: %s' % (data['data']['Fajr'], data['data']['Dhuhr'], data['data']['Asr'], data['data']['Maghrib'], data['data']['Isha'])
                self.bot.replyText(token, kata)
            elif lat != None and lng != None:
                link = 'https://time.siswadi.com/pray/?lat=%s&lng=%s' % (lat, lng)
                data = requests.get(link).json()
                kata = '『Jadwal Sholat』\n'
                kata += '\nShubuh: %s\nAshar: %s\nMaghrib: %s\nIsya: %s' % (data['data']['Fajr'], data['data']['Dhuhr'], data['data']['Asr'], data['data']['Maghrib'], data['data']['Isha'])
                self.bot.replyText(token, kata)
            else:
                self.bot.replyText(token, 'Error')
        except Exception as e:
            raise e

    def shortener(self, url, direct=0):
        try:
            if direct == 0:
                api_key = 'AIzaSyB2JuzKCAquSRSeO9eiY6iNE9RMoZXbrjo'
                req_url = 'https://www.googleapis.com/urlshortener/v1/url?key=' + api_key
                payload = {'longUrl': url}
                headers = {'content-type': 'application/json'}
                r = requests.post(req_url, data=json.dumps(payload), headers=headers)
                resp = json.loads(r.text)
                return resp['id']
            else:
                pass
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

    def googleimage(self, token, query):
        try:
            link = 'https://www.google.co.id/search?q=' + query.replace(' ', '+') +'&dcr=0&source=lnms&tbm=isch&sa=X&ved=0ahUKEwje9__4z6nXAhVMKY8KHUFCCbwQ_AUICigB&biw=1366&bih=672'
            headers = {
                "User-Agent":"Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"
            }
            data = requests.get(link, headers=headers)
            data = data.text.encode('utf-8').decode('ascii', 'ignore')
            filtered = SoupStrainer('div', {'class':'rg_meta notranslate'})
            soup = BeautifulSoup(data, 'lxml', parse_only = filtered)
            piclist = []
            for a in soup.find_all('div', {'class':'rg_meta notranslate'}):
                try:
                    jsonnya = json.loads(str(a.text))
                    piclist.append(jsonnya['ou'])
                except Exception as e:
                    raise e
            TB = []
            random.shuffle(piclist)
            for a in range(10):
                isi_TB = {}
                if 'https://' in piclist[a]:
                    isi_TB['thumbnail'] = piclist[a]
                else:
                    isi_TB['thumbnail'] = shortener(piclist[a])
                isi_TB['action'] = self.bot.actionBuilder(1, ['uri'], ['direct link'], [piclist[a]])
                TB.append(isi_TB)
            passing = {
                "alt":"Multi_Bots GoogleImages",
                "template":self.bot.templateBuilder(len(TB), 'img', TB)
            }
            self.bot.replyCarrousel(token, passing)
        except Exception as e:
            raise e

    def wikiped(self, token, query):
        try:
            image = None
            wikipedia.set_lang('id')
            hasil = wikipedia.summary(query, sentences=3)
            link = wikipedia.page(query).url
            data = requests.get(link).text
            soup = BeautifulSoup(data, 'lxml')
            for a in soup.find_all('meta', {'property':'og:image'}):
                image = a['content']
            if image != None:
                self.bot.replyCustom(token, [
                        self.bot.imageMessage(image),
                        self.bot.textMessage(str(hasil))
                    ])
            else:
                self.bot.replyText(token, str(hasil))
        except Exception as e:
            raise e

    def lyriclagu(self, token, query):
        try:
            query = requests.utils.requote_uri(query)
            link = 'http://rahandiapi.herokuapp.com/lyricapi?key=randi123&q=' + query
            data = json.loads(requests.get(link).text)
            if data['find'] == True:
                kata = data['title'] + '\n\n'
                kata += data['lyric']
                if len(kata) <= 2000:
                    self.bot.replyText(token, str(kata))
                else:
                    kata = [kata[i:i+2000] for i in range(0, len(kata), 2000)]
                    custom = []
                    for a in kata:
                        custom.append(self.bot.textMessage(str(a)))
                        if len(custom) >= 5:
                            break
                    self.bot.replyCustom(token, custom)
        except Exception as e:
            raise e

    def sendGif(self, token, query):
        try:
            link = 'https://api.tenor.com/v1/search?key=LIVDSRZULELA&q=%s&limit=1' % (query)
            data = json.loads(requests.get(link).text)
            giff = data['result'][0]['media'][0]['gif']['url']
            TB = [
                {
                    "thumbnail":giff,
                    "action":self.bot.actionBuilder(1, ['uri'], ['direct link'], [giff])
                }
            ]
            passing = {
                "alt":"Multi_Bots Gif",
                "template":self.bot.templateBuilder(1, 'img', TB)
            }
            self.bot.replyCarrousel(token, passing)
        except Exception as e:
            raise e

    def chatbot(self, token, query):
        try:
            query = requests.utils.requote_uri(query)
            link = 'http://api.ntcorp.us/chatbot/v1/?text=%s&key=beta1.nt&local=id' % (query)
            data = json.loads(requests.get(link).text)
            if data['result']['result'] == 100:
                realresp = data['result']['response']
                self.bot.replyText(token, str(realresp))
            else:
                self.bot.replyText(token, 'error')
        except Exception as e:
            raise e

    def gaul(token, query):
        try:
            pass
        except Exception as e:
            raise e