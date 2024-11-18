from typing import TYPE_CHECKING
from telegram import Message, Update, InputMediaPhoto
from tg_bot_base import ButtonRow, Button, Menu, ButtonRows
from tg_bot_base import FunctionCallbackData as FCD
from tg_bot_base import MenuCallbackData as MCD
from tg_bot_base import StepBackCallbackData as SBCD
from src.controller.useful_functions import generate_simple_screen, is_text_valid, invalid_input
if TYPE_CHECKING:
    from src.model.pictures_bot_manager import PicturesBotManager

def albums_edit_one(bot_manager: "PicturesBotManager", user_id: int) -> list[Menu]:
    user_data = bot_manager.user_data_manager.get(user_id)
    album_id = user_data.albums_browse_album_id
    album_name: str = bot_manager.album_data.get_by_id(
        album_id, "name")[0]
    result = []
    album_photo_size_str = bot_manager.album_data.get_by_id(album_id, "photo_size")[0]
    from tg_bot_base import SaveablePhotoSize
    result.append(
        Menu(photo = InputMediaPhoto(SaveablePhotoSize.from_string(album_photo_size_str)))
    )
    result.append(
        Menu(
            f"Изменение альбома:\n{album_name}"
            , ButtonRows(
                ButtonRow(
                    Button(
                        "Изменить название", FCD(change_name)
                    ),Button(
                        "Изменить картинку", FCD(change_photo)
                    )
                ),ButtonRow(
                    Button(
                        "Добавить/Удалить картины из альбома", MCD("edit_album_pictures")
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
    bot_manager.user_data_manager.get(user_id).directory_stack.append("album_change_name")
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
    album_id = user_data.albums_browse_album_id
    bot_manager.album_data.set_name(album_id, message.text)
    screen = generate_simple_screen("Имя успешно изменено")
    await bot_manager.user_screen_manager.set_user_screen(user_id, screen)

async def change_photo(bot_manager: "PicturesBotManager", user_id: int, update: Update, **kwargs):
    screen = generate_simple_screen("Отправьте новую картинку:")
    bot_manager.user_data_manager.get(user_id).directory_stack.append("album_change_photo")
    await bot_manager.user_screen_manager.set_user_screen(user_id, screen)
    await bot_manager.message_manager.get_message_and_run_method(
        user_id, change_photo_step_2
    )

async def change_photo_step_2(message: Message, bot_manager: "PicturesBotManager", \
    user_id: int, update: Update, **kwargs):
    if message.photo is None:
        invalid_input(bot_manager, user_id)
        return
    from tg_bot_base import SaveablePhotoSize
    photo_size = SaveablePhotoSize.from_photo_size(message.photo[0])
    photo_size_str = photo_size.to_string()
    user_data = bot_manager.user_data_manager.get(user_id)
    album_id = user_data.albums_browse_album_id
    bot_manager.album_data.set_photo(album_id, photo_size_str)
    screen = generate_simple_screen("Картинка успешно изменена")
    await bot_manager.user_screen_manager.set_user_screen(user_id, screen)