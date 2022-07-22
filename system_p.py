import json
import os
from telegram import ReplyKeyboardMarkup
from telegram.ext import ConversationHandler
import datetime as dt


reply_keyboard = [['/add_note', '/show_notes', '/delete_note'],
                  ['/add_reminder', '/show_reminders', '/delete_reminder'],
                  ['/start', '/help', '/stop', '/change_tz']]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)

data = {}
if os.path.exists('data.json'):
    with open('data.json') as archive:
        data = json.load(archive)
        archive.close()


def start(update, context):
    if str(update.message.chat.id) not in data:
        data[str(update.message.chat.id)] = {'name': update.message.chat.first_name, 'utc_offset': '',
                                             'notes': {}, 'reminders': []}
    update.message.reply_text(f'Hello, {update.message.chat.first_name}! I\'ll glad to help you!')
    update.message.reply_text('To see all the commands use /help', reply_markup=markup)
    if data[str(update.message.chat.id)]['utc_offset'] == '':
        change_tz(update, context)
        return 1
    else:
        return ConversationHandler.END


def stop(update, context):
    return ConversationHandler.END


def help(update, context):
    update.message.reply_text('Here are all the commands:\n/start - start a dialogue with Adam\n/help - display this message\n'
                               '/stop - stop running the current task\nNotes:\n/add_note - add'
                               ' new note\n/show_notes - show a message with your notes\n'
                               '/delete_note - delete unwanted note\nReminders:\n'
                               '/add_reminder - add a reminder\n/show_reminders - display active reminders\n'
                               '/delete_reminder - delete reminder\n/change_tz - change time zone')


def change_tz(update, context):
    update.message.reply_text('For all my functions to work correctly,'
                               'I need to determine your time zone')
    update.message.reply_text('Please enter your current time with the format\n<dd.mm.yyyy hh:mm>')
    return 1


def change_tz_part_2(update, context):
    try:
        us_time = dt.datetime.strptime(update.message.text, '%d.%m.%Y %H:%M')
    except Exception:
        update.message.reply_text('The data was entered in the wrong format, please try again')
        change_tz(update, context)
        return 1
    utc_time = dt.datetime.utcnow()
    utc_offset = us_time - utc_time
    if abs(utc_offset.total_seconds()) > 12 * 3600:
        update.message.reply_text('This timezone does not exist, please try again')
        change_tz(update, context)
        return 1
    else:
        data[str(update.message.chat.id)]['utc_offset'] = utc_offset.total_seconds()
        with open('data.json', 'w') as archive:
            json.dump(data, archive)
            archive.close()
        update.message.reply_text('Good job! I determined your time zone)')
        return ConversationHandler.END


def check_reminders(context):
    for key, value in data.items():
        user_id = key
        user_data = data[user_id]['reminders']
        for elem in user_data:
            req_time = dt.datetime(elem['date'][2], elem['date'][1], elem['date'][0], elem['time'][0], elem['time'][1])
            if req_time <= dt.datetime.utcnow() + dt.timedelta(0, int(data[user_id]['utc_offset'])):
                req_text = 'Attention! Reminder:\n' + elem['text']
                context.bot.send_message(user_id, text=req_text)
                temp = []
                for el in user_data:
                    if el != elem:
                        temp.append(el)
                data[user_id]['reminders'] = temp
                with open('data.json', 'w') as archive:
                    json.dump(data, archive)
                    archive.close()