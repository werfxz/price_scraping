import requests
import random
from bs4 import BeautifulSoup 

#creating random headers ve proxies
#https://github.com/taspinar/twitterscraper/blob/0e5e269ee17e868a002b1266a0f1cd2c0de53360/twitterscraper/query.py#L45
HEADERS_LIST = [
    'Mozilla/5.0 (Windows; U; Windows NT 6.1; x64; fr; rv:1.9.2.13) Gecko/20101203 Firebird/3.6.13',
    'Mozilla/5.0 (compatible, MSIE 11, Windows NT 6.3; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows; U; Windows NT 6.1; rv:2.2) Gecko/20110201',
    'Opera/9.80 (X11; Linux i686; Ubuntu/14.10) Presto/2.12.388 Version/12.16',
    'Mozilla/5.0 (Windows NT 5.2; RW; rv:7.0a1) Gecko/20091211 SeaMonkey/9.23a1pre'
]

HEADER = {'User-Agent': random.choice(HEADERS_LIST), 'X-Requested-With': 'XMLHttpRequest'}

PROXY_URL = 'https://free-proxy-list.net/'

def get_proxies():
    response = requests.get(PROXY_URL)
    soup = BeautifulSoup(response.text, 'lxml')
    table = soup.find('table',id='proxylisttable')
    list_tr = table.find_all('tr')
    list_td = [elem.find_all('td') for elem in list_tr]
    list_td = list(filter(None, list_td))
    list_ip = [elem[0].text for elem in list_td]
    list_ports = [elem[1].text for elem in list_td]
    list_proxies = [':'.join(elem) for elem in list(zip(list_ip, list_ports))]
    return list_proxies 

PROXIES = get_proxies()

def get_random_proxy(proxies):

    return random.choice(proxies)



def get_request(url, timeout):
    """
    This function sends get request and return bs4 soup object
    """
    response = requests.get(url, headers=HEADER, proxies={"http": get_random_proxy(PROXIES)}, timeout=timeout)
    soup = BeautifulSoup(response.content, 'html5lib') 

    return soup

def scrape_hepsi(url, timeout=60):
    """
    This function takes hepsiburada product url and returns price of product
    """
    soup = get_request(url, timeout)
    
    content = soup.find_all("span", attrs={"itemprop": "price"})
    price = content[0]['content']

    return round(float(price))

def scrape_trendyol(url, timeout=60):
    """
    This function takes trendyol product url and returns price of product
    """
    soup = get_request(url, timeout)

    #if there is no basket discount
    if len(soup.find_all("div", attrs={"class": "pr-cn"})[0].select('span[class="prc-slg"]')) == 1:
        content = soup.find_all("div", attrs={"class": "pr-cn"})[0].select('span[class="prc-slg"]')
    #if there is a basket discount
    elif len(soup.find_all("div", attrs={"class": "pr-cn"})[0].find_all("span", attrs={"class": "prc-dsc"})) == 1:
        content = soup.find_all("div", attrs={"class": "pr-cn"})[0].find_all("span", attrs={"class": "prc-dsc"})
    else:
        print("Can't find price of the Trendyol Product")
        return 0

    #TODO Virgül ile split yapınce küsüratsız fiyatlarda ikiye ayıramıyorsun
    return content[0].get_text().split(',')[0].replace('.','')

def scrape_amazon(url, timeout=60):
    """
    This function takes amazon product url and returns price of product
    """
    soup = get_request(url, timeout)

    #if product has discount
    if len(soup.find_all("span", attrs={"id": "priceblock_dealprice"})) == 1:
        content = soup.find_all("span", attrs={"id": "priceblock_dealprice"})
    #if product has no discount
    elif len(soup.find_all("span", attrs={"id": "priceblock_ourprice"})) == 1:
        content = soup.find_all("span", attrs={"id": "priceblock_ourprice"})
    else:
        print("Can't find price of the Trendyol Product")
        return 0

    return content[0].get_text()
    
def scrape_vatan(url, timeout=60):
    """
    This function takes vatan product url and returns price of product
    """
    soup = get_request(url, timeout)

    content = soup.find_all("div", attrs= {"class": "product-list__content"})[0].find_all("span", attrs={"class": "product-list__price"})
    
    return content[0].get_text()

def scrape_teknosa(url, timeout=60):
    """
    This function takes teknosa product url and returns price of product
    """
    soup = get_request(url, timeout)
    
    #if product has no discount
    if len(soup.find_all("div", attrs={"class": "product-detail-text"})[0].find_all("div", attrs={"class": "default-price"})) == 1:
        content = soup.find_all("div", attrs={"class": "product-detail-text"})[0].find_all("div", attrs={"class": "default-price"})
    #if product has discount
    elif len(soup.find_all("div", attrs={"class": "product-detail-text"})[0].find_all("div", attrs={"class": "new-price"})) == 1:
        content = soup.find_all("div", attrs={"class": "product-detail-text"})[0].find_all("div", attrs={"class": "new-price"})
    else:
        print("Can't find price of the Teknosa Product")
        return 0

    return content[0].get_text()

def scrape_incehesap(url, timeout=60):
    """
    This function takes incehesap product url and returns price of product
    """
    soup = get_request(url, timeout)
    
    if len(soup.select('div[class="container first"]')[0].find_all("span", attrs={"class": "cur"})) == 1:
        content = soup.select('div[class="container first"]')[0].find_all("span", attrs={"class": "cur"})
    elif len(soup.select('div[class="container first"]')[0].find_all("div", attrs={"class": "arti-indirimli-fiyat cur"})) == 1:
        content = soup.select('div[class="container first"]')[0].find_all("div", attrs={"class": "arti-indirimli-fiyat cur"})
    else:
        print("Can't find price of the İnce hesap Product")
        return 0

    return content[0].get_text()

def scrape_itopya(url, timeout=60):
    """
    This function takes itopya product url and returns price of product
    """
    soup = get_request(url, timeout)

    content = soup.find_all("div", attrs= {"class": "product-info"})[0].select('div[class="new text-right"]')

    return content[0].get_text()
    