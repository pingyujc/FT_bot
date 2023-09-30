import telegram
from telegram.ext import Updater, CommandHandler


# Replace 'YOUR_BOT_TOKEN' with the token you received from BotFather
bot_token = '6427108276:AAEVgX6Cl4iFmwtSpgktXaucP-uFbR5QIJs'

# Create a bot instance
bot = telegram.Bot(token=bot_token)

# Send a message to a specific chat ID
def send_message(update, context):
    chat_id = update.message.chat_id
    message = "Hello from your bot!"
    bot.send_message(chat_id=chat_id, text=message)

# Create an updater
updater = Updater(token=bot_token, use_context=True)

# Get the dispatcher to register handlers
dispatcher = updater.dispatcher

# Register a command handler for the /start command
start_handler = CommandHandler('start', send_message)
dispatcher.add_handler(start_handler)

# Start the bot
updater.start_polling()
updater.idle()
