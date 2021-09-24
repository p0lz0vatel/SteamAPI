import requests
import json
from operator import itemgetter

def getPriceMarket():
    result = requests.get("https://market.csgo.com/api/v2/prices/USD.json")
    source = result.json()
    source = source["items"]
    return source

def getPriceSteam():
    result = requests.get("https://csgobackpack.net/api/GetItemsList/v2/?no_details=TRUE/json")
    result = result.json()
    return result

def FormPrices(source, place):
    if (place == "market"):
        Dict = {"Names": dict()}
        for item in source:
            Dict["Names"][item["market_hash_name"]] = dict(price=item["price"], volume=item["volume"])
        return Dict
    if (place == "steam"):
        source = source["items_list"]
        Dict = {"Names": dict()}
        for item in source:
            try:
                Dict["Names"][item] = source[item]['price']
            except KeyError:
                pass
        return Dict

def mainDict(DictM, DictS):
    Dict = {"Names": list()}
    for item in DictM["Names"].keys():
        if (item in DictS["Names"].keys()):
            try:
                Dict["Names"].append(dict({item: dict(Market_Price=dict(Price=float(DictM["Names"][item]["price"]), OnSale=int(DictM["Names"][item]["volume"])),
                                                Steam_Price=dict(Avg_Price_24=DictS["Names"][item]['24_hours']["average"], with_discount=round(DictS["Names"][item]['24_hours']["average"] * 0.87, 3),
                                                                 Sold=int(DictS["Names"][item]["24_hours"]["sold"])), specifications=dict(
                                                      tendence_30d=round(DictS["Names"][item]['24_hours']["average"] - DictS["Names"][item]["30_days"]["average"], 2), deviation_7d=float(DictS["Names"][item]["7_days"]["standard_deviation"]),
                                                        price_difference=round(DictS["Names"][item]['24_hours']["average"] * 0.87 - float(DictM["Names"][item]["price"]), 3)))}))
            except KeyError:
                pass
            except ValueError:
                pass
    return Dict

def SortDict(Dict, place, sold=None, stability=None, tendence=None, top_price=None):
    # print(Dict)
    # print(place)
    # print(sold)
    # print(stability)
    # print(tendence)
    # print(top_price)
    newList = list()
    if (place == "market"):
        for item in Dict["Names"]:
            key_name = ""
            for key in item.keys():
                if (r"StatTrak\u2122" in key):
                    i.replace(r"\u2122", '')
                key_name = key
            for value in item.values():
                if (value["Steam_Price"]["Sold"] > sold and value["Market_Price"]["Price"] < top_price):
                    newList.append([key_name, value])
        result = sorted(newList, key=lambda item: item[1]["specifications"]["price_difference"], reverse=True)
        return List_to_Dict(result)
    if (place == "steam"):
        for item in Dict["Names"]:
            key_name = ""
            for key in item.keys():
                key_name = key
            for value in item.values():
                if (value["Market_Price"]["OnSale"] > sold and value["specifications"]["deviation_7d"] < stability
                        and value["Steam_Price"]["Avg_Price_24"] < top_price and abs(value["specifications"]["tendence_30d"]) < abs(tendence)):
                    newList.append([key_name, value])
        result = sorted(newList, key=lambda item: item[1]["specifications"]["price_difference"])
        return List_to_Dict(result)

def List_to_Dict(List):
    Dict = list()
    for item in List:
        Dict.append(dict({item[0]: item[1]}))
    return Dict

def Dict_to_List(Dict, Sold):
    List = list()
    for item in Dict["Names"]:
        for key, value in item.items():
            if (value["Market_Price"]["OnSale"] > 20 and value["specifications"]["tendence_30d"] != 0 and
                    value["specifications"]["deviation_7d"] != 0):
                List.append([key, value])
    return List

def FormedDict():
    DictMarket = FormPrices(getPriceMarket(), "market")
    DictSteam = FormPrices(getPriceSteam(), "steam")
    ConDict = mainDict(DictMarket, DictSteam)
    return ConDict

def Prices(place, sold=None, stability=None, tendence=None, top_price=None):
    Dict = SortDict(FormedDict(), place, sold, stability, tendence, top_price)
    return Dict

def ValueSearch(param, isReverse, Sold):
    Dict = Dict_to_List(FormedDict(), Sold)
    return List_to_Dict(sorted(Dict, key=lambda item: item[1]["specifications"][param], reverse=isReverse))

def ItemSearch(name):
    print(name)
    # Dict = FormedDict()
    # for itemName in Dict["Names"].keys():
    #     if (itemName == name):
    #         return Dict["Names"][itemName]


#print(Prices("market", sold=10, stability=None, tendence=None, top_price=10)[0])
#print(Prices("steam", sold=10, stability=4, tendence=0.3, top_price=10)[0])
## Dict = SortDict(FormedDict, place, sold, stability, top_price)
#print(SortDict(Prices(), "market", sold=10, top_price=10))
#SortedDict = SortDict(Dict, "steam", 100, 2, 3)

# with open('dataPrices.json', 'w', encoding='utf-8') as f:
#     json.dump(DictSteam, f, ensure_ascii=False, indent=4)

#print(getPriceSteam())

#224EWZJkhkeRUNEjVL-K0Z4_F-k