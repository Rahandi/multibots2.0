import requests
from campur import Campur

class InstagramAPI():
    def __init__(self, bots):
        self.bot = bots
        self.campur = Campur()

    def Post(self, token, username, urutan):
        try:
            link = 'http://rahandiapi.herokuapp.com/instapost/%s/%s?key=randi123' % (username, urutan)
            data = requests.get(link).json()
            if data['find'] == True:
                if data['see'] == True:
                    if data['banyak'] == True:
                        data = data['media']
                        madiatype = data['mediatype']
                        text = data['caption'] + '\n\nlike: {}\ncomment: {}'.format(data['like_count'], data['comment_count'])
                        if mediatype == 1:
                            text += '\ndirect link: {}'.format(campur.shorten(data['url']))
                            custom = [self.bot.imageMessage(data['url'])]
                        elif mediatype == 2:
                            text += '\ndirect link: {}'.format(campur.shorten(data['url']))
                            custom = [self.bot.videoMessage(data['url'], data['preview'])]
                        elif mediatype == 8:
                            urllist = data['url']
                            TB = []
                            for a in urllist:
                                isi_TB = {}
                                mediatype = a['mediatype']
                                if mediatype == 1:
                                    isi_TB['thumbnail'] = a['url']
                                    isi_TB['action'] = self.bot.actionBuilder(1, ['uri'], ['image'], [a['url']])
                                elif mediatype == 2:
                                    isi_TB['thumbnail'] = a['preview']
                                    isi_TB['action'] = self.bot.actionBuilder(1, ['uri'], ['video'], [a['url']])
                                TB.append(isi_TB)
                            passing = {
                                'alt':'Multi_Bots Instapost',
                                'template':self.bot.templateBuilder(len(urllist), 'img', TB)
                            }
                            custom = [self.bot.templateMessage(passing)]
                        custom.append(self.bot.textMessage(text))
                        self.bot.replyCustom(token, custom)
                    else:
                        self.bot.replyText(token, 'Jumlah post dalam akun {} tidak mencapai {} post'.format(username, urutan))
                else:
                    self.bot.replyText(token, 'Akun {} di private, akan mencoba mem-follow'.format(username))
            else:
                self.bot.replyText(token, 'Akun {} tidak ditemukan'.format(username))
        except Exception as e:
            raise 'instagramapi:Post:' + e

    def Story(self, token, username):
        try:
            link = 'http://rahandiapi.herokuapp.com/instastory/%s?key=randi123' % (username)
            data = requests.get(link).json()
            if data['find'] == True:
                if len(data['url']) == 0:
                    if data['reason'] == 1:
                        self.bot.replyText(token, 'Akun {} tidak memiliki story'.format(username))
                    elif data['reason'] == 2:
                        self.bot.replyText(token, 'Akun {} private, akan mencoba mem-follow'.format(username))
                    else:
                        self.bot.replyText(token, 'Unknown error')
                else:
                    urllist = data['url']
                    TB = []
                    for a in urllist:
                        mediatype = a['tipe']
                        isi_TB = {}
                        if mediatype == 1:
                            isi_TB['thumbnail'] = a['link']
                            isi_TB['action'] = self.bot.actionBuilder(1, ['uri'], ['image'], [a['link']])
                        elif mediatype == 2:
                            isi_TB['thumbnail'] = a['preview']
                            isi_TB['action'] = self.bot.actionBuilder(1, ['uri'], ['video'], [a['link']])
                        TB.append(isi_TB)
                        if len(TB) >= 50:
                            break
                    TB = [TB[i:i+10] for i in range(0, len(TB), 10)]
                    custom = []
                    for a in TB:
                        sendlist = {
                            'alt':'Multi_Bots Instastory',
                            'template':self.bot.templateBuilder(len(a), 'img', a)
                        }
                        custom.append(self.bot.templateMessage(sendlist))
                    self.bot.replyCustom(token, custom)
            else:
                self.bot.replyText(token, 'Akun {} tidak ditemukan'.format(username))
        except Exception as e:
            raise 'instagramapi:Story:' + e

    def Info(self, token, username):
        try:
            link = 'https://rahandiapi.herokuapp.com/instainfo/%s?key=randi123' % (str(username))
            data = requests.get(link).json()
            if data['find'] == True:
                data = data['result']
                kata = '『Instagram Info』\n\n'
                kata += 'Username: ' + result['username']
                kata += '\nName: ' + result['name']
                kata += '\nTotal post: ' + str(result['mediacount'])
                kata += '\nFollower: ' + str(result['follower'])
                kata += '\nFollowing: ' + str(resul['following'])
                kata += '\nPrivate: ' + str(result['private'])
                kata += '\nBio: ' + str(result['bio'])
                self.bot.replyCustom(token, [
                        self.bot.imageMessage(data['url']),
                        self.bot.textMessage(str(kata))
                    ])
            else:
                self.bot.replyText(token, 'Akun {} tidak ditemukan'.format(username))
        except Exception as e:
            raise 'instagramapi:Info:' + e