from html_parser_impulce import write_file
import telebot
import csv
from configparser import ConfigParser

TOKEN = ConfigParser().read('settigs.ini')['token']
bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Отправь мне файл сохраненной страницы. У него расширение .html')


@bot.message_handler(content_types=['text'])
def send_task(message):
    task_number = message.text
    with open(f'{message.chat.id}.csv') as file:
        reader = csv.reader(file)
        records = {rows[0]: rows[1] for rows in reader}
    bot.reply_to(message, records[task_number])


@bot.message_handler(content_types=['document'])
def download_file(message):
    try:
        file_info = bot.get_file(message.document.file_id)
        bot.reply_to(message, ('Напиши номер задания.\n'
                               'Если задание из первого блока, то напиши просто его номер.\n'
                               'Если из второго то в формате 2.1 или 2.14'))
        downloaded_file = bot.download_file(file_info.file_path)

        with open(f'html_doc.html', 'wb') as file:
            file.write(downloaded_file)

        write_file(message.chat.id)

    except Exception as e:
        bot.reply_to(message, e)


bot.polling()





# while True:
#     api_response = requests.get(f'{base_url}getUpdates').json()
#
#     for update in api_response:
#         chat_id = update['chat_id']
#         message = update['message']['text']
#         reply_message = {
#             'chat_id': chat_id,
#             'text': message,
#         }
#         requests.post(f'{base_url}sendMessge', json=reply_message)
