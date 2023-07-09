# Учебный бот, работающий по бесконечному циклу while.
# Отвечает на запросы типовой фразой и показывает по запросу картинки собачек, котиков и лисичек

import requests
import tokens_bots

# функция проверки статуса ответа сервера
def get_result(response, link):
    if response.status_code == 200:
        requests.get(f'{API_URL}{BOT_TOKEN}/sendPhoto?chat_id={chat_id}&photo={link}')
    else:
        requests.get(f'{API_URL}{BOT_TOKEN}/sendMessage?chat_id={chat_id}&text={ERROR_TEXT}')

def do_something() -> None:
    print('Был апдейт')

# API сервисов с картинками котиков, собачек, лисичек и Телеграм
API_URL: str = 'https://api.telegram.org/bot'
API_CATS_URL: str = 'https://api.thecatapi.com/v1/images/search'
API_DOGS_URL: str = 'https://random.dog/woof.json'
API_FOX_URL: str = 'https://randomfox.ca/floof/'

BOT_TOKEN: str = tokens_bots.token_bot1    # токен бота, полученный у @BotFather
# Типовой ответ бота на любой запрос не связанный с котами, собаками и лисами
TEXT = 'Не понял чего ты хочешь, но я могу показывать фотки котиков, собачек или лисичек :))'
# Типовой ответ бота на ошибку сервисов с картинками
ERROR_TEXT: str = 'Здесь должна была быть картинка :('

offset: int = -2
timeout: int = 60  # соединение закрывается где-то за 50-60 секунд

while True:
    updates = requests.get(f'{API_URL}{BOT_TOKEN}/getUpdates?offset={offset + 1}&timeout={timeout}').json()

    # если есть апдейт в боте
    if updates['result']:
        for result in updates['result']:
            massage_from_user = str(result['message']['text']).lower()  # считываем запрос пользователя
            offset = result['update_id']                                # сохраняем последний запрос
            chat_id = result['message']['from']['id']                   # сохраняем id с которого пришел запрос

            # если в запросе нет слов 'кот', 'соба', 'лис' - выводим ответ бота TEXT
            if not any([v in massage_from_user for v in ['кот', 'соба', 'лис']]):
                requests.get(f'{API_URL}{BOT_TOKEN}/sendMessage?chat_id={chat_id}&text={TEXT}')

            # если в запросе есть слово 'кот' - выводим ответ бота фото кота
            elif 'кот' in massage_from_user:
                response = requests.get(API_CATS_URL)
                link = response.json()[0]['url']
                get_result(response, link)

            # если в запросе есть слово 'соба' - выводим ответ бота фото собаки
            elif 'соба' in massage_from_user:
                response = requests.get(API_DOGS_URL)
                link = response.json()['url']
                get_result(response, link)

            # если в запросе есть слово 'лис' - выводим ответ бота фото лисы
            elif 'лис' in massage_from_user:
                response = requests.get(API_FOX_URL)
                link = response.json()['image']
                get_result(response, link)

            do_something()
