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


def pictures_edit(bot_manager: "PicturesBotManager", user_id: int) -> list[Menu]:
    from src.controller.pictures.browse import pictures_browse
    user_data = bot_manager.user_data_manager.get(user_id)
    user_data.pictures_shipping_cart_mode = False
    user_data.pictures_favorites_mode = False
    user_data.pictures_album_mode = False
    user_data.pictures_edit_mode = True
    result = pictures_browse(bot_manager=bot_manager, user_id=user_id)
    if 0 == bot_manager.pictures_data.count_final(user_id):
        return result
    result[-1].buttons.rows[0].buttons[0].text = "Изменить подробности"
    result[-1].buttons.rows[0].buttons[0].callback_data = \
        MCD("pictures_details_edit")
    back_button_row = result[-1].buttons.rows.pop()
    result[-1].buttons.rows.pop()
    from src.controller.pictures.admin.buyed import add_picture_to_buyed
    result[-1].buttons.append(
        ButtonRow(Button("Пометить как купленное и скрыть из каталога", 
            FCD(add_picture_to_buyed))))
    result[-1].buttons.append(
        ButtonRow(
            Button(
                "Изменить", MCD("pictures_edit_one")
            ), Button(
                "Удалить", MCD("pictures_remove")
            )
        )
    )
    result[-1].buttons.append(back_button_row)
    return result

