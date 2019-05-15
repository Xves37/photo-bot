import telebot
import requests
from api_edit import nobg
from pil_edit import blur, gauss_blur, contour
from data import load_data
from config import token

bot = telebot.TeleBot(token)
do_cmd = ''
do_arg = ''
data = load_data('data.json')
cmd_dict, do_list = data['commands'], data['info']['do']


@bot.message_handler(commands=['do'])
def command_change(message):
    global do_cmd, do_arg
    chat = message.chat.id

    msg = message.text.split(' ')
    n = len(msg)
    if n < 2:
        bot.send_message(chat, 'Please, enter a command. To take a list of available commands write: /do list')
        return
    elif msg[1] == 'list':
        str_list = ' '
        for cmd in cmd_dict['do'].keys():
            defin = cmd_dict['do'][cmd]['doc']
            str_list += '/do {cmd} : {defin}\n'.format(cmd=cmd, defin=defin)

        print(str_list)
        bot.send_message(chat, str_list)
    elif msg[1] == 'check':
        if do_cmd:
            bot.send_message(chat, 'Current command: "{0}"'.format(do_cmd))
            if do_arg:
                bot.send_message(chat, 'Current argument: "{0}"'.format(do_arg))
        else:
            bot.send_message(chat, 'Command is not selected!')
    else:
        do_cmd = msg[1]
        do_arg = ''

        bot.send_message(chat, 'Command "{cmd}" if selected.'.format(cmd=do_cmd))

        if cmd_dict['do'][do_cmd]['arg']:
            if n > 2:
                do_arg = msg[2]
                bot.send_message(chat, 'With an argument "{arg}"'.format(arg=do_arg))
            else:
                bot.send_message(chat, 'You can add an argument to this command. Here is a command documentation:'.format(arg=do_arg))
                bot.send_message(chat, cmd_dict['do'][do_cmd]['doc'])


@bot.message_handler(content_types=['document', 'photo'])
def edit(message):
    if do_cmd:
        chat = message.chat.id

        # status
        bot.send_chat_action(chat, 'upload_photo')

        # telegram file downloading
        path = bot.get_file(message.document.file_id).file_path
        url = 'https://api.telegram.org/file/bot{token}/{path}'.format(token=token, path=path)
        response = requests.get(url)

        name = message.document.file_name
        with open('sent/' + name, 'wb') as f:
            f.write(response.content)
            f.close()

        if do_cmd in do_list['api-list']:
            # command handler
            if do_cmd == 'nobg':
                photo = nobg('sent/' + name)

            # save a copy
            name = name[0:message.document.file_name.rfind('.')]
            dest = 'edited/' + name + '-' + do_cmd + '.png'
            with open(dest, 'wb') as f:
                f.write(photo)
                f.close()

        elif do_cmd in do_list['pil-list']:
            src = 'sent/' + name
            if do_cmd == 'blur':
                dest = blur(src)
            elif do_cmd == 'gauss-blur':
                dest = gauss_blur(src)
            elif do_cmd == 'contour':
                dest = contour(src)

        # send file
        bot.send_document(chat, open(dest, 'rb'))

    else:
        bot.send_message(message.chat.id, 'Command is not selected!')


@bot.message_handler(commands=['help'])
def help_msg(message):
    bot.send_message(message.chat.id, str(data['info']['help']))


if __name__ == '__main__':
    print('I have started!')
    bot.polling(none_stop=True)
