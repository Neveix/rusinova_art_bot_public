from typing import TYPE_CHECKING
from telegram import Update
from tg_bot_base import ButtonRows, ButtonRow, Button, Menu
from tg_bot_base import FunctionCallbackData as FCD
from src.controller.useful_functions import leave_default
if TYPE_CHECKING:
    from src.model.pictures_bot_manager import PicturesBotManager

def albums_remove(bot_manager: "PicturesBotManager", user_id: int) -> list[Menu]:
    album_id: int = bot_manager.user_data_manager.get(user_id).albums_browse_album_id
    album_name: str = bot_manager.album_data.get_by_id(album_id, "name")[0]
    return [Menu(
        f"Точно удаляем {album_name}?", 
        ButtonRows(
            ButtonRow(Button("Да, удаляем", FCD(albums_remove_perform)))
            ,ButtonRow(Button("Назад", FCD(leave_default)))
        )
    )]

async def albums_remove_perform(bot_manager: "PicturesBotManager", \
        user_id: int, update: Update, **kwargs) -> None:
    user_data = bot_manager.user_data_manager.get(user_id)
    album_id: int = user_data.albums_browse_album_id
    bot_manager.album_data.remove(album_id)
    if user_data.albums_browse_page > 0:
        user_data.albums_browse_page -= 1
    await bot_manager.user_screen_manager.step_back(user_id)