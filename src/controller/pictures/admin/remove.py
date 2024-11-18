from typing import TYPE_CHECKING
from telegram import Update
from tg_bot_base import ButtonRows, ButtonRow, Button, Menu
from tg_bot_base import FunctionCallbackData as FCD
from src.controller.useful_functions import leave_default
if TYPE_CHECKING:
    from src.model.pictures_bot_manager import PicturesBotManager

def pictures_remove(bot_manager: "PicturesBotManager", user_id: int) -> list[Menu]:
    picture_id: int = bot_manager.user_data_manager.get(user_id).pictures_browse_picture_id
    picture_name: str = bot_manager.pictures_data.get_by_id(picture_id, "name")[0]
    return [Menu(
        f"Точно удаляем {picture_name}?", 
        ButtonRows(
                ButtonRow(Button(f"Да, точно удаляем {picture_name}", FCD(pictures_remove_perform)))
            ,ButtonRow(Button("Назад", FCD(leave_default)))
        )
    )]

async def pictures_remove_perform(bot_manager: "PicturesBotManager", \
        user_id: int, update: Update, **kwargs) -> None:
    user_data = bot_manager.user_data_manager.get(user_id)
    picture_id: int = user_data.pictures_browse_picture_id
    bot_manager.pictures_data.delete(picture_id)
    page = user_data.pictures_browse_page
    if page > 0:
        user_data.pictures_browse_page = page - 1
    await bot_manager.user_screen_manager.step_back(user_id)