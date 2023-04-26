import telebot
from translate import Translator
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from time import sleep
from random import randint

API_TOKEN = "6142954404:AAH-llyGimAd4-1AznsC3mpEIfahl1kr_kI"

bot = telebot.TeleBot(API_TOKEN)

lista = open("blacklist.txt", 'r').read()
blacklist = lista.split(' ')

tradutor = Translator(from_lang='pt', to_lang='en')
sid = SentimentIntensityAnalyzer()


def separador(texto):
    a = str(texto).split(' ')
    return a


def roll(faces, dados):
    resultados = []
    for c in range(1, dados + 1):
        resultados.append(randint(1, faces))
    return resultados


@bot.message_handler(commands=['help', 'start', 'salve'])
def send_welcome(message):
    bot.reply_to(message, "Salve!")


# /r 1d10
@bot.message_handler(commands=['r', 'rolar'])
def rolar(message):
    try:
        texto = str(message.text)[3:].split('d')
        try:
            n = int(texto[0])
        except:
            n = 1
        f = int(texto[1])
        dados = roll(f, n)
        fraseRoll = f'{[x for x in dados]}, Resultado: {sum(dados)}'
        bot.reply_to(message, fraseRoll)
    except:
        bot.reply_to(message, "Erro")


def racismo(message):
    for item in separador(message.text.lower()):
        if item in blacklist:
            return True


@bot.message_handler(func=racismo)
def alerta(message):
    traduzido = tradutor.translate(message.text)
    sentimento = sid.polarity_scores(traduzido)
    if sentimento['neg'] > 0.3:
        bot.reply_to(message, "Cala a boca porra.")
        sleep(5)
        bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    elif sentimento['compound'] >= 0.1:
        pass
    else:
        bot.reply_to(message, "cuidado mano.")
    print(message.text)


bot.polling()
