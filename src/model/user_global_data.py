from sqlite3 import connect
from typing import TYPE_CHECKING\
    
if TYPE_CHECKING:
    from .pictures_bot_manager import PicturesBotManager
class UserGlobalData:
    def __init__(self, path: str):
        self.con = connect(path)
        self.main_table_name = "UserData"
        self.shipping_cart_table_name = "ShippingCart"
        self.paying_shipping_cart_table_name = "PayingShippingCart"
        self.favorite_pictures_table_name = "FavoritePictures"
        from .pictures_bot_manager import PicturesBotManager
        self.bot_manager: PicturesBotManager = None
    def set_bot_manager(self, bot_manager: "PicturesBotManager"):
        self.bot_manager = bot_manager
    def create_tables(self):
        cur = self.con.cursor()
        column_defs = """
 user_id INTEGER PRIMARY KEY NOT NULL
,first_name TEXT NOT NULL DEFAULT ''
,last_name TEXT
,username TEXT
"""
        cur.execute(f"CREATE TABLE IF NOT EXISTS {self.main_table_name} ({column_defs})")
        column_defs = """
 user_id INTEGER NOT NULL
,picture_id INTEGER NOT NULL"""
        cur.execute(f"CREATE TABLE IF NOT EXISTS {self.shipping_cart_table_name} ({column_defs})")
        cur.execute(f"CREATE TABLE IF NOT EXISTS {self.favorite_pictures_table_name} ({column_defs})")
        cur.execute(f"CREATE TABLE IF NOT EXISTS {self.paying_shipping_cart_table_name} ({column_defs})")
        cur.close()
        self.con.commit()
    def __del__(self):
        self.con.close()
    def add_to_shipping_cart(self, user_id: int, picture_id: int) -> None:
        cur = self.con.cursor()
        cur.execute(f"INSERT INTO {self.shipping_cart_table_name} (user_id, picture_id) VALUES (?,?)", (user_id, picture_id))
        cur.close()
        self.con.commit()
    def remove_from_shipping_cart(self, user_id: int, picture_id: int) -> None:
        cur = self.con.cursor()
        cur.execute(f"DELETE FROM {self.shipping_cart_table_name} WHERE user_id = ? AND picture_id = ?", (user_id, picture_id))
        cur.close()
        self.con.commit()
    def remove_from_all_shipping_carts(self, picture_id: int) -> None:
        cur = self.con.cursor()
        cur.execute(f"DELETE FROM {self.shipping_cart_table_name} WHERE picture_id = ?", (picture_id,))
        cur.execute(f"DELETE FROM {self.paying_shipping_cart_table_name} WHERE picture_id = ?", (picture_id,))
        cur.close()
        self.con.commit()
    def get_shipping_cart(self, user_id: int) -> list[int]:
        cur = self.con.cursor()
        fetched: list[tuple[int]] = cur.execute(f"SELECT (picture_id) FROM {self.shipping_cart_table_name} WHERE user_id = ?", (user_id,)).fetchall()
        result = [tupl[0] for tupl in fetched]
        cur.close()
        return result
    def set_paying_shipping_cart(self, user_id: int, picture_ids: list[int]):
        cur = self.con.cursor()
        cur.execute(f"DELETE FROM {self.paying_shipping_cart_table_name} WHERE user_id = ?", (user_id,))
        user_picture_id_pairs = [
            (user_id, picture_id) for picture_id in picture_ids
        ]
        cur.executemany(f"""INSERT INTO {self.paying_shipping_cart_table_name} VALUES (?,?)""", user_picture_id_pairs)
        cur.close()
        self.con.commit()
    def get_paying_shipping_cart(self, user_id: int) -> list[int]:
        cur = self.con.cursor()
        fetched: list[tuple[int]] = cur.execute(f"SELECT (picture_id) FROM \
{self.paying_shipping_cart_table_name} WHERE user_id = ?", (user_id,)).fetchall()
        cur.close()
        result = [tupl[0] for tupl in fetched]
        return result
    def add_to_favorite_pictures(self, user_id: int, picture_id: int) -> None:
        cur = self.con.cursor()
        cur.execute(f"INSERT INTO {self.favorite_pictures_table_name} (user_id, picture_id) VALUES (?,?)", (user_id, picture_id))
        cur.close()
        self.con.commit()
    def remove_from_favorite_pictures(self, user_id: int, picture_id: int) -> None:
        cur = self.con.cursor()
        cur.execute(f"DELETE FROM {self.favorite_pictures_table_name} WHERE user_id = ? AND picture_id = ?", (user_id, picture_id))
        cur.close()
        self.con.commit()
    def get_favorite_pictures(self, user_id: int) -> list[int]:
        cur = self.con.cursor()
        fetched: list[tuple[int]] = cur.execute(f"SELECT (picture_id) FROM {self.favorite_pictures_table_name} WHERE user_id = ?", (user_id,)).fetchall()
        result = [tupl[0] for tupl in fetched]
        cur.close()
        return result
    def set_user_advanced_data(self, user_id: int, 
            first_name: str, 
            last_name: str | None = None, 
            username: str | None = None):
        cur = self.con.cursor()
        exists_row = cur.execute(
f"SELECT EXISTS(\
    SELECT 1 FROM {self.main_table_name} WHERE user_id = ? LIMIT 1)"
, (user_id,)).fetchall()
        if exists_row[0][0]==0:
            cur.execute(f"INSERT INTO {self.main_table_name}\
(user_id, first_name, last_name, username) VALUES (?,?,?,?)",
(user_id, first_name, last_name, username))
        else:
            cur.execute(f"UPDATE {self.main_table_name} SET \
 first_name = ?, last_name = ?, username = ? WHERE user_id = ?", 
(first_name, last_name, username, user_id))
        cur.close()
        self.con.commit()
    def get_user_advanced_data(self, user_id: int, columns: str = "*") -> tuple:
        cur = self.con.cursor()
        result = cur.execute(f"SELECT {columns} FROM {self.main_table_name} WHERE user_id = ?", (user_id,)).fetchall()[0]
        cur.close()
        return result
    def get_max_name(self, user_id: int) -> str:
        first_name, last_name, username = self.get_user_advanced_data(user_id, "first_name, last_name, username")
        result = first_name
        if last_name:
            result += " " + last_name
        tech_data: list[str] = [f"user_id = {user_id}"]
        if username:
            tech_data.append(f"username = {username}")
        result += "(" + ", ".join(tech_data) + ")"
        return result