#discord embed 관련 
import discord

def getEmbed_message_img(message, imgUrl):
    embed = discord.Embed(title = message, description = "",color = 0x62c1cc)
    embed.set_image(url= imgUrl)
    return embed

def getEmbed_daliyCheckList():
    embed = discord.Embed(title = "<로애기들 체크리스트>", description = '',color = 0x62c1cc)
    embed.add_field(
        name = '일일', 
        value = '```- 카던 2회' + '\n' + 
        '- 가디언 토벌 (스택은 쌓였니?)' + '\n'+ 
        '- 길드 기부' + '\n'+ 
        '- 모험 섬 (미니맵 하단 프로키온 나침반)' + '\n'+ 
        '- 필드 보스 (오후 8시 [목,토,일] 오전 2시 [금])' + '\n'+ 
        '- 항해 협동' + '\n'
        '- 영지 기운 (영지 레벨 올려야 좋다...)'+ '\n'
        '- 일일 에포나```'+ '\n', inline = False)
    embed.add_field(
        name = '주간', 
        value = '```- 주간 에포나' + '\n' + 
        '- 어비스 레이드' + '\n'+ 
        '- 어비스 던전' + '\n'+ 
        '- 도전 가디언 토벌' + '\n'+ 
        '- 도전 어비스 던전' + '\n'+
        '- 유령선 (일정 잘 보구 가~)' + '\n' + 
        '- 카오스 게이트 (오후 10시 [토,일] 오후 8시 [화,금]```'
        , inline = False)
    embed.add_field(
        name = '입장권', 
        value = '```- 회랑' + '\n' + 
        '- 큐브```' + '\n'
        , inline = False)
    return embed