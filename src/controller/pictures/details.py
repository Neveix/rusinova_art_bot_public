from typing import TYPE_CHECKING
from telegram import InputMediaPhoto, Update
from tg_bot_base import Menu, SaveablePhotoSize, ButtonRows, ButtonRow, Button,\
    FunctionCallbackData, StepBackCallbackData
if TYPE_CHECKING:
    from src.model.pictures_bot_manager import PicturesBotManager

def pictures_details(bot_manager: "PicturesBotManager", user_id: int) -> list[Menu]:
    user_data = bot_manager.user_data_manager.get(user_id)
    result: list[Menu] = []
    picture_id = user_data.pictures_browse_picture_id
    details_page: int = user_data.pictures_details_page
    photo_size_str_list: list[str] = bot_manager.pictures_data.get_photo_size_list(picture_id)
    details_page_count = len(photo_size_str_list)
    user_data.pictures_details_page_count = details_page_count
    photo_size_str: str = photo_size_str_list[details_page]
    photo: InputMediaPhoto = InputMediaPhoto(
        SaveablePhotoSize.from_string(photo_size_str)
    )
    result.append(Menu(photo = photo))
    button_rows = ButtonRows(
        ButtonRow(
            Button("◄◄",FunctionCallbackData(first_page)),
            Button("⊲",FunctionCallbackData(previous_page)),
            Button("⊳",FunctionCallbackData(next_page)),
            Button("►►",FunctionCallbackData(last_page))
        ),ButtonRow(
            Button("Назад",StepBackCallbackData())
        )
    )
    result.append(
        Menu(
            text = f"Другие изображения этой картины\n\nКартинка {details_page + 1} / {details_page_count}",
            button_rows = button_rows
        )
    )
    return result

async def first_page(bot_manager: "PicturesBotManager", user_id: int, update: Update, **kwargs):
    user_data = bot_manager.user_data_manager.get(user_id)
    if user_data.pictures_details_page > 0:
        user_data.pictures_details_page = 0
        await bot_manager.user_screen_manager.update_current_screen(user_id)

async def previous_page(bot_manager: "PicturesBotManager", user_id: int, update: Update, **kwargs):
    user_data = bot_manager.user_data_manager.get(user_id)
    if user_data.pictures_details_page > 0:
        user_data.pictures_details_page -= 1
        await bot_manager.user_screen_manager.update_current_screen(user_id)

async def next_page(bot_manager: "PicturesBotManager", user_id: int, update: Update, **kwargs):
    user_data = bot_manager.user_data_manager.get(user_id)
    if user_data.pictures_details_page < user_data.pictures_details_page_count - 1:
        user_data.pictures_details_page += 1
        await bot_manager.user_screen_manager.update_current_screen(user_id)

async def last_page(bot_manager: "PicturesBotManager", user_id: int, update: Update, **kwargs):
    user_data = bot_manager.user_data_manager.get(user_id)
    if user_data.pictures_details_page < user_data.pictures_details_page_count - 1:
        user_data.pictures_details_page = user_data.pictures_details_page_count - 1
        await bot_manager.user_screen_manager.update_current_screen(user_id)