from typing import TYPE_CHECKING
from telegram import Update
from tg_bot_base import EvaluatedScreen, EvaluatedMenuDefault, ButtonRows, ButtonRow, Button
from tg_bot_base import FunctionCallbackData as FCD
from tg_bot_base import StepBackCallbackData as SBCD
if TYPE_CHECKING:
    from src.model.pictures_bot_manager import PicturesBotManager

async def leave_default(bot_manager: "PicturesBotManager", user_id: int, update: Update, **kwargs):
    user_data = bot_manager.user_data_manager.get(user_id)
    user_data.after_input = None
    await bot_manager.user_screen_manager.step_back(user_id)

def is_text_valid(text: str | None) -> bool:
    return isinstance(text, str) and len(text) < 60

async def invalid_input(bot_manager: "PicturesBotManager", user_id: int, msg: str | None = None) -> None:
    text = "Неподходящее введённое значение"
    if msg is not None:
        text += ": " + msg
    new_screen: EvaluatedScreen = EvaluatedScreen(
        EvaluatedMenuDefault(
            text,
            ButtonRows(ButtonRow(Button("Назад", SBCD())))
        )
    )
    await bot_manager.user_screen_manager.set_user_screen(user_id, new_screen)

def generate_simple_screen(text: str) -> EvaluatedScreen:
    return EvaluatedScreen(
        EvaluatedMenuDefault(
            text, ButtonRows(ButtonRow(Button("Назад", FCD(leave_default))))
        )
    )