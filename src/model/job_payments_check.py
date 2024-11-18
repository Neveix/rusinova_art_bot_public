
from telegram.ext import ContextTypes

async def job_payments_check(context: ContextTypes.DEFAULT_TYPE):
    from src.init_bot import bot_manager
    get_result = bot_manager.purchased_data.get_purchased("payment_id, user_id",
        "WHERE payed = 0 ORDER BY when_time ASC")
    #if get_result != []:
    #    bot_manager.logger.info(f"""job_payments_check {get_result=}""")
    from yookassa import Payment
    from time import localtime, asctime
    for payment_id, user_id in get_result:
        payment = Payment.find_one(payment_id)
        match payment.status:
            case "canceled":
                bot_manager.purchased_data.delete_by_payment_id(payment_id)
                continue
            case "succeeded":
                pass
            case _:
                continue
        if not payment.paid:
            bot_manager.logger.info(f"""платёж {payment_id} оказался успешным но не оплачен!""")
            continue
        # Только в случае, если этот платёж был оплачен:
        # Полное имя пользователя
        user_max_name = bot_manager.user_global_data.get_max_name(user_id)
        # Короткое имя пользователя
        user_name = bot_manager.user_global_data.get_user_advanced_data(user_id, "first_name")[0]
        msg: str = f"{asctime(localtime())}: {user_max_name} оплатил заказ:\n\
{payment_id=}\n\n"
        # будующие строчки о конкретных купленных картинах в платеже
        pic_notes: list[str] = []
        # Корзина пользователя, замороженная на момент начала покупки
        paying_sc: list[int] = bot_manager.user_global_data.get_paying_shipping_cart(user_id)
        # Итого, скидка
        total_without_discount = bot_manager.purchasing_manager.get_total_price_without_discount(user_id)
        discount = round(bot_manager.purchasing_manager.get_discount(user_id) * 100)
        total_with_discount = bot_manager.purchasing_manager.get_total_price_with_discount(user_id)
        for picture_id in paying_sc:
            # Все картины в ней приобретают статус "купленных"
            bot_manager.pictures_data.set_buyed(picture_id, True)
            pic_name, pic_price = bot_manager.pictures_data.get_by_id(picture_id, "name, price")
            # Администратор получит информацию о покупке этой картины
            # соответствующим пользователем в определённое время
            pic_notes.append(
f"{pic_name} за {pic_price} рублей ")
            # Удаляем картину из всех корзин, если она в них была
            bot_manager.user_global_data.remove_from_all_shipping_carts(picture_id)
        # Этот платёж помечается как оплаченный и теперь будет 
        # игнорироваться этой функцией
        bot_manager.purchased_data.set_payed(payment_id, True)
        pic_count = len(pic_notes)
        if pic_count == 0:
            continue
        pic_notes.append(f"Итого без скидки: {total_without_discount} рублей")
        pic_notes.append(f"Скидка: {discount}%")
        pic_notes.append(f"Итого со скидкой: {total_with_discount} рублей")
        # отправляем письмо на почту о проведённой оплате 
        caption: str = f"Покупка картин ({pic_count} шт.) от {user_name}"
        msg += ";\n".join(pic_notes)
        from src.config.access import RECEIVER_EMAIL
        bot_manager.mail_manager.send_default(
            RECEIVER_EMAIL, caption, msg)
        # Пользователю отправляется уведомление об успешной покупке
        bot_manager.user_screen_manager.clear_user_screen(user_id)
        await bot_manager.user_screen_manager.set_user_screen_by_name(user_id, "payment_succeeded")