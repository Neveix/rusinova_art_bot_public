from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src import PicturesBotManager

class PurchasingManager:
    def __init__(self, bot_manager: "PicturesBotManager"):
        self.bot_manager = bot_manager
        self.payment_return_url = "https://t.me/rusinovaart_bot"
    def generate_check(self, user_id: int, shipping_cart: list[int] | None = None) -> str:
        """if shipping_cart is not present, function will substitute it with \
normal get_shipping_cart method of user_global_data"""
        if shipping_cart is None:
            shipping_cart = self.bot_manager.user_global_data.get_shipping_cart(user_id)
        check_items: list[tuple[str,str]] = []
        for picture_i, picture_id in enumerate(shipping_cart):
            name, price = self.bot_manager.pictures_data.get_by_id(picture_id, "name, price")
            check_items.append((f"{picture_i+1}) {name}", f"{price} руб"))
        check_items.append(("",""))
        total_price_without_discount = self.get_total_price_without_discount(user_id)
        check_items.append(("Итого без скидки",f"{total_price_without_discount} руб"))
        discount = self.get_discount(user_id)
        check_items.append(("Скидка",f"{round(discount*100)}%"))
        total_price_with_discount = self.get_total_price_with_discount(user_id)
        check_items.append(("Итого со скидкой",f"{total_price_with_discount} руб"))
        text = ""
        first = True
        for item in check_items:
            item_name, item_value = item
            if not first:
                text += "\n"
            first = False
            text += f"{item_name} {item_value}"
        return text
    def get_discount(self, user_id: int) -> float:
        discount = 0
        shipping_cart = self.bot_manager.user_global_data.get_shipping_cart(user_id)
        len_shipping_cart = len(shipping_cart)
        if len_shipping_cart == 2:
            discount = 0.2
        elif len_shipping_cart >= 3:
            discount = 0.3
        return discount
    def get_total_price_without_discount(self, user_id: int) -> int:
        total_price = 0
        shipping_cart = self.bot_manager.user_global_data.get_shipping_cart(user_id)
        for picture_id in shipping_cart:
            price = self.bot_manager.pictures_data.get_by_id(picture_id, "price")[0]
            total_price += price
        return total_price
    def get_total_price_with_discount(self, user_id: int) -> int:
        total_price_without_discount = self.get_total_price_without_discount(user_id)
        discount = self.get_discount(user_id)
        total_price_with_discount = round(total_price_without_discount * (1 - discount))
        return total_price_with_discount
    async def create_payment_and_get_link(self, user_id: int) -> str:
        shipping_cart = self.bot_manager.user_global_data.get_shipping_cart(user_id)
        from yookassa import Payment
        from uuid import uuid4
        idempotence_key = str(uuid4())
        value = self.get_total_price_with_discount(user_id)
        payment_dict = {
            "amount": {
                "value": value,
                "currency": "RUB"
            },
            "confirmation": {
                "type": "redirect",
                "return_url": self.payment_return_url
            },
            "capture": True,
            "description": f"Оплата картин на {value} рублей"
        }
        payment = Payment.create(payment_dict, idempotence_key)
        from time import time
        when_time = int(time())
        self.bot_manager.purchased_data.add_purchased(
            payment_id = payment.id,
            user_id = user_id,
            when_time = when_time
        )
        self.bot_manager.user_global_data.set_paying_shipping_cart(user_id,
            shipping_cart)
        return payment.confirmation["confirmation_url"]
    