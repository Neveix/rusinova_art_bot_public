from src import PicturesBotManager

def init_bot() -> PicturesBotManager:
    from src import PicturesData
    from src import CommandsCollection
    result = PicturesBotManager()
    from os import mkdir
    try:
        mkdir("db")
    except FileExistsError:
        pass
    pictures_data = PicturesData("./db/pictures_data.db")
    result.set_pictures_data(pictures_data)
    pictures_data.create_tables()
    
    result.set_commands_collection(CommandsCollection(result))
    
    from src import UserGlobalData
    global_data = UserGlobalData("./db/user_global_data.db")
    result.set_user_global_data(global_data)
    global_data.create_tables()
    
    from src.model.log_manager import logger
    result.set_logger(logger)
    
    from src.model.album_data import AlbumData
    album_data = AlbumData("./db/album_data.db")
    album_data.set_bot_manager(result)
    album_data.create_tables()
    result.set_album_data(album_data)
    
    from src.model.purchasing_manager import PurchasingManager
    result.set_purchasing_manager(PurchasingManager(result))
    
    from src.model.purchased_data import PurchasedData
    purchased_data = PurchasedData("./db/purchased_data.db")
    purchased_data.create_tables()
    result.set_purchased_data(purchased_data)
    
    from src.model.mail_manager import MailManager
    from src.config.access import SENDER_EMAIL, SENDER_PASSWORD
    result.set_mail_manager(
        MailManager(SENDER_EMAIL, SENDER_PASSWORD))
    
    from src.view.generate_screens import generate_screens
    result.screen_manager.extend_screen(*generate_screens())
    
    from tg_bot_base import Command
    result.command_manager.add(Command("start", result.commands_collection.cmd_start))
    return result

bot_manager = init_bot()