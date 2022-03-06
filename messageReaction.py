#봇이 해주는 반응 변수들 반환해주는 것 embed는 여기x
from dataclasses import dataclass
@dataclass
class Emoticon:
    message: str = None
    imgUrl: str = None

emoticonList = [
    Emoticon( "!감정 분노" , "https://cdn-lostark.game.onstove.com/2021/event/210331_event/images/emoticon/emoticon_4.png"),
    Emoticon( "!감정 미안" , "https://cdn-lostark.game.onstove.com/2021/event/210331_event/images/emoticon/emoticon_3.png"),
    Emoticon( "!감정 좌절" , "https://cdn-lostark.game.onstove.com/2021/event/210331_event/images/emoticon/emoticon_8.png"),
    Emoticon( "!감정 환영" , "https://cdn-lostark.game.onstove.com/2021/event/210331_event/images/emoticon/emoticon_13.png"),
    Emoticon( "!감정 기대" , "https://cdn-lostark.game.onstove.com/2021/event/210331_event/images/emoticon/emoticon_14.png"),
    Emoticon( "!감정 탈출" , "https://cdn-lostark.game.onstove.com/2021/event/210331_event/images/emoticon/emoticon_15.png"),
    Emoticon( "!감정 신나" , "https://cdn-lostark.game.onstove.com/2021/event/210331_event/images/emoticon/emoticon_6.png"),
    Emoticon( "!감정 안녕" , "https://cdn-lostark.game.onstove.com/2021/event/210331_event/images/emoticon/emoticon_1.png"),
    Emoticon( "!감정 사랑해" , "https://cdn-lostark.game.onstove.com/2021/event/210331_event/images/emoticon/emoticon_2.png"),
]

def isReaction(message, textlist):
    for index in range(len(textlist)):
        if  textlist[index] in message:  
            return True
    return False

def get_emoticon_img_url(message):
    for emoticon in emoticonList:
        if emoticon.message == message:
            return emoticon.imgUrl
    return None

def get_all_emoticon_message_list():
    messageList = []
    for emoticon in emoticonList:
        messageList.append(emoticon.message)
    return messageList
