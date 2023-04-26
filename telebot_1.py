import telebot
from translate import Translator
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from time import sleep
from random import randint

API_TOKEN = "----------"
# NÃO VAZE O TOKEN NO GITHUB (denovo)!!!!!!

# Cria uma instância da classe bot com o token do bot que o programa vai usar
bot = telebot.TeleBot(API_TOKEN)
# Criando instâncias do tradutor e do vader
tradutor = Translator(from_lang='pt', to_lang='en')
sid = SentimentIntensityAnalyzer()

# Abrindo o blacklist
lista = open("blacklist.txt", 'r').read()
blacklist = lista.split(' ')


# Dependências do programa
def separador(texto):
    a = str(texto).split(' ')
    return a


def roll(faces, dados):
    resultados = []
    for c in range(1, dados + 1):
        resultados.append(randint(1, faces))
    fraseRoll = f'{[x for x in dados]}, Resultado: {sum(dados)}'
    return fraseRoll


def racismo(texto):
    for item in separador(texto.text.lower()):
        if item in blacklist:
            return True


# >>>>> Funções do bot <<<<<<
# Função Inicial
@bot.message_handler(commands=['help', 'start', 'salve'])
def send_welcome(message):
    bot.reply_to(message, "Salve!")


#Função Dado
@bot.message_handler(commands=['r', 'rolar'])
def rolar(message):
    try:
        texto = str(message.text)[3:].split('d')
        try:
            n = int(texto[0])
        except:
            # Se alguém digitar um caractere inválido ou nada vai reverter para 1.
            n = 1
        f = int(texto[1])
        dados = roll(f, n)
        bot.reply_to(message, dados)
    except:
        bot.reply_to(message, "Erro")


# Função anti-processo
@bot.message_handler(func=racismo)
def alerta(message):
    traduzido = tradutor.translate(message.text)
    sentimento = sid.polarity_scores(traduzido)
    if sentimento['neg'] > 0.1:
        bot.reply_to(message, "Cala a boca porra.")
        sleep(3)
        bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    elif sentimento['compound'] >= 0.1:
        pass
    else:
        bot.reply_to(message, "cuidado mano.")
    print(message.text)


bot.polling()
# Deixa o bot rodando até o processo ser parado.
