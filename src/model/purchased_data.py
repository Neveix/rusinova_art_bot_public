import sqlite3
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src import PicturesBotManager

class PurchasedData:
    def __init__(self, path: str):
        self.con = sqlite3.connect(path)
        self.main_table_name = "PurchasedData"
    def create_tables(self):
        cur = self.con.cursor()
        column_defs = """
 payment_id TEXT PRIMARY KEY NOT NULL
,user_id INT NOT NULL
,when_time INT NOT NULL
,payed INT NOT NULL DEFAULT 0
"""
        cur.execute(f"CREATE TABLE IF NOT EXISTS {self.main_table_name} ({column_defs})")
        cur.close()
        self.con.commit()
    def add_purchased(self, payment_id: str, user_id: int, when_time: int):
        cur = self.con.cursor()
        cur.execute(f"INSERT INTO {self.main_table_name} (payment_id, user_id, when_time, payed) VALUES (?,?,?,0)",(
            payment_id, user_id, when_time
        ))
        cur.close()
        self.con.commit()
    def get_purchased(self, columns: str = "*", sql: str = "") -> list[tuple]:
        cur = self.con.cursor()
        result = cur.execute(f"SELECT {columns} FROM {self.main_table_name} {sql}").fetchall()
        cur.close()
        return result
    def delete_by_payment_id(self, payment_id: int):
        cur = self.con.cursor()
        cur.execute(f"DELETE FROM {self.main_table_name} WHERE payment_id = ?", (payment_id,)).fetchall()
        cur.close()
        self.con.commit()
    def set_payed(self, payment_id: int, payed: bool = True):
        cur = self.con.cursor()
        cur.execute(f"UPDATE {self.main_table_name} SET payed = ? WHERE payment_id = ?",
            (int(payed),payment_id))
        cur.close()
        self.con.commit()