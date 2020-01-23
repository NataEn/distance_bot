import logging
import bot_settings
import telegram
from distance import get_distance_from_hifa, geocode, haversine

from telegram import Update, InlineKeyboardButton
from telegram.ext import CommandHandler, CallbackContext, MessageHandler, Filters, Updater, InlineQueryHandler, \
    CallbackQueryHandler

logging.basicConfig(
    format='[%(levelname)s %(asctime)s %(module)s:%(lineno)d] %(message)s',
    level=logging.INFO)

logger = logging.getLogger(__name__)
updater = Updater(token=bot_settings.BOT_TOKEN, use_context=True)
dispatcher = updater.dispatcher


def start(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    context.user_data['place'] = 'jerusalem'
    context.user_data['point_a'] = 'hifa'
    logger.info(f"> Start chat #{chat_id}")
    location_keyboard = telegram.KeyboardButton(text="send_location", request_location=True)
    contact_keyboard = telegram.KeyboardButton(text="send_contact", request_contact=True)
    custom_keyboard = [[location_keyboard, contact_keyboard]]
    reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)
    context.bot.send_message(chat_id=chat_id,
                             text="Would you mind sharing your location and contact with me?",
                             reply_markup=reply_markup)


def respond(update: Update, context: CallbackContext):
    print('message_id', update.message.text)
    logger.info(f'in handeler{update.message.text}')
    if update.message.text == None:
        lat = update.message.location.latitude
        lon = update.message.location.longitude
        address1 = (lon, lat)
        address2 = geocode(context.user_data['point_a'])
        distance = haversine(*address1, *address2)
        print("location", lon, lat)
        response = f'your distance from Hifa is:{distance}'
    elif len(update.message.text) > 0:
        context.user_data['place'] = update.message.text
    response = get_distance_from_hifa(context.user_data['place'])
    chat_id = update.effective_chat.id
    logger.info(f"= Got on chat #{chat_id}: {context.user_data['place']!r}")
    logger.info(f"= Got on chat #{chat_id}: {update.message}")
    context.bot.send_message(chat_id=update.message.chat_id, text=response)


def button(update, context):
    logger.info('in inline button')
    query = update.callback_query
    query.edit_message_text(text="Selected option: {}".format(query.data))


dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(MessageHandler(Filters.text, respond))
# updater.dispatcher.add_handler(CallbackQueryHandler(button))
# dispatcher.add_handler(InlineQueryHandler(callback=button,update_queue=False,job_queue=False))
dispatcher.add_handler(MessageHandler(Filters.location, respond))

logger.info("* Start polling...")
updater.start_polling()  # Starts polling in a background thread.
updater.idle()  # Wait until Ctrl+C is pressed
logger.info("* Bye!")
