from typing import TYPE_CHECKING
from telegram import Message
from tg_bot_base import Menu, ButtonRows, ButtonRow, Button, FunctionCallbackData, \
    EvaluatedScreen, EvaluatedMenuDefault
from src.controller.useful_functions import generate_simple_screen, invalid_input, leave_default
if TYPE_CHECKING:
    from src.model.pictures_bot_manager import PicturesBotManager

def pictures_details_edit(bot_manager: "PicturesBotManager", user_id: int) -> list[Menu]:
    from src.controller.pictures.details import pictures_details
    user_data = bot_manager.user_data_manager.get(user_id)
    user_data.directory_stack.pop()
    user_data.directory_stack.append('pictures_details_edit')
    result = pictures_details(bot_manager=bot_manager, user_id=user_id)
    move_button_row = ButtonRow(
        Button("Сдвинуть назад", FunctionCallbackData(move_back)),
        Button("Сдвинуть вперёд", FunctionCallbackData(move_forth))
    )
    remove_edit_button_row = ButtonRow(
        Button("Добавить", FunctionCallbackData(add_photo)),
        Button("Изменить", FunctionCallbackData(change_photo)),
        Button("Удалить", FunctionCallbackData(remove))
    )
    back_button_row = result[-1].buttons.rows[-1]
    result[-1].buttons.rows[1:] = [
        move_button_row,
        remove_edit_button_row,
        back_button_row
    ]
    return result

async def move_back(bot_manager: "PicturesBotManager", user_id: int, **kwargs):
    user_data = bot_manager.user_data_manager.get(user_id)
    picture_id = user_data.pictures_browse_picture_id
    from src.controller.pictures.details import previous_page
    if user_data.pictures_details_page > 0:
        photo_size_str_list = bot_manager.pictures_data.get_photo_size_list(picture_id)
        index = user_data.pictures_details_page
        l = photo_size_str_list
        l[index-1], l[index] = l[index], l[index-1]
        bot_manager.pictures_data.set_photo_size_list(picture_id, photo_size_str_list)
        await previous_page(bot_manager = bot_manager, user_id = user_id, **kwargs)

async def move_forth(bot_manager: "PicturesBotManager", user_id: int, **kwargs):
    user_data = bot_manager.user_data_manager.get(user_id)
    picture_id = user_data.pictures_browse_picture_id
    from src.controller.pictures.details import next_page
    if user_data.pictures_details_page < user_data.pictures_details_page_count-1:
        photo_size_str_list = bot_manager.pictures_data.get_photo_size_list(picture_id)
        index = user_data.pictures_details_page
        l = photo_size_str_list
        l[index+1], l[index] = l[index], l[index+1]
        bot_manager.pictures_data.set_photo_size_list(picture_id, photo_size_str_list)
        await next_page(bot_manager = bot_manager, user_id = user_id, **kwargs)

async def change_photo(bot_manager: "PicturesBotManager", user_id: int, **kwargs):
    screen = generate_simple_screen("Отправьте новую картинку:")
    bot_manager.user_data_manager.get(user_id).directory_stack.append("pictures_details_change_photo")
    await bot_manager.user_screen_manager.set_user_screen(user_id, screen)
    await bot_manager.message_manager.get_message_and_run_method(
        user_id, change_photo_step_2
    )

async def change_photo_step_2(message: Message, bot_manager: "PicturesBotManager", \
    user_id: int, **kwargs):
    if message.photo is None:
        invalid_input(bot_manager, user_id)
        return
    from tg_bot_base import SaveablePhotoSize
    photo_size = SaveablePhotoSize.from_photo_size(message.photo[0])
    photo_size_str = photo_size.to_string()
    user_data = bot_manager.user_data_manager.get(user_id)
    picture_id = user_data.pictures_browse_picture_id
    details_page = user_data.pictures_details_page
    photo_size_list = bot_manager.pictures_data.get_photo_size_list(picture_id)
    photo_size_list[details_page] = photo_size_str
    bot_manager.pictures_data.set_photo_size_list(picture_id, photo_size_list)
    screen = generate_simple_screen("Картинка успешно изменена")
    await bot_manager.user_screen_manager.set_user_screen(user_id, screen)

async def remove(bot_manager: "PicturesBotManager", user_id: int, **kwargs):
    user_data = bot_manager.user_data_manager.get(user_id)
    bot_manager.user_data_manager.get(user_id).directory_stack.append("pictures_details_remove_photo")
    if user_data.pictures_details_page_count == 1:
        screen = generate_simple_screen("Нельзя удалить единственную картинку")
        await bot_manager.user_screen_manager.set_user_screen(user_id, screen)
        return
    screen = EvaluatedScreen(
        EvaluatedMenuDefault(
            "Точно удаляем?",
            ButtonRows(
                ButtonRow(
                    Button(
                        "Да", FunctionCallbackData(remove_step_2)
                    ),Button(
                        "Назад", FunctionCallbackData(leave_default)
                    )
                )
            )
        )
    )
    await bot_manager.user_screen_manager.set_user_screen(user_id, screen)

async def remove_step_2(bot_manager: "PicturesBotManager", user_id: int, **kwargs):
    user_data = bot_manager.user_data_manager.get(user_id)
    picture_id = user_data.pictures_browse_picture_id
    photo_size_list = bot_manager.pictures_data.get_photo_size_list(picture_id)
    photo_size_list.pop(user_data.pictures_details_page)
    bot_manager.pictures_data.set_photo_size_list(picture_id, photo_size_list)
    screen = generate_simple_screen("Картинка успешно удалена")
    await bot_manager.user_screen_manager.set_user_screen(user_id, screen)

async def add_photo(bot_manager: "PicturesBotManager", user_id: int, **kwargs):
    screen = generate_simple_screen("Отправьте новую картинку:")
    bot_manager.user_data_manager.get(user_id).directory_stack.append("pictures_details_add_photo")
    await bot_manager.user_screen_manager.set_user_screen(user_id, screen)
    await bot_manager.message_manager.get_message_and_run_method(
        user_id, add_photo_step_2
    )

async def add_photo_step_2(message: Message, bot_manager: "PicturesBotManager", \
    user_id: int, **kwargs):
    if message.photo is None:
        invalid_input(bot_manager, user_id)
        return
    from tg_bot_base import SaveablePhotoSize
    photo_size = SaveablePhotoSize.from_photo_size(message.photo[0])
    photo_size_str = photo_size.to_string()
    user_data = bot_manager.user_data_manager.get(user_id)
    picture_id = user_data.pictures_browse_picture_id
    details_page = user_data.pictures_details_page
    photo_size_list = bot_manager.pictures_data.get_photo_size_list(picture_id)
    photo_size_list.insert(details_page, photo_size_str)
    bot_manager.pictures_data.set_photo_size_list(picture_id, photo_size_list)
    screen = generate_simple_screen("Картинка успешно добавлена")
    await bot_manager.user_screen_manager.set_user_screen(user_id, screen)