from tg_bot_base import ButtonRows, ButtonRow, Button, \
    MenuCallbackData
from src.model.pictures_bot_manager import PicturesBotManager

class DynamicMenus:
    @staticmethod
    def welcome_button_rows(bot_manager: PicturesBotManager, user_id: int, **kwargs):
        result = ButtonRows(
            ButtonRow(
                Button("Просмотр картин",MenuCallbackData("pictures")),
                Button("Избранные",MenuCallbackData("pictures_favorites"))
            ),ButtonRow(
                Button("Корзина",MenuCallbackData("shipping_cart")),
                Button("Помощь",MenuCallbackData("help"))
            )
        )
        from src.config.access import ADMIN_LIST
        if user_id in ADMIN_LIST:
            result.append(
                ButtonRow(
                    Button("Меню Администратора", MenuCallbackData("admin_menu"))
                )
            )
        return result