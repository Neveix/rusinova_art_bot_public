from typing import TYPE_CHECKING
#from telegram import Message, Update, InputMediaPhoto
from tg_bot_base import ButtonRow, Button, Menu
#    , ButtonRows
from tg_bot_base import FunctionCallbackData as FCD
from tg_bot_base import MenuCallbackData as MCD
#from tg_bot_base import StepBackCallbackData as SBCD
#from src.controller.useful_functions import generate_simple_screen, is_text_valid, invalid_input
if TYPE_CHECKING:
    from src.model.pictures_bot_manager import PicturesBotManager


def pictures_buyed(bot_manager: "PicturesBotManager", user_id: int) -> list[Menu]:
    from src.controller.pictures.browse import pictures_browse
    user_data = bot_manager.user_data_manager.get(user_id)
    user_data.pictures_buyed_mode = True
    result = pictures_browse(bot_manager=bot_manager, user_id=user_id)
    if 0 == bot_manager.pictures_data.count_final(user_id):
        return result
    if len(result[-1].buttons.rows) > 1:
        target_button_row: ButtonRow = result[-1].buttons.rows[-2]
        target_button_row.buttons.clear()
        target_button_row.extend(
            Button("Вернуть из 'Купленных'", FCD(remove_picture_from_buyed)), 
            Button(
                "Удалить", MCD("pictures_remove")
            )
        )
    return result

async def remove_picture_from_buyed(bot_manager: "PicturesBotManager", user_id: int, **kwargs) -> None:
    user_data = bot_manager.user_data_manager.get(user_id)
    picture_id = user_data.pictures_browse_picture_id
    bot_manager.pictures_data.set_buyed(picture_id, False)
    if user_data.pictures_browse_page > 0:
        user_data.pictures_browse_page -= 1
    await bot_manager.user_screen_manager.update_current_screen(user_id)

async def add_picture_to_buyed(bot_manager: "PicturesBotManager", user_id: int, **kwargs) -> None:
    user_data = bot_manager.user_data_manager.get(user_id)
    picture_id = user_data.pictures_browse_picture_id
    bot_manager.pictures_data.set_buyed(picture_id, True)
    if user_data.pictures_browse_page > 0:
        user_data.pictures_browse_page -= 1
    await bot_manager.user_screen_manager.update_current_screen(user_id)