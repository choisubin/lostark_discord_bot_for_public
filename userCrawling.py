#유저 정보 크롤링 관련
import discord, asyncio
import requests
import re

import chromedriverSetting

from dataclasses import dataclass
from bs4 import BeautifulSoup
from selenium import webdriver

url_loawa = "https://lostark.game.onstove.com/Profile/Character/"

@dataclass
class UserList:
    server: str = None
    guild: str = None
    uclass: str = None
    uclassimg: str = None
    title: str = None
    level: str = None
    itemlevel: str = None
    Expeditionlevel: str = None
    pvp: str = None
    land: str = None

    heart: str = None
    star: str = None
    giant: str = None
    art: str = None
    seed: str = None
    adventure: str = None
    token: str = None
    leaf: str = None

    power: str = None
    hp: str = None
    cri: str = None
    spe: str = None
    over: str = None
    speed: str = None
    pat: str = None
    prof: str = None

    specialPassive: list = None
       
userlist = UserList()

def update_char(uName):
    chromedriverSetting.driver.get(url_loawa + uName)
    chromedriverSetting.driver.implicitly_wait(30)

    html = chromedriverSetting.driver.page_source
    chromedriverSetting.driver.quit()
    soup = BeautifulSoup(html, "html.parser")
    update_UserList(soup)

def update_UserList(soup):
    # 서버
    temp = soup.find(attrs={'class':'profile-character-info__server'}).text
    temp = re.sub("@","", temp)
    userlist.server = temp
    # 길드
    temp = soup.find(attrs={'class':'game-info__guild'}).text
    temp = re.sub("길드","", temp)
    userlist.guild = temp
    # 클래스
    temp = soup.find(attrs={'class':'profile-character-info__img'})['alt']
    userlist.uclass = temp
    # 클래스 이미지
    temp = soup.find(attrs={'class':'profile-character-info__img'})['src']
    userlist.uclassimg = temp
    # 칭호
    temp = soup.find(attrs={'class':'game-info__title'}).text
    temp = re.sub("칭호","", temp)
    userlist.title = temp
    # 전투 레벨
    temp = soup.find(attrs={'class':'level-info__item'}).text
    temp = re.sub("전투 레벨","", temp)
    userlist.level = temp
    # 아이템 레벨
    temp = soup.find(attrs={'class':'level-info2__expedition'}).text
    temp = re.sub("장착 아이템 레벨","", temp)
    userlist.itemlevel = temp
    # 원정대
    temp = soup.find(attrs={'class':'level-info__expedition'}).text
    temp = re.sub("원정대 레벨","", temp)
    userlist.Expeditionlevel = temp
    # PVP
    temp = soup.find(attrs={'class':'level-info__pvp'}).text
    temp = re.sub("PVP","", temp)
    userlist.pvp = temp
    # 영지
    temp = soup.find(attrs={'class':'game-info__wisdom'}).text
    temp = re.sub("영지","", temp)
    userlist.land = temp

    # 섬의 마음
    temp = soup.find(attrs={'id':'lui-tab1-1'}).find(attrs={'class':'count'}).text
    temp = re.sub("개","", temp)
    userlist.heart = temp
    # 오르페우스의 별
    temp = soup.find(attrs={'id':'lui-tab1-2'}).find(attrs={'class':'count'}).text
    temp = re.sub("개","", temp)
    userlist.star = temp
    # 거인의 심장
    temp = soup.find(attrs={'id':'lui-tab1-3'}).find(attrs={'class':'count'}).text
    temp = re.sub("개","", temp)
    userlist.giant = temp
    # 위대한 미술품
    temp = soup.find(attrs={'id':'lui-tab1-4'}).find(attrs={'class':'count'}).text
    temp = re.sub("개","", temp)
    userlist.art = temp
    # 모코코 씨앗
    temp = soup.find(attrs={'id':'lui-tab1-5'}).find(attrs={'class':'count'}).text
    temp = re.sub("개","", temp)
    userlist.seed = temp
    # 향해 모험물
    temp = soup.find(attrs={'id':'lui-tab1-6'}).find(attrs={'class':'count'}).text
    temp = re.sub("개","", temp)
    userlist.adventure = temp
    # 이그네아의 징표
    temp = soup.find(attrs={'id':'lui-tab1-7'}).find(attrs={'class':'count'}).text
    temp = re.sub("개","", temp)
    userlist.token = temp
    # 세계수의 잎
    temp = soup.find(attrs={'id':'lui-tab1-8'}).find(attrs={'class':'count'}).text
    temp = re.sub("개","", temp)
    userlist.leaf = temp

    # 공격력
    tempStr = soup.find(attrs={'class':'profile-ability-basic'}).find_all('span')
    num = 0
    for ability in tempStr:
        num = num + 1
        if ability.text == "공격력":
            break
    temp = tempStr[num].text
    userlist.power = temp
    # 체력
    num = 0
    for ability in tempStr:
        num = num + 1
        if ability.text == "최대 생명력":
            break
    temp = tempStr[num].text
    userlist.hp = temp

    # # 치명
    tempStr = soup.find(attrs={'class':'profile-ability-battle'}).find_all('span')
    num = 0
    for ability in tempStr:
        num = num + 1
        if ability.text == "치명":
            break
    temp = tempStr[num].text
    userlist.cri = temp
    # 특화
    num = 0
    for ability in tempStr:
        num = num + 1
        if ability.text == "특화":
            break
    temp = tempStr[num].text
    userlist.spe = temp
    # 제압
    num = 0
    for ability in tempStr:
        num = num + 1
        if ability.text == "제압":
            break
    temp = tempStr[num].text
    userlist.over = temp
    # 신속
    num = 0
    for ability in tempStr:
        num = num + 1
        if ability.text == "신속":
            break
    temp = tempStr[num].text
    userlist.speed = temp
    # 인내
    num = 0
    for ability in tempStr:
        num = num + 1
        if ability.text == "인내":
            break
    temp = tempStr[num].text
    userlist.pat = temp
    # 숙련
    num = 0
    for ability in tempStr:
        num = num + 1
        if ability.text == "숙련":
            break
    temp = tempStr[num].text
    userlist.prof = temp

    # 각인
    tempStr = soup.find_all(attrs={'class':'swiper-wrapper'})[1].find_all('span')
    temp = []
    temp.clear()
    for ability in tempStr:
        temp.append(ability.text)
    userlist.specialPassive = temp

