#로스트아크 거래소 크롤링 관련
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time
import discord
import re
import chromedriverSetting

url = 'https://lostark.game.onstove.com/Market'
make_url = 'http://lostark.inven.co.kr/dataninfo/craft/'

sell_one = []
sell_ten = ["오레하 원목","오레하 공작석","갈색 진주","빛나는 가죽","삼색 진주"
            ,"만개한 나래꽃","나래꽃","만개한 노을꽃","노을꽃","광대버섯","큰 광대버섯"
            ,"큰 주근깨버섯","만개한 홍선화","만개한 몽유꽃","큰 주근깨버섯"]
sell_100 = ["작은 나래꽃","작은 노을꽃","작은 광대버섯"]

make_30 = ["하급 오레하 융화 재료","중급 오레하 융화 재료","상급 오레하 융화 재료"]

def get_market_prices(serchtext):

    html = get_market_item_html(serchtext)

    soup = BeautifulSoup(html,'html.parser')
    prices = soup.findAll(attrs = {'class' : 'price'})
    itemnames = soup.findAll(attrs = {'class' : 'grade'})
    pricelist = []
    itemnamelist = []
    for price in prices:
        pricelist.append(price.text)
    for itemname in itemnames:
        name = itemname.find(attrs = {'class':'name'})
        if name != None:
            itemnamelist.append(name.text)

    
    embed = discord.Embed(title = "<실시간 거래소 가격>", description = '',color = 0x03fc62)
    length = int(len(pricelist)/3)
    print("length : "+str(length))
    for index in range(length):
         embed.add_field(name = itemnamelist[index], 
         value = "```%s%s\t\n" % ("전일 평균 거래가: ", pricelist[index * 3]) +
         "%s%s\t\n" % ("최근 거래가: ", pricelist[index * 3 + 1]) +
         "%s%s\t```\n" % ("최저가: ", pricelist[index * 3 + 2])
         , inline = False)
    return embed

def get_make_info(item):
    chromedriverSetting.driver.get(make_url)

    chromedriverSetting.driver.find_element_by_name("searchword").send_keys(item)
    chromedriverSetting.driver.find_element_by_name("scheck").click()
    chromedriverSetting.driver.find_element_by_class_name("btn_search").click()
    time.sleep(0.1)


    print("--------------------\n\n\n\n\n\n\n")
    itemTable = chromedriverSetting.driver.find_element_by_class_name("list_table")
    tbody = itemTable.find_element_by_tag_name("tbody")
    rows = tbody.find_elements_by_tag_name("tr")

    itemNames = []#검색 된 키워드가 포함된 아이템 목록
    materials = []#해당 아이템의 재료 및 제작비용

    rowLen = len(rows)

    for index, value in enumerate(rows):

        if index == rowLen-1:
            break
        

        itemName = value.find_elements_by_tag_name("td")[0]
        itemNames.append(itemName.text)

        material = value.find_elements_by_tag_name("td")[1]
        mateList = material.text.split('\n')
        print(mateList)
        mat = Material(mateList)
        materials.append(mat)

    print("itemnames")
    print(itemNames)#검색된 아이템 목록 출력
    buyPriceList = []
    makePriceList = []

    for index, name in enumerate(itemNames):
        html = get_market_item_html_driver(name)

        soup = BeautifulSoup(html,'html.parser')
        prices = soup.findAll(attrs = {'class' : 'price'})

        
        print(name)
        if len(prices) <= 0:#상급 오레하처럼 없는 아이템이 생길경우 계산 중단
            break

        price = float(prices[2].text)
        if name in make_30:
            price *=30

        print(price)
        #만들려는 것의 가격 서칭 

        totalMakePrice = materials[index]._Gold
        print("제작 비용")
        print(totalMakePrice)

        print("필요 재료들")
        print(materials[index]._Materials)
        for matindex,mat in enumerate(materials[index]._Materials):
            matHtml = get_market_item_html_driver(mat)
            
            soup = BeautifulSoup(matHtml,'html.parser')
            prices = soup.findAll(attrs = {'class' : 'price'})
            if mat in sell_one:
                matprice = float(prices[2].text)
            elif mat in sell_ten:
                matprice = float(prices[2].text) / 10.0
            elif mat in sell_100:
                matprice = float(prices[2].text) / 100.0
            else:
                matprice = float(prices[2].text)

            print(matprice)
            print(materials[index]._MaterialsCount[matindex])
            totalMakePrice += matprice * materials[index]._MaterialsCount[matindex]
        print("시세가 반영된 총 재료값 : ")
        print(totalMakePrice)
        print("경매장에서 구매 시")
        print(price)
        makePriceList.append(totalMakePrice)
        buyPriceList.append(price)

    chromedriverSetting.driver.quit()

    embed = discord.Embed(title = "<제작 시세 비교>", description = '',color = 0x03fc62)
    length = int(len(makePriceList))
    print("length : "+str(length))
    for index in range(length):
         embed.add_field(name = itemNames[index], 
         value = "```%s%s\t\n" % ("경매장에서 한 세트 구매 시 : ", buyPriceList[index]) +
         "%s%s\t\n" % ("한세트 제작 시 비용 : ", makePriceList[index]) +
         "%s%s\t```\n" % ("한 세트를 제작 후 판매 시 가격 (수수료o) ", int((buyPriceList[index]*0.95) - makePriceList[index]))
         , inline = False)
    return embed



def get_market_item_html(item):
    chromedriverSetting.driver.get(url)

    chromedriverSetting.driver.find_element_by_id("txtItemName").send_keys(item)
    chromedriverSetting.driver.find_element_by_xpath('//*[@id="lostark-wrapper"]/div/main/div/div/div[2]/form/fieldset/div/div[4]/button[1]').click()
    time.sleep(0.1)
    html = chromedriverSetting.driver.page_source

    chromedriverSetting.driver.quit()

    return html
    

def get_market_item_html_driver(item):

    chromedriverSetting.driver.get(url)

    chromedriverSetting.driver.find_element_by_id("txtItemName").send_keys(item)
    chromedriverSetting.driver.find_element_by_xpath('//*[@id="lostark-wrapper"]/div/main/div/div/div[2]/form/fieldset/div/div[4]/button[1]').click()
    time.sleep(0.2)
    html = chromedriverSetting.driver.page_source

    return html


def get_market_item_htmls(itemList):
    chromedriverSetting.driver.get(url)
    html = []
    for i in itemList:
        chromedriverSetting.driver.find_element_by_id("txtItemName").send_keys(i)
        chromedriverSetting.driver.find_element_by_xpath('//*[@id="lostark-wrapper"]/div/main/div/div/div[2]/form/fieldset/div/div[4]/button[1]').click()
        time.sleep(0.1)
        html.append(chromedriverSetting.driver.page_source)

    
    chromedriverSetting.driver.quit()

    return html

class Material:
    #_Materials = []
    #_MaterialsCount = []
    #_Gold = 0

    def __init__(self,materials):

        self._Materials = []
        self._MaterialsCount = []
        self._Gold = 0
        for i in materials:

            if i.find("골드") != -1:
                self._Gold = int(re.findall("\d+",i)[0])
                print("제작비")
                print(self._Gold)
            else:

                name = i.split(' x', 1)[0]
                self._Materials.append(name)
                count = int(re.findall("\d+",i)[0])
                self._MaterialsCount.append(count)