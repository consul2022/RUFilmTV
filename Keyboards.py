from aiogram.types import *

genres_btn = KeyboardButton(text="🎬 Жанры")
search_btn = KeyboardButton(text="🔎 Поиск")

action_movie_btn = KeyboardButton(text="🔫 Боевики")
comedies_btn = KeyboardButton(text="🎭 Комедии")
horrors_btn = KeyboardButton(text="🩸 Ужасы")
cartoons_btn = KeyboardButton(text="👶 Мультфильмы")
fantastic_btn = KeyboardButton(text="👽 Фантастика")
melodramas_btn = KeyboardButton(text="❤ Мелодрамы")
back_to_menu_btn = KeyboardButton(text="⬅ Назад в меню")
thriller_btn = KeyboardButton(text="👻 Триллер")
adventures_btn = KeyboardButton(text="🗺 Приключения")
drama_btn = KeyboardButton(text="😢 Драма")
history_btn = KeyboardButton(text="🏛️ История")
show_more_btn = KeyboardButton(text="👌 Показать ещё фильмы")



watch_movie_btn = InlineKeyboardButton(text="📺 Смотреть фильм")


text_buttons = [action_movie_btn.text,
                comedies_btn.text,
                horrors_btn.text,
                cartoons_btn.text,
                fantastic_btn.text,
                melodramas_btn.text,
                back_to_menu_btn.text,
                thriller_btn.text,
                adventures_btn.text,
                drama_btn.text,
                history_btn.text,
                show_more_btn.text]
