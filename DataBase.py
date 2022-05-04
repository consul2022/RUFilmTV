from sqlite3 import *

# fetchone получить один из запроса пользователя с базы данных
# fetchall получить всё из запроса пользователя с базы данных
class DataBase:
    def connect(self):
        self.film = connect('RUFilm_TV_database.db')
        self.cur = self.film.cursor()

    def select_film_by_name(self, name):
        requests = self.cur.execute(
            f"SELECT Poster, Name, Genre, Description, Video FROM Films WHERE Name LIKE '%{name.lower()}%'").fetchall()
        return requests

    def select_film_by_genre(self, genre):
        requests_genre = self.cur.execute(
            f"SELECT Poster, Name, Genre, Description, id, Year FROM Films WHERE Genre LIKE '%{genre}%'").fetchall()
        return requests_genre

    def select_video_by_id(self, id):
        requests_id = self.cur.execute(f"SELECT Video FROM Films WHERE id = {id}").fetchone()
        return requests_id