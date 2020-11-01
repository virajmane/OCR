import cloudmersive_ocr_api_client
import os
from telegram import ParseMode
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler


def start(update, context):
    file_id = update.message.photo[-1].file_id
    newFile = context.bot.get_file(file_id)
    newFile.download("test.jpg")
    update.message.reply_text("Got Image")
    filename = "test.jpg"
    configuration = cloudmersive_ocr_api_client.Configuration()
    api = os.environ.get("API_KEY")
    configuration.api_key['Apikey'] = api
    api_instance = cloudmersive_ocr_api_client.ImageOcrApi(cloudmersive_ocr_api_client.ApiClient(configuration))
    api_response = api_instance.image_ocr_photo_to_text(filename)
    result = api_response.text_result+"\n"
    url = "https://www.google.com/search?q="+api_response.text_result
    update.message.reply_text(f'{result}<a href="{url}">Click here</a>', parse_mode=ParseMode.HTML)

def help(update, context):
    update.message.reply_text('Send an image')

def main():
    token = os.environ.get("TOKEN")
    updater = Updater(token, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(MessageHandler(Filters.photo, start))
    dp.add_handler(CommandHandler("help", help))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()