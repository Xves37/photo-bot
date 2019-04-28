import config
import requests
import telebot

bot = telebot.TeleBot(config.token)


@bot.message_handler(content_types=['document'])
def no_bg(message):
    """Remove background from documents"""

    # telegram file downloading
    path = bot.get_file(message.document.file_id).file_path
    url = 'https://api.telegram.org/file/bot{token}/{path}'.format(token=config.token, path=path)
    response = requests.get(url)

    # no-bg api post request
    response = requests.post(
        'https://api.remove.bg/v1.0/removebg',
        files={'image_file': response.content},
        data={'size': 'auto'},
        headers={'X-Api-Key': config.bg_key},
    )

    # with open('src/test-no-bg.png', 'wb') as f:
    #     f.write(response.content)

    # send file
    bot.send_document(message.chat.id, response.content)


if __name__ == '__main__':
    bot.polling(none_stop=True)
