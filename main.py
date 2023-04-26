from translate import Translator

tradutor = Translator(to_lang='en', from_lang='pt')

traduzido = tradutor.translate('Bom dia meu caro.')
print(traduzido)