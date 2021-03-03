from telegram.ext import Updater
import logging
from telegram.ext import CommandHandler


def send_to_telebot(final_url, caption):
	updater = Updater(token='<YOUR TELEGRAM UPDATE TOKEN>', use_context=True)
	dispatcher = updater.dispatcher
	updater.start_polling()
	logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)
	updater.dispatcher.bot.sendPhoto(chat_id='<CHAT ID OF THE GROUP WHERE YOU WANT YOUR PICTURES>', photo=final_url, caption=caption)
	updater.stop()
	return
