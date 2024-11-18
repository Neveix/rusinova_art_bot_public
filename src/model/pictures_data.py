import sqlite3
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src import PicturesBotManager

class PicturesData:
    def __init__(self, path: str):
        self.con = sqlite3.connect(path)
        self.main_table_name = "PicturesData"
        self.photos_table_name = "PicturesPhoto"
        self.bot_manager = None
    def create_tables(self):
        cur = self.con.cursor()
        column_defs = """
 id INTEGER PRIMARY KEY AUTOINCREMENT
,name TEXT
,description TEXT
,price INTEGER
,is_buyed INTEGER NOT NULL DEFAULT 0
"""
        cur.execute(f"CREATE TABLE IF NOT EXISTS {self.main_table_name} ({column_defs})")
        column_defs = """
 id INTEGER
,photo_size TEXT
"""
        cur.execute(f"CREATE TABLE IF NOT EXISTS {self.photos_table_name} ({column_defs})")
        cur.close()
        self.con.commit()
    def set_bot_manager(self, bot_manager: "PicturesBotManager"):
        self.bot_manager = bot_manager
    def add_column(self, column_def: str):
        cur = self.con.cursor()
        cur.execute(f"ALTER TABLE {self.main_table_name} ADD COLUMN {column_def}")
        cur.close()
        self.con.commit()
    def __del__(self):
        self.con.close()
    def add(self, name: str, description: str, price: int, photo_size_list: list[str]):
        cur = self.con.cursor()
        result = cur.execute(f"""INSERT INTO {self.main_table_name} (name, description, price) VALUES (?,?,?)
RETURNING id""",
(name, description, price)).fetchall()
        picture_id = result[0][0]
        values = [(picture_id, photo) for photo in photo_size_list]
        cur.executemany(f"INSERT INTO {self.photos_table_name} (id, photo_size) VALUES (?,?)", values)
        cur.close()
        self.con.commit()
    def set_name(self, picture_id: int, name: str):
        cur = self.con.cursor()
        cur.execute(f"UPDATE {self.main_table_name} SET name = ? WHERE id = ?", (name, picture_id))
        cur.close()
        self.con.commit()
    def set_description(self, picture_id: int, description: str):
        cur = self.con.cursor()
        cur.execute(f"UPDATE {self.main_table_name} SET description = ? WHERE id = ?", (description, picture_id))
        cur.close()
        self.con.commit()
    def set_price(self, picture_id: int, price: int):
        cur = self.con.cursor()
        cur.execute(f"UPDATE {self.main_table_name} SET price = ? WHERE id = ?", (price, picture_id))
        cur.close()
        self.con.commit()
    def set_photo_size_list(self, picture_id: int, photo_size_list: list[str]):
        cur = self.con.cursor()
        cur.execute(f"DELETE FROM {self.photos_table_name} WHERE id = ?", (picture_id,))
        pairs = [(picture_id, photo_size) for photo_size in photo_size_list]
        cur.executemany(f"INSERT INTO {self.photos_table_name} (id, photo_size) VALUES (?,?)",pairs)
        cur.close()
        self.con.commit()
    def get_photo_size_list(self, picture_id: int = -1) -> list[str]:
        cur = self.con.cursor()
        result = cur.execute(f"SELECT photo_size FROM {self.photos_table_name} WHERE id = ?", (picture_id,)).fetchall()
        result = [tupl[0] for tupl in result]
        cur.close()
        return result
    def delete(self, picture_id: int):
        cur = self.con.cursor()
        cur.execute(f"DELETE FROM {self.main_table_name} WHERE id = ?",(picture_id,))
        cur.close()
        self.con.commit()
    def browse(self, page: int, count: int, columns: str = "*", sql: str = "") -> list[tuple]:
        cursor = self.con.cursor()
        limit_str = ""
        if count != -1:
            limit_str = f"LIMIT {count} OFFSET {page*count}"
        result = cursor.execute(f"SELECT {columns} FROM {self.main_table_name} {sql} {limit_str}").fetchall()
        cursor.close()
        return result
    def get_by_id(self, picture_id: int = -1, columns: str = "*"):
        return self.browse(0, 1, columns, f"WHERE id = {picture_id}")[0]
    def count(self, sql: str = "") -> int:
        cursor = self.con.cursor()
        result = cursor.execute(f"SELECT COUNT(*) FROM {self.main_table_name} {sql}").fetchone()[0]
        cursor.close()
        return result
    def generate_filter_text(self, user_id: int) -> str:
        user_data = self.bot_manager.user_data_manager.get(user_id)
        and_filters: list[str] = []
        if user_data.pictures_browse_filter != "":
            for symbol in user_data.pictures_browse_filter:
                symbol_ord = ord(symbol)
                filter_element = f"name LIKE '%{symbol}%'"
                if 1040 <= symbol_ord <= 1071:
                    filter_element += f" OR name LIKE '%{chr(symbol_ord+32)}%'"
                elif 1072 <= symbol_ord <= 1103:
                    filter_element += f" OR name LIKE '%{chr(symbol_ord-32)}%'"
                filter_element = f"({filter_element})"
                and_filters.append(filter_element)
        if user_data.pictures_favorites_mode:
            favorites_list = self.bot_manager.user_global_data.get_favorite_pictures(user_id)
            and_filters.append(f"id IN ({",".join([str(pic) for pic in favorites_list])})")
        if user_data.pictures_shipping_cart_mode:
            shipping_cart = self.bot_manager.user_global_data.get_shipping_cart(user_id)
            and_filters.append(f"id IN ({",".join([str(pic) for pic in shipping_cart])})")
        if user_data.pictures_album_mode:
            album_pictures = self.bot_manager.album_data.get_pictures(user_data.albums_browse_album_id)
            and_filters.append(f"id IN ({",".join([str(pic) for pic in album_pictures])})")
        if user_data.pictures_buyed_mode:
            and_filters.append("is_buyed = 1")
        else:
            and_filters.append("is_buyed = 0")
        result = "WHERE " + " AND ".join(and_filters)
        return result
    def count_final(self, user_id: int):
        filter_text = self.generate_filter_text(user_id)
        return self.count(filter_text)
    def browse_and_count_final(self, user_id: int, columns: str = "*"):
        page = self.bot_manager.user_data_manager.get(user_id).pictures_browse_page
        filter_text = self.generate_filter_text(user_id)
        browse_result = self.browse(page, 1, columns, filter_text)
        count_result = self.count(filter_text)
        return browse_result, count_result
    def set_buyed(self, picture_id: int, buyed: bool = False) -> None:
        cur = self.con.cursor()
        cur.execute(f"UPDATE {self.main_table_name} SET is_buyed = ? WHERE id = ?", (int(buyed), picture_id))
        cur.close()
        self.con.commit()
    def get_buyed(self, picture_id: int) -> bool:
        cur = self.con.cursor()
        result = cur.execute(f"SELECT is_buyed FROM {self.main_table_name} WHERE id = ?", (picture_id,)).fetchall()
        cur.close()
        if not result:
            raise ValueError(f"No picture from under id = {picture_id}")
        else:
            return bool(result[0][0])