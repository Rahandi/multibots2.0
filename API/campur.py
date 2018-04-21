import requests

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
            raise 'campur:sholat:' + e

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
            raise 'campur:shortener' + e

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