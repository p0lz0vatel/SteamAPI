import requests
import json
from bs4 import BeautifulSoup

def getPriceMarket():
    result = requests.get("https://market.csgo.com/api/v2/prices/RUB.json").text
    soup = BeautifulSoup(result, "html.parser")
    source = json.loads(soup.text)
    source = source["items"]
    return source

def getPriceSteam():
    result = requests.get("http://csgobackpack.net/api/GetItemsList/v2/").text
    soup = BeautifulSoup(result, "html.parser")
    source = json.loads(soup.text)
    return result

def SortPrices(source):
    Dict = {"Names": dict()}
    for item in source:
        Dict["Names"][item["market_hash_name"]] = item["price"]
    return Dict
sss
DictM = SortPrices(getPriceMarket())
print(DictM)
#print(getPriceSteam())

#224EWZJkhkeRUNEjVL-K0Z4_F-k
