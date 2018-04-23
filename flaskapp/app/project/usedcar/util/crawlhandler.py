


import lxml # for bs xml markup processing

import urllib # read web data
import json # json
from bs4 import BeautifulSoup
import bs4 as bs # web crawling

import re # 정규식 지원


import urllib.request as urlreq

# 크로울 다루는 책임을 가진 클래스
class CrawlHandler:
    # constructor take <class 'bs4.element.Tag'>
    def __init__(self):
        return

    def setMetaSubSoup(self,index):
        soup = self.meta_soup
        try:
            sub_soup = soup[index]
        except:
            sub_soup = ""
        return sub_soup

    def setSoup(self, div):
        setMetaSubSoup = self.setMetaSubSoup
        self.row_title_soup = div.find('h2', {'class' :'cui-delta listing-row__title'})
        self.miles_soup = div.find('span', {'class' : 'listing-row__mileage'})
        self.vendor_soup =div.find('div',{'class' : 'listing-row__dealer-name listing-row__dealer-name-mobile'}).div
        self.media_soup = div.find('div', {'class' : 'media-count shadowed'})

        self.meta_soup = div.find('ul', {'class' : 'listing-row__meta'}).find_all("li")
        self.exterior_color_soup = setMetaSubSoup(0)
        self.interior_color_soup = setMetaSubSoup(1)
        self.transmission_soup = setMetaSubSoup(2)
        self.drivetrain_soup = setMetaSubSoup(3)

        if div.find('div',{'class' : 'dealer-rating-stars'}) == None:
            self.full_star_soup = 0
            self.half_star_soup = 0
        else:
            self.full_star_soup =div.find('div',{'class' : 'dealer-rating-stars'}).find_all('svg',{'class' : 'icon-image filled'})
            self.half_star_soup =div.find('div',{'class' : 'dealer-rating-stars'}).find_all('svg',{'class' : 'icon-image half'})

        if div.find('span',{'class' : 'listing-row__review-number'}) == None:
            self.review_soup = 0
        else:
            self.review_soup =div.find('span',{'class' : 'listing-row__review-number'})

        if div.find('span', {'class' : 'listing-row__price'}) == None:
            self.price_soup = 0
        else:
            self.price_soup = div.find('span', {'class' : 'listing-row__price'})

    def setElement(self):
        contentProcess = self.contentProcess
        drivertrainProcess = self.drivertrainProcess
        transmissionProcess =self.transmissionProcess


        row_title_soup = self.row_title_soup
        miles_soup = self.miles_soup
        vendor_soup = self.vendor_soup
        media_soup = self.media_soup
        # meta_soup = self.meta_soup
        full_star_soup = self.full_star_soup
        half_star_soup = self.half_star_soup
        review_soup = self.review_soup

        exterior_color_soup = self.exterior_color_soup
        interior_color_soup  = self.interior_color_soup
        transmission_soup  = self.transmission_soup
        drivetrain_soup = self.drivetrain_soup

        price_soup = self.price_soup

        self.year = contentProcess(row_title_soup,"empty year",0," ")
        self.brand = contentProcess(row_title_soup,"empty company",1," ")
        self.model = contentProcess(row_title_soup, "self.company",2," ")
        self.title = contentProcess(row_title_soup,"no-title",[1]," ")
        self.miles = ''.join(contentProcess(miles_soup,"no-mile",0," ").split(','))
        self.vendor = contentProcess(vendor_soup,"no-vendor",[0]," ")
        photoPre = contentProcess(media_soup,0,0,"\n")
        videoPre = contentProcess(media_soup,0,1,"\n")
        self.photos = contentProcess(photoPre,0,0," ")
        self.video = contentProcess(videoPre,0,0," ")

        self.exterior_color = contentProcess(exterior_color_soup,"black",1,":")
        self.interior_color = contentProcess(interior_color_soup,"black",1,":")
        self.transmission = transmissionProcess(transmission_soup,"x-speed")
        self.drivetrain = drivertrainProcess(drivetrain_soup,"4wd")

        if type(full_star_soup)==int and type(half_star_soup)==int:
            self.star = full_star_soup + half_star_soup
        else:
            self.star = len(full_star_soup) + len(half_star_soup)*0.5
        self.review_no = contentProcess(review_soup,"0",0,"\n")
        self.price = ''.join(contentProcess(price_soup,"0",0,"\n")[1:].split(','))


    def getData(self):
        data = {}

        data['year']=self.year
        data['brand']=self.brand
        data['model']=self.model
        data['title']=self.title
        data['miles']=self.miles
        data['vendor']=self.vendor
        data['photos']=self.photos
        data['video']=self.video
        data['exterior_color']=self.exterior_color
        data['interior_color']=self.interior_color
        data['transmission']=self.transmission
        data['drivetrain']=self.drivetrain
        data['star']=self.star
        data['review_no']=self.review_no
        data['price']=self.price

        return data

    def get_rows(self, startpage, endpage):
        rows = []
        cnt = 0
        for page in range(startpage,endpage):
            url = 'https://www.cars.com/for-sale/searchresults.action/?page='+str(page)+'&perPage=100&rd=99999&searchSource=PAGINATION&showMore=true&sort=relevance&stkTypId=28881&zc=31216'

            sauce = urlreq.urlopen(url).read()
            soup = bs.BeautifulSoup(sauce, 'lxml')

            specificSoup = soup.find_all('div', class_='listing-row__details')



            print("===",page)
            for div in specificSoup:
                self.setSoup(div)
                self.setElement()
                data = self.getData()

                from .modelhandler import ModelHandler
                md = ModelHandler()

                # print(data)
                rows.append(data)
                # print(data['title'])
                cnt +=1
        return rows

    def contentProcess(self, obj,holder,index, sep):

        if type(index) == list:
            content = self.contentMerge(obj,holder,index, sep)
        else:
            content = self.contentGet(obj,holder,index, sep)

        # print("contentProcess",content)

        return self.toReplaceAndLower(holder,content)

    def contentGet(self,obj,holder,index, sep):
        if type(obj) == bytes or type(obj) == str:
            try:
                content = obj.split(sep)[index]
            except:
                content=""
        else:
            try:
                content = obj.get_text().strip().split(sep)[index].strip()
            except:
                content=""

        return content

    def contentMerge(self,obj,holder,idxList, sep):
        if type(obj) == bytes:
            try:
                content = " ".join(obj.split(sep)[idxList[0]:idxList[1]])
            except:
                content = " ".join(obj.split(sep)[idxList[0]:])
        else:
            try:
                content = " ".join(obj.get_text().strip().split(sep)[idxList[0]:idxList[1]])
            except:
                content = " ".join(obj.get_text().strip().split(sep)[idxList[0]:])

        return content

    def toReplaceAndLower(self, holder, content):
        if content == "":
            content = holder

        if type(content) !=int:
            content.lower()
        return content

    def transmissionProcess(self, tag,holder):
        contentProcess = self.contentProcess
        content = contentProcess(tag,holder,1,":").lower().split(" ")[0]
        first = content[0]
        numbers = ['1','2','3','4','5','6','7','8','9','10']
        # print(first)
        if type(first) == int and 1<= first <= 10:
            content = content[0]+"-speed"
        elif first in numbers:
            content = first+"-speed"
        elif content == 'automatic':
            content = "6-speed"

        # print(content)
        return content

    def drivertrainProcess(self, tag,holder):
        contentProcess = self.contentProcess
        content = contentProcess(tag,holder ,1,":").lower()
        import copy
        # not ref just value
        x = copy.deepcopy(content)
        if x == 'four wheel drive' or x == '4wd' or x=='4x4'or x=='awd':
            content = '4wd'
        elif x == '2wd' or x=='f w d':
            content = 'fwd'
        elif x == 'rwd':
            pass
        else:
            content = '4wd'

            # print(content)
        return content