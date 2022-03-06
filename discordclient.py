# -*- coding:utf-8 -*- 
#봇 클라이언트
import discord, asyncio
import re
import random
import webcrawling, userCrawling, marketCrawling
import messageReaction, discordEmbed

from discord.ext import commands

token = '토큰'
client = discord.Client()

text_file_path = './userdata.txt'
badwordlist = ['시발','씨발','병신']
@client.event 
async def on_ready():
    await client.change_presence(status=discord.Status.online, activity=discord.Game("므흣"))
    print("I'm Ready!") 
    print(client.user.name) 
    print(client.user.id)

@client.event
async def on_message(message):
    if message.author.bot:
        return None

    if message.content == "!시간" or message.content == "!시간표":
        webcrawling.update_timetable()
        await message.channel.send("니가 찾아봐!!!",embed = webcrawling.get_embed_alltimetable())

    elif message.content.startswith("!시간표"):
        webcrawling.update_timetable()
        string = re.sub("!시간표 ","",message.content)
        embed = webcrawling.get_embed_timetable(string)
        if embed != None:
            await message.channel.send(embed = embed)

    elif message.content.startswith("!시간"):
        webcrawling.update_timetable()
        string = re.sub("!시간 ","",message.content)
        embed = webcrawling.get_embed_timetable(string)
        if embed != None:
            await message.channel.send(embed = embed)
    
    elif message.content.startswith("!이벤트"):
        await message.channel.send("",embed = webcrawling.get_eventlist())

    elif message.content == "!숙제":
        embed = discordEmbed.getEmbed_daliyCheckList()
        await message.channel.send(embed = embed)

    elif message.content == '!명령' or message.content == "!명령어":
        embed = discord.Embed(title = "<명령어>", description = '',color = 0x03fc62)
        embed.add_field(name = '`!시간` `!시간표`', value = '로스트 아크 시간표 테이블', inline = False)
        embed.add_field(name = '`!시간 OOO` `!시간표 OOO`', value = '해당 섬 시간', inline = False)
        embed.add_field(name = '`!이벤트`', value = '진행중인 이벤트', inline = False)
        embed.add_field(name = '`!숙제`', value = '오늘 뭐 해야 하지?', inline = False)
        embed.add_field(name = '`!정보`', value = '캐릭터 정보', inline = False)
        embed.add_field(name = '`!내전`', value = 'ex) !내전 A B C D', inline = False)
        embed.add_field(name = '`!유튜브`', value = 'ex) !유튜브 창술사', inline = False)
        embed.add_field(name = '`!돌파고` `각파고`', value = '돌파고 ,각파고 사이트 링크', inline = False)
        embed.add_field(name = '`!주사위` `주사위 기록`', value = '도르르륵', inline = False)
        embed.add_field(name = messageReaction.get_all_emoticon_message_list(), value = '각종 이모티콘', inline = False)
        await message.channel.send(embed = embed)
    
    elif message.content.startswith('!내전 '):
        string = re.sub("!내전 ","",message.content)
        names = string.split()
        randomlist= random.sample(names,len(names))
        embed = discord.Embed(title = "<랜덤 내전 팀>", description = '',color = 0x03fc62)
        embed.add_field(name = '1팀', value = '`'+ "☆".join(randomlist[:int(len(names)/2)])+'`', inline = False)
        embed.add_field(name = '2팀', value = '`'+ "☆".join(randomlist[int(len(names)/2):])+'`', inline = False)
        await message.channel.send(embed = embed)

    elif message.content.startswith('!거래소'):
        await message.channel.send("점검중.")
    #    string = re.sub("!거래소 ","",message.content)
    #    embed = marketCrawling.get_market_prices(string)
    #    await message.channel.send(embed = embed)

    elif message.content.startswith('!제작'):
        await message.channel.send("점검중.")
    #    string = re.sub("!제작 ","",message.content)
    #    embed = marketCrawling.get_make_info(string)
    #    await message.channel.send(embed = embed)

    elif message.content.startswith("!정보"):
        string = re.sub("!정보 ","",message.content)
        string = ''.join(char for char in string if char.isalnum())
        userCrawling.update_char(string)
        embed = userCrawling.getEmbed_char(string)
        await message.channel.send(embed = embed)

    elif message.content.startswith("!유튜브 "):
        string = re.sub("!유튜브 ","",message.content)
        string = re.sub(" ","+",string)
        embed = discord.Embed(title = "[ " + string + " ]", url = "https://www.youtube.com/results?search_query=" + string, color = 0x62c1cc)
        await message.channel.send(embed = embed)

    elif message.content.startswith("!돌파고"):
        embed = discord.Embed(title = "[  돌파고  ]", url = "https://www.mgx.kr/lostark/utility/dolpago", color = 0x62c1cc)
        await message.channel.send(embed = embed)
        
    elif message.content.startswith("!각파고"):
        #embed = discord.Embed(title = "[  MGX 각파고  ]", url = "https://www.mgx.kr/lostark/utility/carvingpago", color = 0x62c1cc)
        embed = discord.Embed(title = "[  icepeng 각파고  ]", url = "https://icepeng.github.io/loa-calc/imprinting", color = 0x62c1cc)
        await message.channel.send(embed = embed)

    elif message.content.startswith("!감정"):
        url = messageReaction.get_emoticon_img_url(message.content)
        if url != None:
            embed = discordEmbed.getEmbed_message_img("", url)
            await message.channel.send(embed = embed)
        else :
            await message.channel.send(messageReaction.get_all_emoticon_message_list())
    
    elif message.content == "!주사위":
        isExist = False
        new_text_content = ''
        randomnum = random.randrange(0,100000000000)
        minNum = 0
        maxNum = 0
        #with open(text_file_path,'w') as f:
        #    f.write("")
        with open(text_file_path,'r') as f:
            tmp = f.readlines()
            for line in tmp:
                info = line.split()
                if int(info[0]) == int(message.author.id):
                    isExist = True
                    maxNum = int(info[2])
                    minNum = int(info[3])
                    if (int(info[2]) < randomnum):
                        new_string = str(message.author.id) +" "+message.author.name+" "+str(randomnum)+" "+info[3]
                        maxNum = randomnum
                    elif (int(info[3])> randomnum):
                        new_string = str(message.author.id) +" "+message.author.name+" "+ info[2] +" " + str(randomnum)
                        minNum = randomnum
                    else:
                        new_string = line.strip()
                else:
                    new_string = line.strip()

                if new_string:
                    new_text_content +=new_string + '\n'
                else:
                    new_text_content += '\n'

        if isExist:
            with open(text_file_path,'w') as f:
                f.write(new_text_content)
        else :
            with open(text_file_path,'a') as f:
                f.write(str(message.author.id) +" "+message.author.name+" "+str(randomnum)+" "+str(randomnum)+'\n')
                minNum = randomnum
                maxNum = randomnum
        embed = discord.Embed(title = "<주사위>", description = '',color = 0x03fc62)
        embed.add_field(name = '결과', value = '`'+ str(randomnum)+'`\n', inline = False)
        embed.add_field(name = message.author.name+'의 기록', value = '`최고기록: '+ str(maxNum)+'`\n'+
                                                          '`최저기록: '+ str(minNum)+'`\n', inline = False)
        await message.channel.send(embed = embed)

    elif message.content == "!주사위 기록":
        embed = discord.Embed(title = "<주사위 기록>", description = '',color = 0x03fc62)
        with open(text_file_path,'r') as f:
            tmp = f.readlines()
            for line in tmp:
                info = line.split()
                embed.add_field(name = info[1], value = '`최고기록: '+ info[2]+'`\n'+
                                                        '`최저기록: '+ info[3]+'`\n', inline = False)
        await message.channel.send(embed = embed)       

    if messageReaction.isReaction(message.content, badwordlist):
        await message.channel.send("고운말~")
    
    #if "공감" in message.content:
        #await message.channel.send("공감해~")

    #if "강선" in message.content:
        #embed = discordEmbed.getEmbed_message_img("그 저 빛 . . . ★", "https://upload3.inven.co.kr/upload/2020/12/19/bbs/i16438227526.jpg")
        #await message.channel.send(embed = embed)

    #if "야호" in message.content:
        #embed = discordEmbed.getEmbed_message_img("무 야 ~ 호 ~ !", "http://img.khan.co.kr/news/2021/03/14/l_2021031401001628900137951.jpg")
        #await message.channel.send(embed = embed)

    

client.run(token)