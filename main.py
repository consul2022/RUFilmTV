'''Основная библиотека для работы с телеграмм бот (подключает)'''
from aiogram import Bot, Dispatcher, executor

# Bot - взаимосвязь бота в телеграмме с питоном
# Dispatcher - связка между различным функионалом и ботом
# executor - исполнитель (выполняет работу программы)


'''Подключение типов, которые будут применены в боте'''
import asyncio  # библиотка для работы с асинхронным програмированием
from Constans import *
from DataBase import *
from Keyboards import *
from states import *  # хранилище состояний
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext  # содержание состояния state
from key import *
from random import shuffle # перемешивает фильмы рондомно

bot = Bot(BOT_TOKEN)
loop = asyncio.get_event_loop()  # асинхронный цикл
dp = Dispatcher(bot, loop, storage=MemoryStorage())

db = DataBase()
db.connect()


@dp.message_handler(state=Films.by_search)
async def finding_by_search(message: Message, state: FSMContext):
    films = db.select_film_by_name(message.text)
    # print(films)
    if films:
        for film in films:
            await bot.send_photo(chat_id=message.from_user.id, photo=film[0])
            await bot.send_message(chat_id=message.from_user.id, text=
            f"""*Название:* {film[1].capitalize()}
        
*Жанр:* {film[2]}

*Описание:* {film[3]}""", parse_mode="Markdown")  # управление шрифтами (* _ !)

            # **bold** жирным
            # __italic__ курсив
            # --underline-- подчеркивание
            # ~~strikethrough~~ перечёркнутый
            # [hyperlink](https://google.com) вставляем ссылку
            # [user mention](tg://user?id=12345) упоминание пользователя
            # `inline monospaced text`
            # ```block monospaced text```
            # ||spoiler||

            await bot.send_video(chat_id=message.from_user.id,
                                 video=film[4])

        await state.finish()
    else:
        await message.answer(text="Ничего не найдено, попробуйте ещё раз ")


@dp.message_handler(commands="start")
async def start_handler(message: Message):
    buttons = ReplyKeyboardMarkup(resize_keyboard=True)
    buttons.add(genres_btn, search_btn)

    await message.answer(
        text="Добро пожаловать в RUFilmTV, здесь Вы сможете найти фильм по жанру или в поисковике, на любой вкус. Приятного просмотра!",
        reply_markup=buttons)


@dp.callback_query_handler()
async def get_movie(callback: CallbackQuery):
    # ["Video", "1"]
    data = callback.data.split("|")
    print(db.select_video_by_id(data[1]))
    if data[0] == "Video":
        await bot.send_video(chat_id=callback.message.chat.id,
                             video=db.select_video_by_id(data[1])[0])


# content_types="text" - считывание запроса пользователя только по тексту
@dp.message_handler(content_types="text")  # декоратор - добавить функционал к функции
async def main_buttons_handler(message: Message):
    if message.text == genres_btn.text:  # список кнопок
        buttons = ReplyKeyboardMarkup(resize_keyboard=True)
        buttons.add(action_movie_btn, horrors_btn)
        buttons.add(comedies_btn, melodramas_btn)
        buttons.add(cartoons_btn, fantastic_btn)
        buttons.add(thriller_btn, adventures_btn)
        buttons.add(drama_btn, history_btn)
        buttons.add(back_to_menu_btn)
        await message.answer(text="Выберете желаем жанр фильма!", reply_markup=buttons)

    # elif message.text == cartoons_btn.text:
    #     await bot.send_video(chat_id=message.from_user.id,
    #                          video ="BAACAgIAAxkBAANsYl1xcBVMCMdb7Cq49nAg4fTFx8kAAvgTAAKoXOhKVcErsqn-3ZAkBA")
    # elif message.text == action_movie_btn.text:
    #     await bot.send_video(chat_id=message.from_user.id,
    #                          video ="BAACAgIAAxkBAAPBYmFkq15_Ar6V2PMM1l7LM9xQhwkAAtUVAAJ6HRBLDk8SF3aCjUokBA")
    # elif message.text == comedies_btn.text:
    #     await bot.send_video(chat_id=message.from_user.id,
    #                          video = "BAACAgIAAxkBAAOBYl2J55ja71_8rJ1qZSCyfXk-i6QAAjoYAALl4ulKA-L3it2edqIkBA")
    # elif message.text == horrors_btn.text:
    #     await bot.send_video(chat_id=message.from_user.id,
    #                          video = "BAACAgIAAxkBAAP8YmK5w12y17uFOAL3i9h-alox_J0AAqYXAALNdxhLqP0aycv6xVQkBA")
    # elif message.text == fantastic_btn.text:
    #     await bot.send_video(chat_id=message.from_user.id,
    #                          video = "BAACAgIAAxkBAAP7YmK4rKXXy2d4feRm9yB_ZzHaQ4oAAqwbAAIdHhFL5ghWrMD9AS4kBA")
    # elif message.text == melodramas_btn.text:
    #     await bot.send_video(chat_id=message.from_user.id,
    #                          video = "BAACAgIAAxkBAAIBL2Jiv-IXhZ7NJ8FqzAPqHLJ4gPaOAAK7GwACHR4RSzN6EFkHN_DWJAQ")
    elif message.text == search_btn.text:
        await bot.send_message(chat_id=message.from_user.id, text="Введите название фильма")
        await Films.by_search.set()
    elif message.text == back_to_menu_btn.text:
        buttons = ReplyKeyboardMarkup(resize_keyboard=True)
        buttons.add(genres_btn, search_btn)
        await message.answer(text="Вы вернулись в главное меню!", reply_markup=buttons)
    else:
        # смайлик Мелодраммы
        films = db.select_film_by_genre(message.text.split()[1][:-1])
        for film in films:
            await bot.send_photo(chat_id=message.from_user.id, photo=film[0])
            buttons = InlineKeyboardMarkup()
            watch_movie_btn.callback_data = f"Video|{film[4]}"
            buttons.add(watch_movie_btn)

            await bot.send_message(chat_id=message.from_user.id, text=f"""*Название:* {film[1].capitalize()}

*Жанр:* {film[2]}

*Описание:* {film[3]}""", parse_mode="Markdown", reply_markup=buttons)  # управление шрифтами (* _ !)


executor.start_polling(dp)
