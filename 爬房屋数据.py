import requests
from bs4 import BeautifulSoup
headers = {'user-Agent' : 'Mozilla/5.0(Windows NT 6.1; wow64）Safari/537.36'}
link = 'https://beijing.anjuke.com/sale/'
r = requests.get(link,headers = headers)
soup = BeautifulSoup|(r.text,'lxml')
house_list = soup.find_all('li',class_='list_item')
for house in house_list:
    name = houes.find('div',class_ = 'housetitle').a.text.strip()
    price = house.find('span',class_='pricedet').test.strip()
    price_area = house.find('span',class_='unitprice').text.strip()
    no_room = house.find('div',class_='detailsitem').span.text
    area = house.find('div',class_='detailsitem').contents[3].text
    floor = house.find('div',class_='detailsitem').contents[5].text
    year = house.find('div',class_='detailsitem'.contents[7].text)
    broker = house.find('span',class_='brokername').text
    broker = broker[1:]
    address = house.find('span',class_='commaddress').text.strip()
    address = address .replace('\xa0\xa0\n     ','')
    tag_list = house.find_all('span',class_='item-tage')
    tage = [i.text for i in tag_list]
    print(name,price,price_area,no_room,area,floor,year,broker,address,tags)









