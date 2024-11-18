from tg_bot_base import MenuCallbackData as MCD
from tg_bot_base import FunctionCallbackData as FCD
from tg_bot_base import StepBackCallbackData as SBCD
from tg_bot_base import Screen, StaticScreen, Menu, ButtonRows, ButtonRow, Button, DynamicScreen
from src import DynamicMenus

from src.controller.shipping_cart_browse import shipping_cart_browse
from src.controller.pictures.all import pictures_all
from src.controller.pictures.favorites import pictures_favorites
from src.controller.pictures.search import pictures_search
from src.controller.pictures.from_album import pictures_from_album
from src.controller.pictures.browse import pictures_browse
from src.controller.pictures.admin.add import pictures_add_step_1
from src.controller.pictures.admin.edit import pictures_edit
from src.controller.pictures.admin.edit_one import pictures_edit_one
from src.controller.pictures.admin.remove import pictures_remove
from src.controller.albums.browse import albums_browse
from src.controller.albums.admin.add import albums_add_step_1
from src.controller.albums.admin.edit import albums_edit
from src.controller.albums.admin.remove import albums_remove
from src.controller.albums.admin.edit_one import albums_edit_one
from src.controller.albums.admin.edit_album_pictures import edit_album_pictures
from src.controller.pictures.admin.buyed import pictures_buyed
from src.controller.pictures.from_shipping_cart import pictures_from_shipping_cart
from src.controller.pictures.details import pictures_details
from src.controller.pictures.admin.details_edit import pictures_details_edit

def generate_screens() -> list[Screen]:
    return [
        StaticScreen(
            Menu("Добро пожаловать в Rusinova Art Bot! Перейти в начало: /start",
                DynamicMenus.welcome_button_rows 
            ), name = "welcome"
        ),StaticScreen(
            Menu("Тут можно посмотреть картины",
                ButtonRows(
                    ButtonRow(
                        Button("Все картины",MCD("pictures_all")),
                        Button("Поиск",FCD(pictures_search))
                    ),ButtonRow(
                        Button("Из альбома",MCD("albums_browse")),
                    ),ButtonRow(
                        Button("Назад",SBCD())
                    )
                )
            ), name = "pictures"
        ),StaticScreen(
            Menu("При покупке от 2 картин скидка = 20%, от 3 картин и больше = 30%",
                ButtonRows(
                    ButtonRow(
                        Button("Назад",SBCD())
                    )
                )
            ), name = "help"
        ),StaticScreen(
            Menu("Меню Администратора",
                ButtonRows(
                    ButtonRow(
                        Button("Добавить/изменить картины",MCD("pictures_add_or_edit"))
                    ),ButtonRow(
                        Button("Добавить/изменить альбомы",MCD("albums_add_or_edit"))
                    ),ButtonRow(
                        Button("Меню пользователя",MCD("welcome"))
                    )
                )
            ), name = "admin_menu"
        ),
        StaticScreen(
            Menu("Здесь можно добавить или удалить картины",
                ButtonRows(
                    ButtonRow(
                        Button("Добавить новую картину",FCD(pictures_add_step_1))
                    ),ButtonRow(
                        Button("Редактировать картины",MCD("pictures_edit"))
                    ),ButtonRow(
                        Button("Купленные картины",MCD("pictures_buyed"))
                    ),ButtonRow(
                        Button("Назад",SBCD())
                    )
                )
            ), name = "pictures_add_or_edit"
        ),StaticScreen(
            Menu("Здесь можно добавить или удалить альбомы",
                ButtonRows(
                    ButtonRow(
                        Button("Добавить альбом",FCD(albums_add_step_1))
                    ),ButtonRow(
                        Button("Редактировать альбомы",MCD("albums_edit"))
                    ),ButtonRow(
                        Button("Назад",SBCD())
                    )
                )
            ), name = "albums_add_or_edit"
        ),StaticScreen(
            Menu(
                "Платёж успешен, с вами в ближайшее время свяжутся.\n\
По вопросам пишите @n_rusinova\nПерейти в начало - /start"
                ,button_rows = ButtonRows()
            ), name = "payment_succeeded"
        ),DynamicScreen(
            pictures_all, name = "pictures_all"
        ),DynamicScreen(
            pictures_browse, name = "pictures_browse"
        ),DynamicScreen(
            pictures_favorites, name = "pictures_favorites"
        ),DynamicScreen(
            pictures_from_shipping_cart, name = "pictures_shipping_cart"
        ),DynamicScreen(
            shipping_cart_browse, name = "shipping_cart"
        ),DynamicScreen(
            albums_browse, name = "albums_browse"
        ),DynamicScreen(
            pictures_from_album, name = "pictures_from_album"
        ),DynamicScreen(
            pictures_edit, name = "pictures_edit"
        ),DynamicScreen(
            pictures_remove, name = "pictures_remove"
        ),DynamicScreen(
            pictures_edit_one, name = "pictures_edit_one"
        ),DynamicScreen(
            albums_edit, name = "albums_edit"
        ),DynamicScreen(
            albums_remove, name = "album_remove"
        ),DynamicScreen(
            albums_edit_one, name = "album_edit"
        ),DynamicScreen(
            edit_album_pictures, name = "edit_album_pictures"
        ),DynamicScreen(
            pictures_buyed, name = "pictures_buyed"
        ),DynamicScreen(
            pictures_details, name = "pictures_details"
        ),DynamicScreen(
            pictures_details_edit, name = "pictures_details_edit"
        )
    ]