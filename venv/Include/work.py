import json
from fuzzywuzzy import fuzz, process

key = "9593LueQz7Q5sfLzJ0FhJ41z872q8L7"

def ForCount(Dict, Count):
    if (Count == None):
        return json.dumps(Dict, indent=4)
    else:
        new_Dict = []
        for i in range(Count):
            new_Dict.append(Dict[i])
        return json.dumps(new_Dict, indent=4)

def ForForm(DictF):
    print("Forming Dict...")
    Dict = json.loads(DictF)
    strList = list()
    for i in Dict:
        for key in i.keys():
            loc_Dict = i[key]
            strList.append('Name: {skin_name}\n'
                           ' Market:\n'
                           '  Price: {market_price}\n'
                           '  On Sale: {on_sale}\n'
                           ' Steam:\n'
                           '  Average Price: {avg_price_24}\n'
                           '  With Discount: {with_discount}\n'
                           '  Sold: {sold}\n'
                           ' Specifications:\n'
                           '  Tendence for 30 days: {tendence_30d}\n'
                           '  Deviation for 7 days: {deviation_7d}\n'
                           '  Price difference: {price_difference}\n'
                           '-----'.format(
                skin_name=key, market_price=loc_Dict["Market_Price"]["Price"], on_sale=loc_Dict["Market_Price"]["OnSale"],
                avg_price_24=loc_Dict["Steam_Price"]["Avg_Price_24"], with_discount=loc_Dict["Steam_Price"]["with_discount"], sold=loc_Dict["Steam_Price"]["Sold"],
                tendence_30d=loc_Dict["specifications"]["tendence_30d"], deviation_7d=loc_Dict["specifications"]["deviation_7d"], price_difference=abs(loc_Dict["specifications"]["price_difference"])))
    Dict = '\n'.join(strList)
    return Dict

def CompareIntents(user_word, expected_word, List=None):
    if (List == None):
        if (fuzz.ratio(user_word, expected_word) >= 60):
            user_word = expected_word
        else:
            user_word = "wrong"
    else:
        closeWords = process.extractOne(user_word, expected_word)
        print(closeWords)
        if (closeWords[1] >= 80):
            user_word = closeWords[0]
        else:
            user_word = "wrong"
    return user_word

def InvalidInt(message):
    try:
        message = int(message)
        return message
    except ValueError:
        return "wrong"

def RefactorName(name, float, tag):
    if ("★" in name):
        nameList = name.split(" ", 1)
        name = nameList[1]
        tag = nameList[0] + " " + tag
    nameR = str(f"{tag}{name}{float}")
    return nameR

# print(RefactorName("★ Desert Eagle | Directive", "Factory New", "StatTrak "))
# print("LOX")