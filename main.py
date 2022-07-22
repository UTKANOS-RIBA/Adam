import logging
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler, ConversationHandler
from system_p import stop, start, help, change_tz, change_tz_part_2, check_reminders
from notes import add_note, show_notes, save_note, res_notes, delete_note
from reminders import add_reminder, add_reminder_part_2, delete_reminder, delete_reminder_part_2, show_reminders


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__)

TOKEN = ''


def main():
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher
    start_conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={1: [MessageHandler(Filters.text & ~Filters.command, change_tz_part_2)]},
        fallbacks=[CommandHandler('stop', stop)])
    add_note_conv_handler = ConversationHandler(
        entry_points=[CommandHandler('add_note', add_note)],
        states={'note': [MessageHandler(Filters.text & ~Filters.command, save_note)]},
        fallbacks=[CommandHandler('stop', stop)])
    del_note_conv_handler = ConversationHandler(
        entry_points=[CommandHandler('delete_note', delete_note)],
        states={1: [MessageHandler(Filters.text & ~Filters.command, res_notes)]},
        fallbacks=[CommandHandler('stop', stop)])
    add_reminder_conv_handler = ConversationHandler(
        entry_points=[CommandHandler('add_reminder', add_reminder)],
        states={1: [MessageHandler(Filters.text & ~Filters.command, add_reminder_part_2)]},
        fallbacks=[CommandHandler('stop', stop)])
    delete_reminder_conv_handler = ConversationHandler(
        entry_points=[CommandHandler('delete_reminder', delete_reminder)],
        states={1: [MessageHandler(Filters.text & ~Filters.command, delete_reminder_part_2)]},
        fallbacks=[CommandHandler('stop', stop)])
    inspect_tz_conv_handler = ConversationHandler(
        entry_points=[CommandHandler('change_tz', change_tz)],
        states={1: [MessageHandler(Filters.text & ~Filters.command, change_tz_part_2)]},
        fallbacks=[CommandHandler('stop', stop)])
    dispatcher.add_handler(start_conv_handler)
    dispatcher.add_handler(inspect_tz_conv_handler)
    dispatcher.add_handler(delete_reminder_conv_handler)
    dispatcher.add_handler(add_reminder_conv_handler)
    dispatcher.add_handler(CommandHandler('show_reminders', show_reminders))
    dispatcher.add_handler(add_note_conv_handler)
    dispatcher.add_handler(del_note_conv_handler)
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('show_notes', show_notes))
    dispatcher.add_handler(CommandHandler('help', help))
    updater.start_polling()
    updater.job_queue.run_repeating(check_reminders, interval=10, first=0)
    updater.idle()


if __name__ == '__main__':
    main()
