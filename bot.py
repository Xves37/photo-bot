import telebot
import requests
from api_edit import nobg
from pil_edit import blur, gauss_blur, contour, sharpen, smooth, rotate
from data import load_data
from config import token

bot = telebot.TeleBot(token)
do_cmd = ''
do_arg = ''
data = load_data('data.json')
cmd_dict, do_list = data['commands'], data['info']['do']


def send(chat_id, msg):
    bot.send_message(chat_id, msg)


@bot.message_handler(commands=['do'])
def command_change(message):
    global do_cmd, do_arg
    chat = message.chat.id

    msg = message.text.split(' ')
    n = len(msg)

    # /do without any command
    if n < 2:
        send(chat, 'Please, enter a command. To take a list of available commands write: /do list')
        return

    # sys commands (list, check)
    elif msg[1] == 'list':
        str_list = ' '
        for cmd in cmd_dict['do'].keys():
            defin = cmd_dict['do'][cmd]['doc']
            str_list += '/do {cmd} : {defin}\n'.format(cmd=cmd, defin=defin)

        send(chat, str_list)
    elif msg[1] == 'check':
        if do_cmd:
            send(chat, 'Current command: "{0}"'.format(do_cmd))
            if do_arg:
                send(chat, 'Current argument: "{0}"'.format(do_arg))
        else:
            send(chat, 'Command was not selected!')

    # save a command
    elif msg[1] in do_list['all']:
        do_cmd = msg[1]
        do_arg = ''

        send(chat, 'Command "{cmd}" was selected.'.format(cmd=do_cmd))

        # save an argument
        if n > 2 and cmd_dict['do'][do_cmd]['arg']:
            do_arg = msg[2]
            send(chat, 'With an argument "{arg}"'.format(arg=do_arg))
        elif n < 3 and cmd_dict['do'][do_cmd]['arg']:
            send(chat, 'You can add an argument to this command. /'
                       'Here is a command documentation:\n{doc}'.format(doc=cmd_dict['do'][do_cmd]['doc']))

    # command not found
    else:
        send(chat, 'Command "{cmd}" was not found'.format(cmd=msg[1]))


@bot.message_handler(content_types=['document', 'photo'])
def edit(message):
    chat = message.chat.id
    dest = 'src/error.jpg'

    if do_cmd:

        # status
        bot.send_chat_action(chat, 'upload_photo')

        # document or photo validation
        if message.content_type == 'document':
            path = bot.get_file(message.document.file_id).file_path
            name = message.document.file_name
        else:
            file_id = bot.get_file(message.photo[-1].file_id)
            path = file_id.file_path
            name = file_id.file_id + '.jpg'

        # telegram file downloading
        url = 'https://api.telegram.org/file/bot{token}/{path}'.format(token=token, path=path)
        response = requests.get(url)

        # saving file that was sent
        with open('sent/' + name, 'wb') as f:
            f.write(response.content)
            f.close()

        # api commands handler
        if do_cmd in do_list['api-list']:
            if do_cmd == 'nobg':
                dest = nobg('sent/' + name)

        # pil commands handler
        elif do_cmd in do_list['pil-list']:
            src = 'sent/' + name
            if do_cmd == 'blur':
                dest = blur(src)
            elif do_cmd == 'gauss-blur':
                dest = gauss_blur(src, do_arg)
            elif do_cmd == 'contour':
                dest = contour(src)
            elif do_cmd == 'smooth':
                dest = smooth(src)
            elif do_cmd == 'sharpen':
                dest = sharpen(src)
            elif do_cmd == 'rotate':
                dest = rotate(src, do_arg)

        # send file to user
        bot.send_document(chat, open(dest, 'rb'))

    else:
        send(chat, 'Command is not selected!')


@bot.message_handler(commands=['help'])
def help_msg(message):
    send(message.chat.id, str(data['info']['help']))


if __name__ == '__main__':
    print('I have started!')
    bot.polling(none_stop=True)
