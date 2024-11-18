from typing import TYPE_CHECKING
from telegram import Message, Update, InputMediaPhoto
from tg_bot_base import ButtonRow, Button, Menu, ButtonRows
from tg_bot_base import FunctionCallbackData as FCD
# from tg_bot_base import MenuCallbackData as MCD
from tg_bot_base import StepBackCallbackData as SBCD
from src.controller.useful_functions import generate_simple_screen, is_text_valid, invalid_input
if TYPE_CHECKING:
    from src.model.pictures_bot_manager import PicturesBotManager

def pictures_edit_one(bot_manager: "PicturesBotManager", user_id: int) -> list[Menu]:
    user_data = bot_manager.user_data_manager.get(user_id)
    picture_id = user_data.pictures_browse_picture_id
    picture_name, picture_description, picture_price = bot_manager.pictures_data.get_by_id(
        picture_id, "name, description, price")
    result = []
    photo_size_str = bot_manager.pictures_data.get_photo_size_list(picture_id)[0]
    from tg_bot_base import SaveablePhotoSize
    result.append(
        Menu(photo = InputMediaPhoto(SaveablePhotoSize.from_string(photo_size_str)))
    )
    result.append(
        Menu(
            f"Изменение картины:\n{picture_name}\n\n{picture_description}\n\nЦена: {picture_price}"
            , ButtonRows(
                ButtonRow(
                    Button(
                        "Изменить название", FCD(change_name)
                    ),Button(
                        "Изменить описание", FCD(change_description)
                    )
                ),ButtonRow(
                    Button(
                        "Изменить цену", FCD(change_price)
                    )
                ),ButtonRow(
                    Button(
                        "Назад", SBCD()
                    )
                )
            )
        )
    )
    return result

async def change_name(bot_manager: "PicturesBotManager", user_id: int, update: Update, **kwargs):
    screen = generate_simple_screen("Введите новое название:")
    bot_manager.user_data_manager.get(user_id).directory_stack.append("pictures_change_name")
    await bot_manager.user_screen_manager.set_user_screen(user_id, screen)
    await bot_manager.message_manager.get_message_and_run_method(
        user_id, change_name_step_2
    )

async def change_name_step_2(message: Message, bot_manager: "PicturesBotManager", \
    user_id: int, update: Update, **kwargs):
    if not is_text_valid(message.text):
        await invalid_input(bot_manager, user_id)
        return
    user_data = bot_manager.user_data_manager.get(user_id)
    picture_id = user_data.pictures_browse_picture_id
    bot_manager.pictures_data.set_name(picture_id, message.text)
    screen = generate_simple_screen("Имя успешно изменено")
    await bot_manager.user_screen_manager.set_user_screen(user_id, screen)
    
async def change_description(bot_manager: "PicturesBotManager", user_id: int, update: Update, **kwargs):
    screen = generate_simple_screen("Введите новое описание:")
    bot_manager.user_data_manager.get(user_id).directory_stack.append("pictures_change_description")
    await bot_manager.user_screen_manager.set_user_screen(user_id, screen)
    await bot_manager.message_manager.get_message_and_run_method(
        user_id, change_description_step_2
    )

async def change_description_step_2(message: Message, bot_manager: "PicturesBotManager", \
    user_id: int, update: Update, **kwargs):
    if not is_text_valid(message.text):
        await invalid_input(bot_manager, user_id)
        return
    user_data = bot_manager.user_data_manager.get(user_id)
    picture_id = user_data.pictures_browse_picture_id
    bot_manager.pictures_data.set_description(picture_id, message.text)
    screen = generate_simple_screen("Описание успешно изменено")
    await bot_manager.user_screen_manager.set_user_screen(user_id, screen)
    
async def change_price(bot_manager: "PicturesBotManager", user_id: int, update: Update, **kwargs):
    screen = generate_simple_screen("Введите новую цену:")
    bot_manager.user_data_manager.get(user_id).directory_stack.append("pictures_change_price")
    await bot_manager.user_screen_manager.set_user_screen(user_id, screen)
    await bot_manager.message_manager.get_message_and_run_method(
        user_id, change_price_step_2
    )

async def change_price_step_2(message: Message, bot_manager: "PicturesBotManager", \
    user_id: int, update: Update, **kwargs):
    if message.text is None or not is_text_valid(message.text):
        await invalid_input(bot_manager, user_id)
        return
    try:
        price = int(message.text)
    except ValueError:
        await invalid_input(bot_manager, user_id, "Невозможно преобразовать в число")
        return
    user_data = bot_manager.user_data_manager.get(user_id)
    picture_id = user_data.pictures_browse_picture_id
    bot_manager.pictures_data.set_price(picture_id, price)
    screen = generate_simple_screen("Цена успешно изменена")
    await bot_manager.user_screen_manager.set_user_screen(user_id, screen)

