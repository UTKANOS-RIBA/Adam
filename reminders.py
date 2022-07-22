import json
from telegram.ext import ConversationHandler
import datetime as dt

from system_p import data


def add_reminder(update, context):
    update.message.reply_text('Please enter data in the following format: \n <reminder text> \n '
                               '<day dd.mm.yyyy> \n <time hh:mm> (default 10:00)')
    return 1


def check(update):
    text = update.message.text.split('\n')
    if len(text[0]) == 0:
        update.message.reply_text('Need to add text')
        return False
    if len(text) > 3 or len(text) < 2:
        update.message.reply_text('The data was entered in the wrong format, please try again')
        return False
    if '.' not in text[1]:
        update.message.reply_text('The data was entered in the wrong format, please try again')
        return False
    try:
        date = text[1].split('.')
    except Exception:
        update.message.reply_text('The data was entered in the wrong format, please try again')
        return False
    if len(text) == 3:
        if ':' not in text[2]:
            update.message.reply_text('The data was entered in the wrong format, please try again')
            return False
        try:
            time = text[2].split(':')
        except Exception:
            update.message.reply_text('The data was entered in the wrong format, please try again')
            return False
    else:
        time = ['10', '00']
    year = int(date[2])
    month = int(date[1])
    day = int(date[0])
    hour = int(time[0])
    minute = int(time[1])
    checker = True
    if 1 <= month <= 12 and day >= 1:
        if month in [1, 3, 5, 7, 8, 10, 12]:
            if day > 31:
                checker = False
        elif month == 2:
            if year % 4 == 0:
                if day > 29:
                    checker = False
            else:
                if day > 28:
                    checker = False
        else:
            if day > 30:
                checker = False
    else:
        checker = False
    if not (0 <= hour <= 23 and 0 <= minute <= 59):
        checker = False
    if not checker:
        update.message.reply_text('The data was entered in the wrong format, please try again')
        return False
    req_time = dt.datetime(year, month, day, hour, minute)
    if req_time <= dt.datetime.utcnow() + dt.timedelta(0, int(data[str(update.message.chat.id)]['utc_offset'])):
        update.message.reply_text('I still can\'t go back in time')
        return False
    return [text[0], [day, month, year], [hour, minute]]


def add_reminder_part_2(update, context):
    text = check(update)
    if text:
        data[str(update.message.chat.id)]['reminders'].append({'text': text[0], 'date': text[1], 'time': text[2]})
        with open('data.json', 'w') as archive:
            json.dump(data, archive)
            archive.close()
        update.message.reply_text('Excellent! I will remind you of this')
    return ConversationHandler.END


def show_reminders(update, context):
    us_id = str(update.message.chat.id)
    us_data = data[us_id]['reminders']
    res = ''
    if len(us_data) == 0:
        update.message.reply_text('You don\'t have active reminders)')
    else:
        for i in range(len(us_data)):
            res += f'*** {i + 1} ***\n'
            month = str(us_data[i]['date'][1])
            day = str(us_data[i]['date'][0])
            year = str(us_data[i]['date'][2])
            minute = str(us_data[i]['time'][1])
            hour = str(us_data[i]['time'][0])
            if len(month) == 1:
                month = '0' + month
            if len(day) == 1:
                day = '0' + day
            if len(minute) == 1:
                minute = '0' + minute
            date = f'{day}.{month}.{year};  {hour}:{minute}'
            res += date + '\n' + us_data[i]['text'] + '\n'
        update.message.reply_text(f'{update.message.chat.first_name}, here are all your reminders:\n')
        update.message.reply_text(res)


def delete_reminder(update, context):
    show_reminders(update, context)
    if len(data[str(update.message.chat.id)]['reminders']) != 0:
        update.message.reply_text('Write the number of the reminder you want to delete')
        return 1


def delete_reminder_part_2(update, context):
    try:
        number_to_delete = int(update.message.text)
    except Exception:
        update.message.reply_text('Invalid input format, please try again')
        return ConversationHandler.END
    us_data = data[str(update.message.chat.id)]['reminders']
    if number_to_delete <= len(us_data):
        temp = []
        for i in range(len(us_data)):
            if i + 1 != number_to_delete:
                temp.append(us_data[i])
        data[str(update.message.chat.id)]['reminders'] = temp
        update.message.reply_text('Excellent! Reminder deleted successfully')
        with open('data.json', 'w') as archive:
            json.dump(data, archive)
            archive.close()
        if len(data[str(update.message.chat.id)]['reminders']) > 0:
            show_reminders(update, context)
        else:
            update.message.reply_text('Now you have no reminders')
    else:
        update.message.reply_text('You don\'t have that kind of reminder')
    return ConversationHandler.END