from typing import TYPE_CHECKING
#from telegram import Message, Update, InputMediaPhoto
from tg_bot_base import ButtonRow, Button, Menu
#, ButtonRows
#from tg_bot_base import FunctionCallbackData as FCD
from tg_bot_base import MenuCallbackData as MCD
#from tg_bot_base import StepBackCallbackData as SBCD
#from src.controller.useful_functions import generate_simple_screen, is_text_valid, invalid_input
if TYPE_CHECKING:
    from src.model.pictures_bot_manager import PicturesBotManager


def albums_edit(bot_manager: "PicturesBotManager", user_id: int) -> list[Menu]:
    from src.controller.albums.browse import albums_browse
    user_data = bot_manager.user_data_manager.get(user_id)
    user_data.directory_stack.pop()
    user_data.directory_stack.append('albums_edit')
    result = albums_browse(bot_manager=bot_manager, user_id=user_id)
    result_count = bot_manager.album_data.count_final(user_id)
    if 0 == result_count:
        return result
    result[1].buttons.rows.insert(-1, 
        ButtonRow(
            Button("Изменить", MCD("album_edit")),
            Button("Удалить", MCD("album_remove"))
        )
    )
    return result