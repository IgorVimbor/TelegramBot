# Бот-2_эхо-бот с картинками (с клавишами)
# Повторяет отправленное пользователем сообщение (текст, фото, видео, картинки и др.),
# кроме команд start и help и если в сообщении нет слов 'кот', 'соба', 'пес', 'лис'.
# В ответ на эти запросы свои обработчики.
# Регистрирация обработчиков (хэндлеров) через декораторы.

from aiogram import Bot, Dispatcher
from aiogram.filters import Command, Text
from aiogram.types import KeyboardButton, Message, ReplyKeyboardMarkup
import bot_tokens
import requests


# API сайтов для скачивания фотографий
API_CATS_URL: str = 'https://api.thecatapi.com/v1/images/search'
API_DOGS_URL: str = 'https://random.dog/woof.json'
API_FOX_URL: str = 'https://randomfox.ca/floof/'

API_TOKEN: str = bot_tokens.token_bot2        # токен бота (вставляем свой)

animals = ['кот', 'соба', 'пес', 'пёс', 'лис']    # список слов для фильтра

# Создаем объекты бота и диспетчера
bot: Bot = Bot(token=API_TOKEN)
dp: Dispatcher = Dispatcher()

# Создаем объекты кнопок
button_1: KeyboardButton = KeyboardButton(text='Старт')
button_2: KeyboardButton = KeyboardButton(text='Информация')
button_3: KeyboardButton = KeyboardButton(text='Котик')
button_4: KeyboardButton = KeyboardButton(text='Собачка')
button_5: KeyboardButton = KeyboardButton(text='Лисичка')

# Создаем объект клавиатуры, добавляя в него кнопки
keyboard: ReplyKeyboardMarkup = ReplyKeyboardMarkup(
    keyboard=[[button_1, button_2],
              [button_3, button_4, button_5]],
    resize_keyboard=True)


# Этот хэндлер будет срабатывать на команду "/start" и кнопку "Старт"
# и отправлять в чат клавиатуру
@dp.message(Command(commands=["start"]))
@dp.message(Text(text='Старт'))
async def process_start_command(message):
    if message.from_user.first_name:
        text = f'Привет, {message.from_user.first_name}!'
    else:
        text = 'Привет!'
    await message.answer(f'{text}\nЯ эхо-бот с картинками!\nЕсли хочешь - '
                         f'можешь мне что-нибудь прислать и я отправлю тебе '
                         f'копию твоего сообщения или нажми кнопку "Информация" '
                         f'... там дополнительная интересная информация :))',
                         reply_markup=keyboard)


# хэндлер будет срабатывать на команду "/help" и кнопку "Информация"
@dp.message(Command(commands=["help"]))
@dp.message(Text(text='Информация'))
async def process_help_command(message: Message):
    await message.answer('Я просто отправляю тебе копию сообщения, но...еще я умею показывать '
                         'картинки котиков, собачек или лисичек по твоему запросу :)) '
                         '\nТы можешь отправить письменный запрос или нажать нужную кнопку.')


# хэндлер срабатывает, если в запросе есть слова из списка animals и на кнопки
# "Котик", "Собачка", "Лисичка". В ответ бот отправляет фото животных.
@dp.message(Text(contains=['Котик', 'Собачка', 'Лисичка']))
@dp.message(lambda msg: any(word in msg.text.lower() for word in animals))
async def send_picture(message: Message):
    msg = str(message.text).lower()
    try:
        if 'кот' in msg:
            response = requests.get(API_CATS_URL)
            if response.status_code == 200:
                link = response.json()[0]['url']
        elif any([value in msg for value in ('соба', 'пес', 'пёс')]):
            response = requests.get(API_DOGS_URL)
            if response.status_code == 200:
                link = response.json()['url']
        elif 'лис' in msg:
            response = requests.get(API_FOX_URL)
            if response.status_code == 200:
                link = response.json()['image']
        await bot.send_photo(chat_id=message.chat.id, photo=link)
    except TypeError:
        await message.reply(text='Ошибка! Я не понял, чего ты хочешь? :((')


# хэндлер будет срабатывать на любые сообщения, кроме команд
# "/start" и "/help" и если в сообщении нет слов из списка animals
# метод send_copy вернет входящее сообщение во всех форматах
@dp.message(~Text(contains=animals, ignore_case=True))
async def send_echo(message: Message):
    try:
        await message.send_copy(chat_id=message.chat.id)
    except TypeError:
        await message.reply(text='Ошибка! Я не понял, чего ты хочешь? :((')


if __name__ == '__main__':
    dp.run_polling(bot)
