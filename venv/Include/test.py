'''
import telebot
import time
from work import ForCount, CompareIntents, InvalidInt
from SortingPrices import Prices
from Dictionary import Vocabulary

bot = telebot.TeleBot("1912654268:AAH--YX6lzy1lHSwNPYlCggrLfcdckC2pdE")
intents = []
proccess = 0

#----- Additional Functions:
def InvalidNumberIntent(Intent, nextFunc, parametr, message):
    print("Invalid")
    bot.send_message(message.chat.id,"Input is Made in Numbers,\nPlease Try Again...")
    print(intents)
    message.text = intents[Intent]
    if (Intent == 0):
        intents.pop(Intent)
    if (isinstance(parametr, telebot.types.Message) == True):
        Market(parametr, market=parametr.text)
    else:
        bot.register_next_step_handler(message, nextFunc, parametr)
#----

@bot.message_handler(commands=['prices'])
def startPrices(message):
    print("startPrices")
    intents.clear()
    # doc of prices
    msg = bot.send_message(message.chat.id, "Which Market:")
    bot.register_next_step_handler(msg, Market)

def Market(message, market=None):
    print("Sold " + str(message.text))
    if (market != None):
        message.text = market
    message.text.lower()
    if (CompareIntents(message.text, "steam") == "steam"):
        msg = bot.reply_to(message, "Number of Sales in the Last 24 Hours:")
        message.text = "steam"
        intents.append(message.text)
        bot.register_next_step_handler(msg, Arguments, "Sold")
    elif (CompareIntents(message.text, "market") == "market"):
        msg = bot.reply_to(message, "Curren Items Quantity on Sale:")
        message.text = "market"
        intents.append(message.text)
        bot.register_next_step_handler(msg, Arguments, "Sold")
    else:
        msg = bot.send_message(message.chat.id, "Check the Spelling of the Market Name and Write Down Again:")
        bot.register_next_step_handler(msg, Market)

def Arguments(message, step):
    print("Arguments " + message.text)
    if (InvalidInt(message.text) != "wrong"):
        if (step == "Sold"):
            intents.append(int(message.text))
            msg = bot.send_message(message.chat.id, "Item Price Stability Over the Last 7 Days:")
            bot.register_next_step_handler(msg, Arguments, "Stability")
        elif (step == "Stability"):
            intents.append(int(message.text))
            msg = bot.send_message(message.chat.id, "Upper Price Bar:")
            bot.register_next_step_handler(msg, Arguments, "topPrice")
        elif (step == "topPrice"):
            intents.append(int(message.text))
            msg = bot.send_message(message.chat.id, "How many variations do you want to display?")
            bot.register_next_step_handler(msg, PricesPrint)
    else:
        if (step == "Sold"):
            InvalidNumberIntent(0, Market, message, message)
        elif (step == "Stability"):
            InvalidNumberIntent(1, Arguments, "Stability", message)
        elif (step == "topPrice"):
            InvalidNumberIntent(2, Arguments, "topPrice", message)

def PricesPrint(message):
    print("PricesPrint")
    print("Count: " + message.text)
    print(intents)
    try:
        if (InvalidInt(message.text) != "wrong"):
            if (int(message.text) < 10):
                bot.send_message(message.chat.id, "Printing Results...")
                #time.sleep(1)
                bot.send_message(message.chat.id, ForCount(Prices(intents[0], intents[1], intents[2], intents[3]), int(message.text)))
            else:
                msg = bot.reply_to(message, "Too Large Number for Telegram, Please Write Down Again:")
                bot.register_next_step_handler(msg, PricesPrint)
    except ValueError:
        msg = bot.reply_to(message, "Invalid Number, Please Write Down Again:")
        bot.register_next_step_handler(msg, PricesPrint)

bot.polling(none_stop=True)
'''
int("str")

'''
def PricesPrint(message):
    print("PricesPrint")
    CountToDisplay = message.text
    parametrDict = dict()
    if (InvalidInt(CountToDisplay) != "wrong"):
        if (int(CountToDisplay) < messageLen):
            print("Count: " + CountToDisplay)
            CountToDisplay = int(CountToDisplay)
            bot.send_message(message.chat.id, "Printing Results...")
            #time.sleep(1)
            for i in Vocabulary["commands"]:
                if (i in intents.keys()):
                    parametrDict[i] = intents[i]
                else:
                    parametrDict[i] = None
            parametrDict["CountToDisplay"] = CountToDisplay
            print("Intents:")
            print(parametrDict)
            mainDict = ForCount(Prices(place=parametrDict["place"], sold=parametrDict["sold"], stability=parametrDict["stability"],
                                       tendence=parametrDict["tendence"], top_price=parametrDict["top_price"]), parametrDict["CountToDisplay"])
            bot.send_message(message.chat.id, "Found Results: " + str(len(Dict)))
            bot.send_message(message.chat.id, ForForm(mainDict))
        else:
            msg = bot.reply_to(message, "Too Large Number for Telegram, Please Write Down Again:")
            bot.register_next_step_handler(msg, PricesPrint)
    else:
        msg = bot.reply_to(message, "Invalid Number, Please Write Down Again:")
        bot.register_next_step_handler(msg, PricesPrint)
'''

#@bot.message_handler(func=lambda m: True)
# if (message.text == "Привет"):