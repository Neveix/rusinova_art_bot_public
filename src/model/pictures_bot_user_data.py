from tg_bot_base import UserData, UserDataManager
from src.model.pictures_bot_manager import PicturesBotManager

class PicturesBotUserData(UserData):
    def __init__(self, user_id: int):
        super().__init__(user_id)
        self.reset_pictures_attributes()
        self.reset_albums_attributes()
    @staticmethod
    def from_user_data(user_data: UserData) -> "PicturesBotUserData":
        result = PicturesBotUserData(user_data.user_id)
        result.after_input = user_data.after_input
        result.callback_data = user_data.callback_data
        result.directory_stack = user_data.directory_stack
        result.media_group_id = user_data.media_group_id
        result.screen = user_data.screen
        return result
    def reset_pictures_attributes(self) -> None:
        self.pictures_browse_page: int = 0
        self.pictures_browse_page_count: int = 0
        self.pictures_browse_filter: str = ""
        self.pictures_browse_picture_id: int = -1
        self.pictures_favorites_mode: bool = False
        self.pictures_shipping_cart_mode: bool = False
        self.pictures_album_mode: bool = False
        self.pictures_add_name: str | None = None
        self.pictures_add_description: str | None = None
        self.pictures_add_price: int | None = None
        self.pictures_edit_mode: bool = False
        self.pictures_buyed_mode: bool = False
        self.pictures_details_page: int = 0
        self.pictures_details_page_count: int = 0
    def reset_albums_attributes(self) -> None:
        self.albums_browse_page: int | None = 0
        self.albums_browse_page_count: int | None = 0
        self.albums_browse_album_id: int | None = -1
        self.albums_add_name: str | None = None
        self.albums_browse_checkout_id: int | None = None
        
        
class PicturesBotUserDataManager(UserDataManager):
    def __init__(self, bot_manager: PicturesBotManager):
        super().__init__(bot_manager)
        self.bot_manager: PicturesBotManager = bot_manager
        self.__users_data: dict[int, PicturesBotUserData] = {}
    def get(self, user_id: int) -> PicturesBotUserData:
        user_data = self.__users_data.get(user_id)
        if user_data is None:
            user_data = PicturesBotUserData(user_id)
            self.set(user_id, user_data)
        return user_data
    def reset(self, user_id: int) -> None:
        self.set(user_id, PicturesBotUserData(user_id))
    def set(self, user_id: int, user_data: PicturesBotUserData):
        self.__users_data[user_id] = user_data
