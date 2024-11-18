from typing import TYPE_CHECKING
from logging import Logger
from tg_bot_base import BotManager
from src.model.album_data import AlbumData
if TYPE_CHECKING:
    from src import PicturesData, CommandsCollection, UserGlobalData
    from src.model.purchasing_manager import PurchasingManager
    from src.model.purchased_data import PurchasedData
    from src.model.mail_manager import MailManager

class PicturesBotManager(BotManager):
    def __init__(self):
        super().__init__()
        self.pictures_data = None
        self.commands_collection = None
        self.logger = None
        from .pictures_bot_user_data import PicturesBotUserDataManager
        self.user_data_manager = PicturesBotUserDataManager(self)
        self.user_global_data = None
        self.album_data: AlbumData = None
        from .purchasing_manager import PurchasingManager
        self.purchasing_manager: PurchasingManager = None
        from .purchased_data import PurchasedData
        self.purchased_data: PurchasedData = None
        from src.model.mail_manager import MailManager
        self.mail_manager: MailManager = None
    def set_pictures_data(self, pictures_data: "PicturesData"):
        self.pictures_data = pictures_data
        pictures_data.set_bot_manager(self)
    def set_commands_collection(self, commands_collection: "CommandsCollection"):
        self.commands_collection = commands_collection
    def set_logger(self, logger: Logger):
        self.logger = logger
    def set_user_global_data(self, user_global_data: "UserGlobalData"):
        self.user_global_data = user_global_data
        user_global_data.set_bot_manager(self)
    def set_album_data(self, album_data: AlbumData):
        self.album_data = album_data
    def set_purchasing_manager(self, purchasing_manager: "PurchasingManager"):
        self.purchasing_manager = purchasing_manager
    def set_purchased_data(self, purchased_data: "PurchasedData"):
        self.purchased_data = purchased_data
    def set_mail_manager(self, mail_manager: "MailManager"):
        self.mail_manager = mail_manager