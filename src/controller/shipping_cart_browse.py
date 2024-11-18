from typing import TYPE_CHECKING
from tg_bot_base import Menu, ButtonRows, ButtonRow, Button, \
    FunctionCallbackData, MenuCallbackData
if TYPE_CHECKING:
    from src.model.pictures_bot_manager import PicturesBotManager

def shipping_cart_browse(bot_manager: "PicturesBotManager", user_id: int) -> list[Menu]:
    shipping_cart = bot_manager.user_global_data.get_shipping_cart(user_id)
    from .pictures.browse import leave
    if len(shipping_cart) == 0:
        return [
            Menu("Ваша корзина пуста",
                ButtonRows(
                    ButtonRow(
                        Button("Назад", FunctionCallbackData(leave))
                    )
                )
            )
        ]
    result: list[Menu] = []
    text = "В вашей корзине лежат: "
    check = bot_manager.purchasing_manager.generate_check(user_id)
    # text += f"\n<code>Чек\n{check}</code>" 
    text += f"\n{check}"
    from telegram.constants import ParseMode
    from src.controller.shipping_cart_purchase import shipping_cart_purchase
    result.append(
        Menu(
            text,
            ButtonRows(
                ButtonRow(
                    Button("Оформить заказ", FunctionCallbackData(shipping_cart_purchase))
                ),ButtonRow(
                        Button("Просмотреть картины из корзины", MenuCallbackData("pictures_shipping_cart"))
                ),ButtonRow(
                    Button("Назад", FunctionCallbackData(leave))
                )
            ),
            parse_mode=ParseMode.HTML
        )
    )
    return result