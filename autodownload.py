import time
import os
import requests
from PIL import Image
from io import BytesIO
from bs4 import BeautifulSoup
from selenium import webdriver
from fake_useragent import UserAgent

URL_MANHUAREN='https://www.manhuaren.com/'
#URL_HOME="https://www.manhuaren.com/manhua-xiarichongxian/"
URL_HOME="https://www.manhuaren.com/manhua-yequ/"
CHAPTER_NO=0

driver = webdriver.Edge("./msedgedriver.exe")
driver.get(URL_HOME)
soup=BeautifulSoup(driver.page_source,"lxml")

index_url = []
index_title = []
a_class = soup.find_all('a',{'class':'chapteritem'})
for href in a_class:
    page_url = href.get('href') # 每一章節的網址
    title = href.text
    # title = href.get('title') #每一章節的開頭
    
    index_url.append(page_url) #新增每個章節的網址進去陣列裡
    index_title.append(title)


if CHAPTER_NO == 0:
    MAX_CHAPTER=len(index_url)
else:
    MAX_CHAPTER=CHAPTER_NO


#每一章節的圖片擷取
for i in range(MAX_CHAPTER):#所有章節數量
    index_page = []
    COMIE_NAME = index_title[i]
    comie_page = MAX_CHAPTER - i #第幾號
    
    
    comie_index_url = URL_MANHUAREN + str(index_url[i]) #進入第一個網頁
    response = driver.get(comie_index_url)#打開網頁
    #driver.get(comie_index_url)

    soup_ = BeautifulSoup(driver.page_source,"lxml")#進行分析
    # print (soup_.prettify())
    PAGE_MAX = soup_.find('p',{'class':'view-fix-top-bar-title'})
    index_page = PAGE_MAX.text
    number_of_page = int(index_page[-2:])
    os.mkdir(f'./photo_save/{COMIE_NAME}')


    for j in range(number_of_page):
        if soup_ !=None:
            
            img_find = soup_.find('img', {'class' : 'lazy'})
            img_url = img_find.get('src')
            print(img_find.get('src'))
            ua = UserAgent()
            headers=ua.edge
            
            response = requests.get(img_url,headers)
            img = Image.open(BytesIO(response.content))
            
            # store_path=f'./Kimetsu_no_Yaiba/{comie_page}'+str(comie_page)+'_'+str(i+1)+'_'+'.png'
            store_path=f'./photo_save/{COMIE_NAME}/'+str(COMIE_NAME)+'_'+str(j+1)+'_'+'.png'
            img = img.save(store_path)
            ### 由於點擊下一頁，擷取程式碼還在上一頁
            
            element = driver.find_element('xpath','/html/body/ul/li[3]/a')#點下一頁
            driver.execute_script("arguments[0].click()",element)
            time.sleep(1)
            soup_ = BeautifulSoup(driver.page_source,"lxml")
            

            del response
