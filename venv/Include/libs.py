import requests
from bs4 import BeautifulSoup
from operator import itemgetter
import json
from fuzzywuzzy import process

def Get(Url):
    result = requests.get(url=Url)
    return result

def ForPrice(price):
    price = price[:len(price)-2] + "." + price[len(price)-2:]
    return float(price)

def Sorting(Dict ,Element_Name):
    if (Element_Name != "Benefit"):
        return sorted(Dict, key=itemgetter())
    else:
        try:
            return sorted(Dict, key=itemgetter("Price", "Float"))
        except KeyError:
            return "Check Keys Names)"

def Printing(Dict, Count=None):
    print("Dict's Len: " + str(len(Dict)))
    if (Count == None):
        return json.dumps(Dict, indent = 4)
    else:
        new_Dict = []
        for i in range(Count):
            new_Dict.append(Dict[i])
        return json.dumps(new_Dict, indent = 4)

def RefactorName(item_Name):
    print(str(item_Name) + " UnRefactor")
    skinFloatIn = 2
    item_Name = item_Name.split()
    print(item_Name)
    if ("(Field-Tested)" in item_Name or "(Well-Worn)" in item_Name or "(Battle-Scarred)" in item_Name):
        skinFloat = item_Name[-1]
        skinFloat = skinFloat.replace(" ", "-")
        skinFloatIn = 1
        print("for -")
    skinFloat = " ".join(item_Name[len(item_Name) - skinFloatIn:])
    print(skinFloat)
    del item_Name[len(item_Name) - skinFloatIn:]
    item_Name = " ".join(item_Name)
    item_Name = item_Name.split(" | ")
    item_Name.insert(1, " | ")
    item_Name.append(" " + skinFloat)
    print(str(item_Name) + " Refactor")
    return item_Name

def CloseName(item_Name):
    with open("data.json", 'r') as file:
        data = json.load(file)
        checkType = process.extractOne(item_Name[0], data.keys())
        if (checkType[1] >= 65 and checkType != None):
            print(checkType)
            item_Name[0] = checkType[0]
            checkSkin = process.extractOne(item_Name[2], data[item_Name[0]])
            if (checkSkin[1] >= 60):
                item_Name[2] = checkSkin[0]
    return item_Name

def isKnifeName(item_Name, time):
    isKnife = False
    item_Name = RefactorName(item_Name)
    for i in item_Name:
        if ("Knife" in i):
            isKnife = True
    if (isKnife == True):
        if (time == False):
            CloseName(item_Name)
            item_Name.insert(0, "★ ")
        else:
            splitted = item_Name[0].split()
            splitted.pop(0)
            splitted = " ".join(splitted)
            item_Name[0] = splitted
    elif (time == False):
        CloseName(item_Name)
    if (time == True):
        CollectingNames(item_Name)
    return "".join(item_Name)

def CollectingNames(item_Name):
    print(item_Name)
    with open("data.json", 'r+') as file:
        data = json.load(file)
        if (item_Name[0] not in data.keys()):
            data[item_Name[0]] = list()
            data[item_Name[0]].append(item_Name[2])
        elif (item_Name[2] not in data[item_Name[0]]):
            data[item_Name[0]].append(item_Name[2])
        file.seek(0)
        json.dump(data, file)

def SearchItems(key, name):
    Dicts = []
    #print(name)
    name = isKnifeName(name, False)
    print(name)
    Url = "https://market.csgo.com/api/v2/search-item-by-hash-name-specific?key=" + key + "&hash_name=" + name
    req = Get(Url + "/json").text
    soup = BeautifulSoup(req, "html.parser")
    try:
        source = json.loads(soup.text)
        #print("Try")
    except json.decoder.JSONDecodeError:
        source = "Uncoded"
        #print(soup.text)
        print("Except")
    if (source == "Uncoded"):
        print("Again Please")
    else:
        source = source["data"]
    if (len(source) == 0):
        print("Несуществует")
        return []
    else:
        name = isKnifeName(name, True)
        print(source)
        for i in range(len(source)):
            try:
                Dict = {"Name": name, "Price": ForPrice(str(source[i]["price"])),
                        "Float": float(source[i]["extra"]["float"]), "Id": source[i]["id"]}
                Dicts.append(Dict)
            except TypeError:
                source[i]["extra"] = "Error"
                print("Error")
        return Dicts

def Item_Search(Dict, id):
    for i in Dict:
        if i["Id"] == id:
            return i
            break