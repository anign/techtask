from time import sleep
from random import random

import requests
from bs4 import BeautifulSoup
import lxml

MAIN_PAGE = 'https://zakupki.gov.ru/'
NUM_PAGES = 2

headers = {
    "Accept":'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'UserAgent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36'
}

def convert_to_xml(l: list) -> list:
    """ Конвертация ссылок в XML """

    xml_list = []
    for i in l:
        xml_list.append(i.replace('view', 'viewXml'))
    return xml_list

def parse_printform_link(n: int):
    """ Возвращает список ссылок на печатную форму тендера """ 

    links = []
    src = requests.get(
        f'https://zakupki.gov.ru/epz/order/extendedsearch/results.html?fz44=on&pageNumber={n}')
    soup = BeautifulSoup(src.content, 'lxml').find_all('a')
    for i in soup:
        link = i.get('href')
        if link is not None:
            if 'printForm' in link and 'view' in link and 'regNumber' in link:   
                links.append(MAIN_PAGE + link)
    return links

def parse_date_from_xml(l):
    """ Парсинг даты публикации """
    dates = []
    xml_links = convert_to_xml(l)
    for i in xml_links:
        data = requests.get(i).text
        sleep(1 + random()) # не помогает
        soup = BeautifulSoup(data, 'xml')
        
        date = soup.find_all('publishDTInEIS')  
        dates.append(date[0].text) 
    return dates

if __name__ == '__main__':
    for i in range(1, NUM_PAGES + 1):
        #dates = parse_date_from_xml(parse_printform_link(i))
        print(f'Страница - {i}')
        for link in parse_printform_link(i):
            print(link + f' || Дата публикации: ', sep='\n')
        print('-------------------------------------------------------------------')
