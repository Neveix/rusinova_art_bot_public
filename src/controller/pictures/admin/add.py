from typing import TYPE_CHECKING
from telegram import Message, Update
from tg_bot_base import ButtonRow, Button
from tg_bot_base import FunctionCallbackData as FCD
from src.controller.useful_functions import is_text_valid, invalid_input, generate_simple_screen
if TYPE_CHECKING:
    from src.model.pictures_bot_manager import PicturesBotManager
    



async def pictures_add_step_1(bot_manager: "PicturesBotManager", user_id: int, \
        update: Update, **kwargs):
    await bot_manager.user_screen_manager.set_user_screen(user_id, 
        generate_simple_screen("Введите название новой картины:"))
    await bot_manager.message_manager.get_message_and_run_method(user_id, pictures_add_step_2)

async def pictures_add_step_2(message: Message, bot_manager: "PicturesBotManager", \
        user_id: int, update: Update, **kwargs):
    if not is_text_valid(message.text):
        await invalid_input(bot_manager, user_id)
        return
    bot_manager.user_data_manager.get(user_id).pictures_add_name = message.text
    await bot_manager.user_screen_manager.set_user_screen(user_id, 
        generate_simple_screen("Введите описание новой картины:"))
    await bot_manager.message_manager.get_message_and_run_method(user_id, pictures_add_step_3)
    
async def pictures_add_step_3(message: Message, bot_manager: "PicturesBotManager", \
        user_id: int, update: Update, **kwargs):
    if not is_text_valid(message.text):
        await invalid_input(bot_manager, user_id)
        return
    bot_manager.user_data_manager.get(user_id).pictures_add_description = message.text
    await bot_manager.user_screen_manager.set_user_screen(user_id, 
        generate_simple_screen("Введите цену новой картины:"))
    await bot_manager.message_manager.get_message_and_run_method(user_id, pictures_add_step_4)
    
async def pictures_add_step_4(message: Message, bot_manager: "PicturesBotManager", \
        user_id: int, update: Update, **kwargs):
    if message.text is None or not is_text_valid(message.text):
        await invalid_input(bot_manager, user_id)
        return
    try:
        text: str = message.text
        price = int(text)
    except ValueError:
        await invalid_input(bot_manager, user_id, msg = \
"Невозможно преобразовать введённое значение в число. \
Попробуйте написать его в виде 12500 (без дробей, пробелов)")
        return
    bot_manager.user_data_manager.get(user_id).pictures_add_price = price
    await bot_manager.user_screen_manager.set_user_screen(user_id, 
        generate_simple_screen("Отправьте изображение новой картины:"))
    await bot_manager.message_manager.get_message_and_run_method(user_id, pictures_add_step_5)
    
async def pictures_add_step_5(message: Message, bot_manager: "PicturesBotManager", \
        user_id: int, update: Update, **kwargs):
    if message.photo is None:
        await invalid_input(bot_manager, user_id, "Вы не отправили фото")
        return
    user_data = bot_manager.user_data_manager.get(user_id)
    name = user_data.pictures_add_name
    desc = user_data.pictures_add_description
    price = user_data.pictures_add_price
    from tg_bot_base import SaveablePhotoSize
    photo_size = SaveablePhotoSize.from_photo_size(message.photo[0])
    photo_size_str = photo_size.to_string()
    bot_manager.pictures_data.add(name, desc, price, [photo_size_str])
    new_screen = generate_simple_screen("Картина успешно добавлена")
    new_screen.menus[0].button_rows.rows.insert(0,
        ButtonRow(
            Button(
                "Просмотреть картину",
                FCD(pictures_checkout)
            )
        ))
    await bot_manager.user_screen_manager.set_user_screen(user_id, 
        new_screen)

async def pictures_checkout(bot_manager: "PicturesBotManager", user_id: int, update: Update, **kwargs):
    user_data = bot_manager.user_data_manager.get(user_id)
    bot_manager.user_data_manager.get(user_id).pictures_browse_filter = user_data.pictures_add_name
    await bot_manager.user_screen_manager.set_user_screen_by_name(user_id, "pictures_all")