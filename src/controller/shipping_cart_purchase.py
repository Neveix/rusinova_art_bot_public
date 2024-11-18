from typing import TYPE_CHECKING
from tg_bot_base import ButtonRows, EvaluatedScreen, EvaluatedMenuDefault
if TYPE_CHECKING:
    from src.model.pictures_bot_manager import PicturesBotManager

async def shipping_cart_purchase(bot_manager: "PicturesBotManager", user_id: int, 
        **kwargs) -> None:
    link = await bot_manager.purchasing_manager.create_payment_and_get_link(user_id)
    text = f"""Вы можете оплатить свой заказ <a href="{link}">по этой ссылке</a>\n""" \
        +r"Вернуться в начало - /start"
    from telegram.constants import ParseMode
    old_screen = bot_manager.user_screen_manager.get_user_screen(user_id)
    text = old_screen.menus[-1].text + "\n" + text
    print(f"{text=}")
    screen = \
    EvaluatedScreen(
        EvaluatedMenuDefault(
            text, button_rows=ButtonRows(),
            parse_mode = ParseMode.HTML
        )
    )
    await bot_manager.user_screen_manager.set_user_screen(
        user_id, screen
    )