from typing import TYPE_CHECKING
from telegram import Update

if TYPE_CHECKING:
    from src import PicturesBotManager
class CommandsCollection:
    def __init__(self, bot_manager: "PicturesBotManager"):
        self.bot_manager: PicturesBotManager = bot_manager
        async def cmd_start(update : Update, _):
            user = update.message.from_user
            user_id = user.id
            bot_manager.user_global_data.set_user_advanced_data(user.id,\
                user.first_name, user.last_name, user.username)
            bot_manager.logger.info(f"{user_id} написал /start")
            screen_name = "welcome"
            bot_manager.user_data_manager.reset(user_id)
            await bot_manager.user_screen_manager.set_user_screen_by_name(user_id, screen_name)
        self.cmd_start = cmd_start