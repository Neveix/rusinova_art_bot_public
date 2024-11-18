import os
import logging
import time
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .pictures_bot_manager import PicturesBotManager

logger = logging.getLogger(__name__)

def init_logging():
    logger.setLevel(logging.INFO)
    try:
        os.mkdir("logs")
    except FileExistsError:
        pass
    current_time = time.localtime()
    readable_time = time.strftime("%Y-%m-%d %H:%M:%S", current_time)
    handler = logging.FileHandler(f"logs/{readable_time}.log", mode='w')
    formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)

def log_message_handler(func):
    from telegram import Update
    from telegram.ext import CallbackContext
    def wrapper(update: Update, context: CallbackContext):
        user_id = update.message.from_user.id
        message = update.message.text
        logger.info(f"{user_id} написал сообщение {message}")
        return func(update,context)
    return wrapper

def log_button_handler(func, bot_manager: "PicturesBotManager"):
    from telegram import Update
    from telegram.ext import CallbackContext
    from .pictures_bot_manager import PicturesBotManager
    bm: PicturesBotManager = bot_manager
    def wrapper(update: Update, context: CallbackContext):
        user_id = update.callback_query.from_user.id
        data = int(update.callback_query.data)
        user_data = bm.user_data_manager.get(user_id)
        callback_data = user_data.callback_data
        if callback_data is None:
            logger.warning(f"{user_id} нажал на кнопку, {callback_data=}")
        else:
            if len(callback_data) <= data:
                logger.warning(f"{user_id} нажал на неизвестную кнопку, {callback_data=}")
            else:
                from tg_bot_base import CallbackData
                button_data: CallbackData = callback_data[data]
                if button_data.action == "button":
                    logger.info(f"{user_id} нажал на кнопку и перешёл в {button_data.args[0]}")
                elif button_data.action == "step_back":
                    logger.info(f"{user_id} нажал на кнопку и перешёл назад")
                elif button_data.action == "function":
                    function = button_data.args[0]
                    args = button_data.args[1:]
                    logger.info(f"{user_id} нажал на кнопку с функцией {function.__qualname__ \
                        } {args} {button_data.kwargs}")
                else:
                    logger.info(f"{user_id} нажал на кнопку {button_data.action} {button_data.args \
                        } {button_data.kwargs}")
        result = func(update,context)
        return result
    return wrapper