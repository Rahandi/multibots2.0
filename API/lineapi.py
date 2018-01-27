from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import *

class LineAPI():
    def __init__(self, code):
        self.bot = LineBotApi(code)

    def replyText(self, token, text):
        try:
            return self.bot.reply_message(token, TextSendMessage(text=text))
        except Exception as e:
            raise e

    def replyImage(self, token, url):
        try:
            return self.bot.reply_message(token, ImageSendMessage(original_content_url=url, preview_image_url=url))
        except Exception as e:
            raise e

    def replyAudio(self, token, url, duration=1):
        try:
            return self.bot.reply_message(token, AudioSendMessage(original_content_url=url, duration=duration))
        except Exception as e:
            raise e

    def replyVideo(self, token, url, thumbnail):
        try:
            return self.bot.reply_message(token, VideoSendMessage(original_content_url=url, preview_image_url=thumbnail))
        except Exception as e:
            raise e

    def replyLocation(self, token, title, address, lat, lng):
        try:
            return self.bot.reply_message(token, LocationSendMessage(title=title, address=address, latitude=lat, longitude=lng))
        except Exception as e:
            raise e

    def replyCarrousel(self, token, data):
        try:
            return self.bot.reply_message(token, TemplateSendMessage(alt_text=data['alt'], template=data['template']))
        except Exception as e:
            raise e

    def replySticker(self, token, package, sticker):
        try:
            return self.bot.reply_message(token, StickerSendMessage(package_id=str(package), sticker_id=str(sticker)))
        except Exception as e:
            raise e

    def replyButtons(self, token, data):
        try:
            return self.bot.reply_message(token, TemplateSendMessage(alt_text=data['alt'], template=ButtonsTemplate(thumbnail_image_url = data['thumbnail'], title = data['title'], text = data['text'], actions = data['action'])))
        except Exception as e:
            raise e

    def replyConfirm(self, token, data):
        try:
            return self.bot.reply_message(token, TemplateSendMessage(alt_text=data['alt'], template=ConfirmTemplate(text=data['text'], actions=data['action'])))
        except Exception as e:
            raise e

    def replyCustom(self, token, custom):
        try:
            return self.bot.reply_message(token, custom)
        except Exception as e:
            raise e

    def textMessage(self, text):
        return TextSendMessage(text=text)

    def imageMessage(self, url):
        return ImageSendMessage(original_content_url=url, preview_image_url=url)

    def audioMessage(self, url, duration=1):
        return AudioSendMessage(original_content_url=url, duration=duration)

    def videoMessage(self, url, thumbnail):
        return VideoSendMessage(original_content_url=url, preview_image_url=thumbnail)

    def locationMessage(self, title, address, lat lng):
        return LocationSendMessage(title=title, address=address, latitude=lat, longitude=lng)

    def templateMessage(self, data):
        return TemplateSendMessage(alt_text=data['alt'], template=data['template'])

    def stickerMessage(self, package, sticker):
        return StickerSendMessage(package_id=str(package), sticker_id=str(sticker))

    def getProfile(self, userID):
        try:
            return self.bot.get_profile(userID)
        except Exception as e:
            raise e

    def leaveGroup(self, groupID):
        try:
            return self.bot.leave_group(groupID)
        except Exception as e:
            raise e

    def leaveRoom(self, roomID):
        try:
            return self.bot.leave_room(roomID)
        except Exception as e:
            raise e

    def getContent(self, messageID):
        try:
            return self.bot.get_message_content(messageID)
        except Exception as e:
            raise e

    def actionBuilder(self,amount, type, param1, param2):
        try:
            built = []
            for i in range(0, amount):
                if type[i] == 'msg':
                    ap = MessageTemplateAction(label=param1[i], text=param2[i])
                elif type[i] == 'uri':
                    ap = URITemplateAction(label=param1[i], uri=param2[i])
                elif type[i] == 'pbk':
                    ap = PostbackTemplateAction(label=param1[i], data=param2[i])
                built.append(ap)
            return built
        except Exception as e:
            raise e

    def templateBuilder(self, amount, type, data):
        try:
            colum = []
            for i in range(0, amount):
                if type =='tmp':
                    ap = CarouselColumn(
                        thumbnail_image_url=data[i]['thumbnail'],
                        title=data[i]['title'],
                        text=data[i]['text'],
                        actions=data[i]['action']
                    )
                elif type == 'img':
                    ap = ImageCarouselColumn(
                        image_url=data[i]['thumbnail'],
                        action=data[i]['action']
                    )
                colum.append(ap)
            if type == 'tmp':
                return CarouselTemplate(columns=colum)
            elif type == 'img':
                return ImageCarouselTemplate(columns=colum)
        except Exception as e:
            raise e