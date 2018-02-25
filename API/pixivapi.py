from pixivpy3 import *

class PixivAPI:
    def __init__(self, username, password, bots):
        self.api = PixivAPI()
        self.api.login(username, password)
        self.bot = bots

    def search(self, token, query):
        try:
            data = self.api.search_works(query=query, page=1, per_page=10, mode='tag')
            TB = []
            for a in data.response:
                isi_TB = {}
                img = a.image_urls.px_480mw
                isi_TB['thumbnail'] = img
                isi_TB['action'] = self.bot.actionBuilder(1, ['uri'], ['direct link'], [img])
                TB.append(isi_TB)
            data = {
                'alt': 'Multi_Bots PixivSearch',
                'template': self.bot.templateBuilder(len(TB), 'img', TB)
            }
            self.bot.replyCarrousel(token, data)
        except Exception as e:
            raise e

    def ranking(self, token):
        try:
            data = self.api.ranking(page=1, per_page=10)
            TB = []
            for a in data.response[0].works:
                isi_TB = {}
                image = a.work.image_urls.px_480mw.replace('http://', 'https://')
                isi_TB['thumbnail'] = image
                isi_TB['action'] = self.bot.actionBuilder(1, ['uri'], ['Rank %s' % (a+1)], [image])
                TB.append(isi_TB)
            data = {
                'alt' : 'Multi_Bots PixivRank',
                'template' : self.bot.templateBuilder(len(TB), 'img', TB)
            }
            self.bot.replyCarrousel(token, data)
        except Exception as e:
            raise e