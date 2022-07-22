import json
from telegram.ext import ConversationHandler
from system_p import data


def add_note(update, context):
    update.message.reply_text('Enter the text of the note you want to save')
    return 'note'


def save_note(update, context):
    user_id = str(update.message.chat.id)
    data[user_id]['notes'][str(len(data[user_id]['notes']) + 1)] = update.message.text
    with open('data.json', 'w') as archive:
        json.dump(data, archive)
        archive.close()
    update.message.reply_text('Excellent! I wrote it down')
    return ConversationHandler.END


def show_notes(update, context):
    res = ''
    us_data = data[str(update.message.chat.id)]['notes']
    if len(us_data) != 0:
        for key, value in us_data.items():
            res += f'*** {key} ***\n\n{value}\n\n'
        update.message.reply_text(f'{update.message.chat.first_name}, here are all your notes:\n')
        update.message.reply_text(res)
    else:
        update.message.reply_text('You don\'t have any notes yet')


def delete_note(update, context):
    show_notes(update, context)
    if len(data[str(update.message.chat.id)]['notes']) != 0:
        update.message.reply_text('Write the number of the note you want to delete')
        return 1


def res_notes(update, context):
    user_notes = data[str(update.message.chat.id)]['notes']
    temp = []
    if update.message.text in user_notes:
        for key, value in user_notes.items():
            if str(key) != str(update.message.text):
                temp.append(value)
        user_notes.clear()
        for i in range(1, len(temp) + 1):
            user_notes[str(i)] = temp[i - 1]
        with open('data.json', 'w') as archive:
            json.dump(data, archive)
            archive.close()
        if len(user_notes) != 0:
            update.message.reply_text('Excellent! This is what your notes look like now')
            show_notes(update, context)
        else:
            update.message.reply_text(f'Good, {update.message.chat.first_name}! Now you have no notes')
    else:
        update.message.reply_text('You don\'t have such a note')
    return ConversationHandler.END