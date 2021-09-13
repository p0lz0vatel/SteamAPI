import telebot
import time
from work import ForCount, CompareIntents, InvalidInt, ForForm
from SortingPrices import Prices, ValueSearch
from Dictionary import Vocabulary

bot = telebot.TeleBot("1912654268:AAH--YX6lzy1lHSwNPYlCggrLfcdckC2pdE")
intents = {}
messageLen = 100
proccess = 0

#----- Additional Functions:
def CollectingIntents(message, chain, element, enter=None):
    if (element != len(chain) - 1):
        message.text = InvalidNumberIntent(message, chain, element)
        if (message.text != "command"):
            if (message.text != "wrong"):
                if (len(chain) - 1 != element):
                    msg = bot.send_message(message.chat.id, chain[element + 1][1])
                bot.register_next_step_handler(msg, CollectingIntents, chain, element + 1)
            else:
                msg = bot.reply_to(message, "Input is Made in Numbers,\nPlease Try Again...")
                bot.register_next_step_handler(msg, CollectingIntents, chain, element)
        else:
            msg = bot.send_message(message.chat.id, chain[element][1])
            bot.register_next_step_handler(msg, CollectingIntents, chain, element)
    else:
        PricesPrint(message)

def InvalidNumberIntent(message, chain, element):
    if (message.text not in Vocabulary["bot_commands"]):
        if (InvalidInt(message.text) != "wrong"):
            print("new intent " + message.text + " Valid")
            intents[chain[element][0]] = int(message.text)
            return message.text
        else:
            print("new intent " + message.text + " Invalid")
            return "wrong"
    else:
        return "command"

def PricesPrint(message):
    print("PricesPrint")
    print("Intents:\n" + str(intents))
    if (InvalidInt(message.text) != "wrong"):
        if (int(message.text) < messageLen):
            CountToDisplay = int(message.text)
            print("Count: " + str(CountToDisplay))
            if (intents["param"] == "prices"):
                bot.send_message(message.chat.id, "Printing Results...")
                parametrDict = dict()
                for i in Vocabulary["commands"]:
                    if (i in intents.keys()):
                        parametrDict[i] = intents[i]
                    else:
                        parametrDict[i] = None
                parametrDict["CountToDisplay"] = CountToDisplay
                print("Parametrs: " + str(parametrDict["CountToDisplay"]))
                mainDict = ForCount(Prices(place=parametrDict["place"], sold=parametrDict["sold"], stability=parametrDict["stability"],
                                           tendence=parametrDict["tendence"], top_price=parametrDict["top_price"]), parametrDict["CountToDisplay"])
                #bot.send_message(message.chat.id, "Found Results: " + str(len(mainDict)))
                bot.send_message(message.chat.id, ForForm(mainDict))
            elif (intents["param"] == "value"):
                bot.send_message(message.chat.id, "Printing Results...")
                mainDict = ForCount(ValueSearch(Vocabulary["sortingParam"][str(intents["valueS"])], Vocabulary["True/False"][str(intents["reverse"])]), CountToDisplay)
                bot.send_message(message.chat.id, ForForm(mainDict))
        else:
            msg = bot.reply_to(message, "Too Large Number for Telegram, Please Write Down Again:")
            bot.register_next_step_handler(msg, PricesPrint)
    else:
        msg = bot.reply_to(message, "Invalid Number, Please Write Down Again:")
        bot.register_next_step_handler(msg, PricesPrint)
#-----

@bot.message_handler(commands=['tosteam'])
def Steam(message):
    print("toSteam")
    intents.clear()
    intents["place"] = "market"
    intents["param"] = "prices"
    msg = bot.send_message(message.chat.id, "Some Documentation...")
    chain = list([["sold", "Currency Number of Items on Sale:"], ["top_price", "Upper Price Bar:"], ["CountToDisplay", "How many variations do you want to display?"]])
    CollectingIntents(message, chain, 0)

@bot.message_handler(commands=['tomarket'])
def toMarket(message):
    print("toMarket")
    intents.clear()
    intents["place"] = "steam"
    intents["param"] = "prices"
    msg = bot.send_message(message.chat.id, "Some Documentation...")
    chain = list([["sold", "Number of Sales in the Last 24 Hours:"], ["top_price", "Upper Price Bar:"], ["stability", "Stability Coefficient:"],
                  ["tendence", "Number of Price Change Over the Past 30 Days:"], ["CountToDisplay", "How many variations do you want to display?"]])
    CollectingIntents(message, chain, 0)

@bot.message_handler(commands=['tosort'])
def toSort(message):
    print("tovaluesort")
    intents.clear()
    intents["param"] = "value"
    msg = bot.send_message(message.chat.id, "Some Documentation...")
    chain = list([["valueS", "Parameter from the Presented:"], ["reverse", "Is Reversed?\n 1 - True\n 0 - False"], ["CountToDisplay", "How many variations do you want to display?"]])
    CollectingIntents(message, chain, 0)

bot.polling(none_stop=True)

#@bot.message_handler(func=lambda m: True)
# if (message.text == "Привет"):