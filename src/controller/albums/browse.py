from typing import TYPE_CHECKING
from tg_bot_base import Menu, ButtonRows, ButtonRow, Button, \
    FunctionCallbackData, SaveablePhotoSize, MenuCallbackData
from telegram import Update, InputMediaPhoto

if TYPE_CHECKING:
    from src.model.pictures_bot_manager import PicturesBotManager

def albums_browse(bot_manager: "PicturesBotManager", user_id: int) -> list[Menu]:
    user_data = bot_manager.user_data_manager.get(user_id)
    browse_result, count_result = bot_manager.album_data.browse_and_count_final(
        user_id, "id, name, photo_size")
    user_data.albums_browse_page_count = count_result
    if count_result == 0:
        return [
            Menu("Альбомов нет",
                ButtonRows(
                    ButtonRow(
                        Button("Назад", FunctionCallbackData(leave))
                    )
                )
            )
        ]
    result: list[Menu] = []
    album_id, name, photo_size_str = browse_result[0]
    user_data.albums_browse_album_id = album_id
    result.append(
        Menu(photo = InputMediaPhoto(SaveablePhotoSize.from_string(photo_size_str)))
    )
    page = user_data.albums_browse_page
    max_page = user_data.albums_browse_page_count
    menu_text = f"🖼 {name}"
    if user_data.albums_browse_checkout_id is None:
        menu_text += f"\n\nСтраница: {page+1} / {max_page}"
    menu_button_rows = ButtonRows(
        ButtonRow(
            Button("◄◄",FunctionCallbackData(first_page)),
            Button("⊲",FunctionCallbackData(previous_page)),
            Button("⊳",FunctionCallbackData(next_page)),
            Button("►►",FunctionCallbackData(last_page))
        )
    )
    menu_button_rows.append(
        ButtonRow(
            Button("Открыть", MenuCallbackData('pictures_from_album'))
        )
    )
    menu_button_rows.append(
        ButtonRow(
            Button("Назад", FunctionCallbackData(leave))
        )
    )
    result.append(Menu(
        text = menu_text,
        button_rows = menu_button_rows
    ))
    return result

async def first_page(bot_manager: "PicturesBotManager", user_id: int, update: Update, **kwargs):
    user_data = bot_manager.user_data_manager.get(user_id)
    if user_data.albums_browse_page > 0:
        user_data.albums_browse_page = 0
        await bot_manager.user_screen_manager.update_current_screen(user_id)

async def previous_page(bot_manager: "PicturesBotManager", user_id: int, update: Update, **kwargs):
    user_data = bot_manager.user_data_manager.get(user_id)
    if user_data.albums_browse_page > 0:
        user_data.albums_browse_page -= 1
        await bot_manager.user_screen_manager.update_current_screen(user_id)
        
async def next_page(bot_manager: "PicturesBotManager", user_id: int, update: Update, **kwargs):
    user_data = bot_manager.user_data_manager.get(user_id)
    if user_data.albums_browse_page < user_data.albums_browse_page_count - 1:
        user_data.albums_browse_page += 1
        await bot_manager.user_screen_manager.update_current_screen(user_id)

async def last_page(bot_manager: "PicturesBotManager", user_id: int, update: Update, **kwargs):
    user_data = bot_manager.user_data_manager.get(user_id)
    if user_data.albums_browse_page < user_data.albums_browse_page_count - 1:
        user_data.albums_browse_page = user_data.albums_browse_page_count - 1
        await bot_manager.user_screen_manager.update_current_screen(user_id)

async def leave(bot_manager: "PicturesBotManager", user_id: int, update: Update, **kwargs):
    bot_manager.user_data_manager.get(user_id).reset_albums_attributes()
    await bot_manager.user_screen_manager.step_back(user_id)
