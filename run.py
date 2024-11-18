
from telegram.ext import Application

from yookassa import Configuration

from src.config.access import TELEGRAM_BOT_TOKEN, YOOKASSA_SHOP_ID, YOOKASSA_SECRET_KEY

from src.init_bot import bot_manager

Configuration.account_id = YOOKASSA_SHOP_ID
Configuration.secret_key = YOOKASSA_SECRET_KEY

def main():
    from src.model.log_manager import init_logging, log_message_handler, log_button_handler
    init_logging()
    bot_manager.message_manager.handle_message = log_message_handler(bot_manager.message_manager.handle_message)
    bot_manager.callback_query_manager.callback_query_handler = log_button_handler(
        bot_manager.callback_query_manager.callback_query_handler, 
        bot_manager)
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    bot_manager.set_bot(application.bot)
    job_queue = application.job_queue
    from src.model.job_payments_check import job_payments_check
    job_queue.run_repeating(job_payments_check, interval=5, first=1)
    
    # Commands
    application.add_handlers(bot_manager.command_manager.get_all_handlers())

    # CallbackQuery
    application.add_handler(bot_manager.callback_query_manager.get_handler())
    
    # Messages
    application.add_handler(bot_manager.message_manager.get_handler())
    
    
    print("Поллинг...")
    
    application.run_polling(poll_interval=0.1)

if __name__ == "__main__":
    main()    
