from typing import TYPE_CHECKING
from tg_bot_base import ButtonRow, Button, Menu
from tg_bot_base import FunctionCallbackData as FCD
if TYPE_CHECKING:
    from src.model.pictures_bot_manager import PicturesBotManager


def edit_album_pictures(bot_manager: "PicturesBotManager", user_id: int) -> list[Menu]:
    from src.controller.pictures.browse import pictures_browse
    user_data = bot_manager.user_data_manager.get(user_id)
    result = pictures_browse(bot_manager=bot_manager, user_id=user_id)
    if 0 == bot_manager.pictures_data.count_final(user_id):
        return result
    target_button_row: ButtonRow = result[-1].buttons.rows[-2]
    picture_id = user_data.pictures_browse_picture_id
    album_id = user_data.albums_browse_album_id
    album_pictures = bot_manager.album_data.get_pictures(album_id)
    if picture_id in album_pictures:
        text = "Удалить из альбома"
        callback_data = FCD(remove_from_album)
    else:
        text = "Добавить в альбом"
        callback_data = FCD(add_to_album)
    target_button_row.buttons.clear()
    target_button_row.extend(
        Button(text, callback_data)
    )
    return result

async def add_to_album(bot_manager: "PicturesBotManager", user_id: int, **kwargs):
    user_data = bot_manager.user_data_manager.get(user_id)
    picture_id = user_data.pictures_browse_picture_id
    album_id = user_data.albums_browse_album_id
    bot_manager.album_data.add_picture(album_id, picture_id)
    await bot_manager.user_screen_manager.update_current_screen(user_id)

async def remove_from_album(bot_manager: "PicturesBotManager", user_id: int, **kwargs):
    user_data = bot_manager.user_data_manager.get(user_id)
    picture_id = user_data.pictures_browse_picture_id
    album_id = user_data.albums_browse_album_id
    bot_manager.album_data.remove_picture(album_id, picture_id)
    await bot_manager.user_screen_manager.update_current_screen(user_id)