def getEmbed_char(uName):
    embed = discord.Embed(title = "< " + uName + " >", description = '',color = 0x62c1cc)
    embed.set_thumbnail(url = userlist.uclassimg)
    embed.add_field(name = '서  버', value = "```" + userlist.server + "```" + '\t', inline = True)
    embed.add_field(name = '길  드', value = "```" + userlist.guild + "```" + '\t', inline = True)
    embed.add_field(name = '클래스', value = "```" + userlist.uclass + "```" + '\t', inline = True)
    embed.add_field(name = '칭  호', value = "```" + userlist.title + "```" + '\t', inline = True)
    embed.add_field(name = '전  투', value = "```" + userlist.level + "```" + '\t', inline = True)
    embed.add_field(name = '아이템', value = "```" + userlist.itemlevel + "```" + '\t', inline = True)
    embed.add_field(name = '원정대', value = "```" + userlist.Expeditionlevel + "```" + '\t', inline = True)
    embed.add_field(name = 'PVP', value = "```" + userlist.pvp + "```" + '\t', inline = True)
    embed.add_field(name = '영  지', value = "```" + userlist.land + "```" + '\t', inline = True)
    embed.add_field(name = '수집형 포인트', value = 
                    "```" + "%-5s%4s\t\t%-5s%4s\n" % ("섬맘", userlist.heart, "별똥별", userlist.star) +
                            "%-5s%4s\t\t%-5s%4s\n" % ("거심", userlist.giant, "미술품", userlist.art) +
                            "%-5s%4s\t\t%-5s%4s\n" % ("씨앗", userlist.seed, "모험물", userlist.adventure) +
                            "%-5s%4s\t\t%-5s%4s\n" % ("징표", userlist.token, "세계수", userlist.leaf) + "```", inline = False)
    embed.add_field(name = '기본 특성', value = 
                    "```" + "%-5s%7s\t%-5s%7s\n" % ("공격력", userlist.power, "생명력", userlist.hp) + "```", inline = False)
    embed.add_field(name = '전투 특성', value = 
                    "```" + "%-5s%4s\t\t%-5s%4s\n" % ("치명", userlist.cri, "특화", userlist.spe) +
                            "%-5s%4s\t\t%-5s%4s\n" % ("제압", userlist.over, "신속", userlist.speed) +
                            "%-5s%4s\t\t%-5s%4s\n" % ("인내", userlist.pat, "숙련", userlist.prof) + "```", inline = False)
    temp = ''
    for Passive in userlist.specialPassive:
        temp = temp + Passive + '\n'
    embed.add_field(name = '각인 효과', value = "```" + temp + "```", inline = False)
    return embed