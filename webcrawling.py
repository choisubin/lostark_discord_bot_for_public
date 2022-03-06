#게임 이벤트 크롤링, 로스트아크 타이머 크롤링
import discord, asyncio
import requests

from bs4 import BeautifulSoup

url_inven_timer = "http://m.inven.co.kr/lostark/timer/"

list_npcname = []
list_gentime = []

def update_timetable():
    list_npcname.clear()
    list_gentime.clear()

    html_contents = requests.get(url_inven_timer).text
    soup = BeautifulSoup(html_contents, "html.parser")

    for name in soup.find_all(attrs={'class':'npcname'}):
        list_npcname.append(name.text)

    for gentime in soup.find_all(attrs={'class':'gentime'}):
        list_gentime.append(gentime.text)

def get_embed_alltimetable():
    embed = discord.Embed(title = "<로스트아크 시간표>",description = "",color = 0x62c1cc)
    for index in range(len(list_npcname)):
        embed.add_field(name = list_npcname[index], value = list_gentime[index], inline = True)
    embed.set_footer(text = "알람은 못해줘~")
    return embed

def get_embed_timetable(string):
    for index in range(len(list_npcname)):
        if string in list_npcname[index]:
            embed = discord.Embed(title = list_npcname[index], description = list_gentime[index],color = 0x62c1cc)
            return embed
    return None

url_inven = "http://lostark.inven.co.kr/"
list_eventname = []
list_eventurl = []
list_eventdate = []

def get_eventlist():
    list_eventname.clear()
    list_eventurl.clear()
    list_eventdate.clear()

    html_inven_event_content = requests.get(url_inven).text
    soup = BeautifulSoup(html_inven_event_content, "html.parser")
    eventlist = soup.find(attrs = {'class' : 'menuGroup bg event'}).find_all(attrs = {'class':'link'})

    for event in eventlist:
        list_eventurl.append(event['href'])
        list_eventname.append(event.find(attrs = {'class':'ev_txt'}).text)
        list_eventdate.append(event.find(attrs = {'class':'ev_day'}).text)

    embed = discord.Embed(title = "<로스트아크 이벤트>",description = "",color = 0x62c1cc)
    for index in range(len(list_eventname)):
        embed.add_field(name = list_eventname[index], value = '기간: '+ list_eventdate[index] + '\n' + list_eventurl[index]+'\n', inline = False)
    embed.set_footer(text = "들어가서 직접 봐~")
    return embed