from typing import TYPE_CHECKING
from telegram import Message, Update
from tg_bot_base import EvaluatedScreen, EvaluatedMenuDefault, ButtonRows, ButtonRow, Button
from tg_bot_base import FunctionCallbackData as FCD
from tg_bot_base import StepBackCallbackData as SBCD
if TYPE_CHECKING:
    from src.model.pictures_bot_manager import PicturesBotManager

async def leave(bot_manager: "PicturesBotManager", user_id: int, update: Update, **kwargs):
    bot_manager.user_data_manager.get(user_id).after_input = None
    await bot_manager.user_screen_manager.step_back(user_id)

async def pictures_search(bot_manager: "PicturesBotManager", user_id: int, update: Update, **kwargs):
    new_screen: EvaluatedScreen = EvaluatedScreen(
        EvaluatedMenuDefault(
            "Введите текст для поиска картин с похожим названием:",
                ButtonRows(ButtonRow(Button("Назад", FCD(leave))))
        )
    )
    await bot_manager.user_screen_manager.set_user_screen(user_id, new_screen)
    await bot_manager.message_manager.get_message_and_run_method(user_id, pictures_search_step_2)

async def pictures_search_step_2(message: Message, bot_manager: "PicturesBotManager", \
    user_id: int, update: Update, **kwargs):
    if message.text is None and len(message.text) < 60:
        new_screen: EvaluatedScreen = EvaluatedScreen(
            EvaluatedMenuDefault(
                "Неподходящий поисковой запрос",
                ButtonRows(ButtonRow(Button("Назад", SBCD())))
            )
        )
        await bot_manager.user_screen_manager.set_user_screen(user_id, new_screen)
        return
    bot_manager.user_data_manager.get(user_id).pictures_browse_filter = message.text
    await bot_manager.user_screen_manager.set_user_screen_by_name(user_id, "pictures_all")