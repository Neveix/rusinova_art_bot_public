from typing import TYPE_CHECKING
from tg_bot_base import Menu, ButtonRows, ButtonRow, Button, \
    FunctionCallbackData, SaveablePhotoSize, MenuCallbackData
from telegram import Update, InputMediaPhoto

if TYPE_CHECKING:
    from src.model.pictures_bot_manager import PicturesBotManager

def pictures_browse(bot_manager: "PicturesBotManager", user_id: int) -> list[Menu]:
    user_data = bot_manager.user_data_manager.get(user_id)
    
    browse_result, count_result = bot_manager.pictures_data.browse_and_count_final(
        user_id, "id, name, description, price")
    user_data.pictures_browse_page_count = count_result
    if count_result == 0:
        return [
            Menu("Картин нет",
                ButtonRows(
                    ButtonRow(
                        Button("Назад", FunctionCallbackData(leave))
                    )
                )
            )
        ]
    result: list[Menu] = []
    picture_id, name, description, price = browse_result[0]
    user_data.pictures_browse_picture_id = picture_id
    photo_size_str_list = bot_manager.pictures_data.get_photo_size_list(picture_id)
    user_data.pictures_details_page = 0
    user_data.pictures_details_page_count = len(photo_size_str_list)
    photo_size_str = photo_size_str_list[0]
    result.append(
        Menu(photo = InputMediaPhoto(SaveablePhotoSize.from_string(photo_size_str)))
    )
    page = user_data.pictures_browse_page
    max_page = user_data.pictures_browse_page_count
    menu_text = f"🖼 {name}\n💰 Цена: {price} руб\n{description}\n\
Картинок: {user_data.pictures_details_page_count}\n\nСтраница: {page+1} / {max_page}"
    
    menu_button_rows = ButtonRows()
    menu_button_rows.append(ButtonRow(
        Button(
            "Подробности",
            MenuCallbackData("pictures_details")
        )
    ))
    menu_button_rows.append(ButtonRow(
        Button("◄◄",FunctionCallbackData(first_page)),
        Button("⊲",FunctionCallbackData(previous_page)),
        Button("⊳",FunctionCallbackData(next_page)),
        Button("►►",FunctionCallbackData(last_page))
    ))
    favorites_shipping_cart_button_row = ButtonRow()
    favorites = bot_manager.user_global_data.get_favorite_pictures(user_id)
    if picture_id in favorites:
        favorites_shipping_cart_button_row.append(
            Button("Удалить из избранного", 
                FunctionCallbackData(remove_from_favorites)))
    else:
        favorites_shipping_cart_button_row.append(
            Button("Добавить в избранное", 
                FunctionCallbackData(add_to_favorites)))
    shipping_cart = bot_manager.user_global_data.get_shipping_cart(user_id)
    if picture_id in shipping_cart:
        favorites_shipping_cart_button_row.append(
            Button("Удалить из корзины", 
                FunctionCallbackData(remove_from_shipping_cart)))
    else:
        favorites_shipping_cart_button_row.append(
            Button("Добавить в корзину", 
                FunctionCallbackData(add_to_shipping_cart)))
    menu_button_rows.append(favorites_shipping_cart_button_row)
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
    if user_data.pictures_browse_page > 0:
        user_data.pictures_browse_page = 0
        await bot_manager.user_screen_manager.update_current_screen(user_id)

async def previous_page(bot_manager: "PicturesBotManager", user_id: int, update: Update, **kwargs):
    user_data = bot_manager.user_data_manager.get(user_id)
    if user_data.pictures_browse_page > 0:
        user_data.pictures_browse_page -= 1
        await bot_manager.user_screen_manager.update_current_screen(user_id)

async def next_page(bot_manager: "PicturesBotManager", user_id: int, update: Update, **kwargs):
    user_data = bot_manager.user_data_manager.get(user_id)
    if user_data.pictures_browse_page < user_data.pictures_browse_page_count - 1:
        user_data.pictures_browse_page += 1
        await bot_manager.user_screen_manager.update_current_screen(user_id)

async def last_page(bot_manager: "PicturesBotManager", user_id: int, update: Update, **kwargs):
    user_data = bot_manager.user_data_manager.get(user_id)
    if user_data.pictures_browse_page < user_data.pictures_browse_page_count - 1:
        user_data.pictures_browse_page = user_data.pictures_browse_page_count - 1
        await bot_manager.user_screen_manager.update_current_screen(user_id)

async def add_to_favorites(bot_manager: "PicturesBotManager", user_id: int, update: Update, **kwargs):
    bot_manager.user_global_data.add_to_favorite_pictures(user_id, 
        bot_manager.user_data_manager.get(user_id).pictures_browse_picture_id)
    await bot_manager.user_screen_manager.update_current_screen(user_id)

async def remove_from_favorites(bot_manager: "PicturesBotManager", user_id: int, update: Update, **kwargs):
    user_data = bot_manager.user_data_manager.get(user_id)
    bot_manager.user_global_data.remove_from_favorite_pictures(user_id, 
        bot_manager.user_data_manager.get(user_id).pictures_browse_picture_id)
    if user_data.pictures_favorites_mode and user_data.pictures_browse_page > 0:
        user_data.pictures_browse_page -= 1
    await bot_manager.user_screen_manager.update_current_screen(user_id)

async def add_to_shipping_cart(bot_manager: "PicturesBotManager", user_id: int, update: Update, **kwargs):
    bot_manager.user_global_data.add_to_shipping_cart(user_id, 
        bot_manager.user_data_manager.get(user_id).pictures_browse_picture_id)
    await bot_manager.user_screen_manager.update_current_screen(user_id)

async def remove_from_shipping_cart(bot_manager: "PicturesBotManager", user_id: int, update: Update, **kwargs):
    user_data = bot_manager.user_data_manager.get(user_id)
    bot_manager.user_global_data.remove_from_shipping_cart(user_id, 
        user_data.pictures_browse_picture_id)
    if user_data.pictures_shipping_cart_mode and user_data.pictures_browse_page > 0:
        user_data.pictures_browse_page -= 1
    await bot_manager.user_screen_manager.update_current_screen(user_id)

async def leave(bot_manager: "PicturesBotManager", user_id: int, update: Update, **kwargs):
    bot_manager.user_data_manager.get(user_id).reset_pictures_attributes()
    await bot_manager.user_screen_manager.step_back(user_id)
