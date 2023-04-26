import telebot
from translate import Translator
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from time import sleep

API_TOKEN = "------"

bot = telebot.TeleBot(API_TOKEN)

blacklist = ['branco', 'preto', 'negro', 'pardo', 'branca', 'preta', 'negra', 'parda', 'pardola', 'escravo', 'escrava',
             'favelada', 'louça', 'favelado', 'favelados', 'faveladas', 'brancos', 'pretos', 'negros', 'pardos',
             'brancas', 'pardas', 'negras', 'pardolas', 'escravos', 'escravas', 'macaco', 'alforriado', 'bicha',
             'boiola', 'gay', 'viado', 'pardinhas', 'pardinhos', 'pardinho', 'pardinha', 'neguinho', 'neguinha',
             'negrinho', 'negrinha', 'neguinhos', 'neguinhas', 'negrinhos', 'negrinhas', 'hitler', 'nazismo', 'nazista']

tradutor = Translator(from_lang='pt', to_lang='en')
sid = SentimentIntensityAnalyzer()


def separador(texto):
    a = str(texto).split(' ')
    return a


@bot.message_handler(commands=['help', 'start', 'salve'])
def send_welcome(message):
    bot.reply_to(message, "Salve!")


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
