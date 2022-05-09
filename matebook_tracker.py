import pandas as pd
import requests
from bs4 import BeautifulSoup
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import easygui

# FIRST WE PULL DATA FROM ALL PAGES

# HUAWEI

huawei = 'https://consumer.huawei.com/pl/shop/product/huawei-matebook-d16'



exe_path =  easygui.enterbox(r"Please provide full path to chromedriver executable file")

# sending request to page
driver = webdriver.Chrome(executable_path=exe_path)
driver.get(huawei)
time.sleep(2)

# getting page code 
htmlSource = driver.page_source

# turning code into bs object
soup = BeautifulSoup(htmlSource,'lxml')

# finding price
find_price_huawei = soup.find('span',id="pro-special-price")

# adjusting price
price_huawei = find_price_huawei.text.replace('\xa0',"").replace('\xa0','').replace('zł',"").replace(',','.')

# XKOM
xkom='https://www.x-kom.pl/p/637987-notebook-laptop-16-huawei-matebook-d-16-r5-4600h-16gb-512-win10.html?utm_source=ceneo&utm_medium=comparison&utm_campaign=ceneo_click'


# sending request
driver.get(xkom)
time.sleep(2)

# getting page code
htmlSource = driver.page_source

# turning code into bs object
soup = BeautifulSoup(htmlSource,'lxml')

# finding price
find_price_xkom = soup.find('div',class_='u7xnnm-4 jFbqvs')

# adjusting price
price_xkom = find_price_xkom.text.replace(' zł','').replace(' ','').replace(',','.')

# ALTO
alto = 'https://www.al.to/p/637987-notebook-laptop-16-huawei-matebook-d-16-r5-4600h-16gb-512-win10.html?utm_source=ceneo&utm_medium=comparison&utm_campaign=ceneo_click'

# sending request
driver.get(alto)
time.sleep(2)

# getting page code
htmlSource = driver.page_source

# turning code into bs object
soup = BeautifulSoup(htmlSource,'lxml')

# finding price
find_price_alto  = soup.find('div',class_='u7xnnm-4 jFbqvs')

# adjusting price
price_alto = find_price_alto.text.replace(' ','').replace('zł','').replace(',','.')

# closing web browser
driver.quit()

# ELECTRO
electro = 'https://www.electro.pl/komputery-i-tablety/laptopy-i-ultrabooki/laptopy/notebook-huawei-matebook-d16-53011sjw-r5-4600h-16gb-512ssd-int-16-w10?utm_source=ceneo&utm_medium=cpc&utm_content=393762&utm_campaign=2021-07&utm_term=Laptopy&ceneo_spo=true'

# sending request
source = requests.get(electro).text

# turning text into bs object
soup = BeautifulSoup(source,'lxml')

# finding price
find_price = soup.find('div',class_='a-price_new')

# adjusting price
price_electro = "{:.2f}".format(int(find_price['data-price'])/100)


# MORELE

morele = 'https://www.morele.net/laptop-huawei-matebook-d16-53011sjw-8259073/?utm_source=ceneo&utm_medium=referral'

# sending request
source = requests.get(morele).text

# turning text into bs object
soup = BeautifulSoup(source,'lxml')

# finding price
price_morele = soup.find('div',id='product_price_brutto')['content']

# KOMPUTRONIK

komputronik = 'https://www.komputronik.pl/product/717221/huawei-matebook-d15-53011sjw.html?utm_source=Ceneo&utm_medium=link&utm_campaign=NiePromo'

# sending request
source = requests.get(komputronik).text

# turning text into bs object
soup = BeautifulSoup(source,'lxml')

# finding price
find_price_komputronik = soup.find('span',class_='proper')

# adjusting price
price_komputronik = find_price_komputronik.text.replace('\n','').replace(' ','').replace('zł','').replace('\xa0','')

# AVANS

avans = 'https://www.avans.pl/komputery-i-tablety/laptopy-i-ultrabooki/laptopy/notebook-huawei-matebook-d16-53011sjw-r5-4600h-16gb-512ssd-int-16-w10?utm_source=Ceneo&utm_medium=cpc&utm_content=393762&utm_campaign=2021-07&utm_term=Laptopy&ceneo_spo=false'

# sending request
source = requests.get(avans).text

# turning text into bs object
soup = BeautifulSoup(source,'lxml')

# finding price
find_price_avans = soup.find('span',class_="a-price_price")

# pulling price from found element
price_avans =find_price_avans.text

# MEDIA EXPERT

media_expert = 'https://www.mediaexpert.pl/komputery-i-tablety/laptopy-i-ultrabooki/laptopy/notebook-huawei-matebook-d16-53011sjw-r5-4600h-16gb-512ssd-int-16-w10?utm_source=Ceneo&utm_medium=cpc&utm_content=393762&utm_campaign=2021-07&utm_term=Laptopy&ceneo_spo=false'

# sending request
source = requests.get(media_expert).text

# turning text into bs object
soup = BeautifulSoup(source,'lxml')

# finding price
find_price_mediaepxert = soup.find('span',class_="whole")

# getting text
find_price_mediaepxert.get_text()

# adjusting price
price_mediaexpert = find_price_mediaepxert.text.replace('\u202f','')


# Creating frame for data
df = pd.DataFrame(columns=['Market','Price',"Address"])

# preparing data to be added to the frame
data_for_df = [{"Market":"Media Expert",'Price':price_mediaexpert,'Address':media_expert},{"Market":"Avans",'Price':price_avans,'Address':avans},
                {"Market":"Komputronik",'Price':price_komputronik,"Address":komputronik},{"Market":"Morele",'Price':price_morele,'Address':morele},
                {"Market":"Alto",'Price':price_alto,'Address':alto},{"Market":"X-Kom",'Price':price_xkom,"Address":xkom},
                {"Market":"Huawei",'Price':price_huawei,'Address':huawei},{"Market":"Electro",'Price':price_electro,'Address':electro}]



# appending data to dataframe
df = df.append(data_for_df,ignore_index=True)



# switching format for price to float
df['Price'] = df['Price'].astype(float)

# filter for wrong values
df = df[(df['Price']>2000)]

# sorting dataframe by price and market, both ascending
df.sort_values(by=['Price','Market'],ascending=['True','True'],inplace=True)




# creating filter for price
filtering = df['Price']<3998


# checking if there are discounts
if len(df[filtering]['Address'])>0:
    # assigning address
    link_to_shop = df[filtering]['Address'][df[filtering]['Address'].index[0]]

    # going to webpage
    browser = webdriver.Chrome()
    browser.get(link_to_shop)
else:
    easygui.msgbox("No discounts for laptop", title="Prices checked")
    print('No discount :(')


