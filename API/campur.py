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
            raise e