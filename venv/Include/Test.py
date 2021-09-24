from Dictionary import Vocabulary

List = []
for item in Vocabulary["WeaponNames"]:
    print(item)
    if ("StatTrak™" in item):
        print("StatTrak")
        item = item.replace("StatTrak™ ", '')
    if ("★" in item):
        print("Knife")
        item = item.replace("★ ", '')
    for float in Vocabulary["floatR"]:
        float = f"({float})"
        if (float in item):
            print("Float: " + float)
            item = item.replace(float, '')
    print("Result: " + item)
    List.append(item)

with open('dataNames.txt', 'w', encoding='utf-8') as f:
    print(List, file=f, sep=", ")

# s = "★ Ursus Knife | Urban Masked (Well-Worn)"
# print(s.replace("(Well-Worn)", ''))