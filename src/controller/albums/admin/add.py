from typing import TYPE_CHECKING
from telegram import Message, Update
from tg_bot_base import ButtonRow, Button
from tg_bot_base import FunctionCallbackData as FCD
from src.controller.useful_functions import is_text_valid, invalid_input, generate_simple_screen
if TYPE_CHECKING:
    from src.model.pictures_bot_manager import PicturesBotManager
    
async def albums_add_step_1(bot_manager: "PicturesBotManager", user_id: int, \
        update: Update, **kwargs):
    screen = generate_simple_screen("Введите название нового альбома:")
    await bot_manager.user_screen_manager.set_user_screen(user_id, screen)
    await bot_manager.message_manager.get_message_and_run_method(user_id, albums_add_step_2)

async def albums_add_step_2(message: Message, bot_manager: "PicturesBotManager", \
        user_id: int, update: Update, **kwargs):
    if not is_text_valid(message.text):
        await invalid_input(bot_manager, user_id)
        return
    bot_manager.user_data_manager.get(user_id).albums_add_name = message.text
    await bot_manager.user_screen_manager.set_user_screen(user_id, 
        generate_simple_screen("Отправьте картинку для нового альбома:"))
    await bot_manager.message_manager.get_message_and_run_method(user_id, albums_add_step_3)
    
    
async def albums_add_step_3(message: Message, bot_manager: "PicturesBotManager", \
        user_id: int, update: Update, **kwargs):
    if message.photo is None:
        await invalid_input(bot_manager, user_id, "Вы не отправили фото")
        return
    user_data = bot_manager.user_data_manager.get(user_id)
    name = user_data.albums_add_name
    from tg_bot_base import SaveablePhotoSize
    photo_size = SaveablePhotoSize.from_photo_size(message.photo[0])
    photo_size_str = photo_size.to_string()
    bot_manager.album_data.add(name, photo_size_str)
    new_screen = generate_simple_screen("Альбом успешно добавлен")
    new_screen.menus[0].button_rows.rows.insert(0,
        ButtonRow(
            Button(
                "Просмотреть альбом",
                FCD(album_checkout)
            )
        ))
    await bot_manager.user_screen_manager.set_user_screen(user_id, 
        new_screen)

async def album_checkout(bot_manager: "PicturesBotManager", user_id: int, update: Update, **kwargs):
    user_data = bot_manager.user_data_manager.get(user_id)
    album_count = bot_manager.album_data.count_albums()
    user_data.albums_browse_checkout_id = \
        bot_manager.album_data.browse(album_count - 1, "id")[0][0]
    await bot_manager.user_screen_manager.set_user_screen_by_name(user_id, "albums_edit")