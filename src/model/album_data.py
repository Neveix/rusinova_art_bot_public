import sqlite3
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .pictures_bot_manager import PicturesBotManager

class AlbumData:
    def __init__(self, path: str):
        self.con = sqlite3.connect(path)
        self.main_table_name = "AlbumsData"
        self.pictures_table_name = "AlbumPictures"
        self.bot_manager = None
    def create_tables(self):
        cur = self.con.cursor()
        cur.execute(f"""CREATE TABLE IF NOT EXISTS {self.main_table_name} (
 id INTEGER PRIMARY KEY AUTOINCREMENT
,name TEXT NOT NULL DEFAULT ''
,photo_size TEXT NOT NULL DEFAULT ''
)""")
        cur.execute(f"""CREATE TABLE IF NOT EXISTS {self.pictures_table_name} (
 id INT
,picture_id INT
)""")
        cur.close()
        self.con.commit()
    def set_bot_manager(self, bot_manager: "PicturesBotManager"):
        self.bot_manager = bot_manager
        bot_manager.album_data = self
    def add(self, name: str, photo_size: str):
        cur = self.con.cursor()
        cur.execute(f"INSERT INTO {self.main_table_name} (name, photo_size) VALUES (?,?)", (name, photo_size))
        cur.close()
        self.con.commit()
    def set_name(self, album_id: int, name: str):
        cur = self.con.cursor()
        cur.execute(f"UPDATE {self.main_table_name} SET name = ? WHERE id = ?",(name,album_id))
        cur.close()
        self.con.commit()
    def set_photo(self, album_id: int, photo_size: str):
        cur = self.con.cursor()
        cur.execute(f"UPDATE {self.main_table_name} SET photo_size = ? WHERE id = ?",(photo_size,album_id))
        cur.close()
        self.con.commit()
    def remove(self, album_id: int):
        cur = self.con.cursor()
        cur.execute(f"DELETE FROM {self.main_table_name} WHERE id = ?", (album_id,))
        cur.close()
        self.con.commit()
    def browse(self, page: int, columns: str = "*", filter_text: str = "") -> list[tuple]:
        cur = self.con.cursor()
        result = cur.execute(f"SELECT {columns} FROM {self.main_table_name} {filter_text} LIMIT 1 OFFSET {page}").fetchall()
        cur.close()
        return result
    def get_by_id(self, album_id: int, columns: str = "*", sql: str = "") -> tuple:
        cur = self.con.cursor()
        result = cur.execute(f"SELECT {columns} FROM {self.main_table_name} WHERE id = ? {sql}", (album_id,)).fetchall()
        cur.close()
        return result[0]
    def count_albums(self, filter_text: str = "") -> int:
        cur = self.con.cursor()
        result = cur.execute(f"SELECT COUNT() FROM {self.main_table_name} {filter_text}").fetchall()[0][0]
        cur.close()
        return result
    def add_picture(self, album_id: int, picture_id: int):
        cur = self.con.cursor()
        cur.execute(f"INSERT INTO {self.pictures_table_name} (id, picture_id) VALUES (?,?)", (album_id, picture_id))
        cur.close()
        self.con.commit()
    def remove_picture(self, album_id: int, picture_id: int):
        cur = self.con.cursor()
        cur.execute(f"DELETE FROM {self.pictures_table_name} WHERE id = ? AND picture_id = ?", (album_id, picture_id))
        cur.close()
        self.con.commit()
    def get_pictures(self, album_id: int, sql: str = "") -> list[int]:
        cur = self.con.cursor()
        result = cur.execute(f"SELECT picture_id FROM {self.pictures_table_name} WHERE id = ? {sql}", (album_id,)).fetchall()
        result = [t[0] for t in result]
        cur.close()
        return result
    def set_pictures(self, album_id: int, picture_ids: list[int]):
        cur = self.con.cursor()
        cur.execute(f"DELETE FROM {self.pictures_table_name} WHERE id = ?",(album_id,))
        values = [(album_id, picture_id) for picture_id in picture_ids]
        cur.executemany(f"INSERT INTO {self.pictures_table_name} (id, picture_id) VALUES (?,?)",values)
        cur.close()
        self.con.commit()
    def generate_filter_text(self, user_id: int) -> str:
        user_data = self.bot_manager.user_data_manager.get(user_id)
        checkout_id: int | None = user_data.albums_browse_checkout_id
        and_filters: list[str] = []
        if checkout_id is not None:
            and_filters.append(f"id = {checkout_id}")
        if not and_filters: # and_filters == []
            return ""
        result = "WHERE "
        result += " AND ".join(
            [f"({and_filter})" for and_filter in and_filters]
        )
        return result
    def count_final(self, user_id: int) -> int:
        filter_text = self.generate_filter_text(user_id)
        return self.count_albums(filter_text)
    def browse_and_count_final(self, user_id: int, columns: str = "*"):
        page = self.bot_manager.user_data_manager.get(user_id).albums_browse_page
        filter_text = self.generate_filter_text(user_id)
        browse_result = self.browse(page, columns, filter_text)
        count_result = self.count_albums(filter_text)
        return browse_result, count_result