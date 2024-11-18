from typing import TYPE_CHECKING
from tg_bot_base import Menu
if TYPE_CHECKING:
    from src.model.pictures_bot_manager import PicturesBotManager

def pictures_from_album(bot_manager: "PicturesBotManager", user_id: int) -> list[Menu]:
    from src.controller.pictures.browse import pictures_browse
    user_data = bot_manager.user_data_manager.get(user_id)
    user_data.pictures_album_mode = True
    user_data.directory_stack.pop()
    user_data.directory_stack.append('pictures_browse')
    return pictures_browse(bot_manager=bot_manager, user_id=user_id)