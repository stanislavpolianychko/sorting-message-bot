from src.bot import bot
from aiogram import types
from message_handler import message_handler
from validator import validator
from db.database import database
from trans.message_parser import message_parser


class CommandHandler:
    """
        Class to handle all commands
            inputted by user

             ...
            Methods
            -------
            @bot.bot_dispatcher.message_handler(commands=['command name'])
            async def command(message)
                method answer on user command
    """

    # manage /start command
    @staticmethod
    @bot.bot_dispatcher.message_handler(commands=['start'])
    async def send_welcome(message: types.Message):
        user_id = str(message.from_user['id'])

        if validator.user_is_new(user_id):
            database.set_data_base_connection()
            database.set_new_user(user_id)
            database.end_connection()

        await message.reply(f"Hi, {message.from_user['first_name']} {message.from_user['last_name']}.\n" +
                            message_parser.message('start', 'en'))

    # manage /info command
    @staticmethod
    @bot.bot_dispatcher.message_handler(commands=['info'])
    async def send_info(message: types.Message):

        await message.reply(message_parser.message('info', validator.get_user_lang(message)))

    # manage /run_managing command
    @staticmethod
    @bot.bot_dispatcher.message_handler(commands=['run_managing'])
    async def run_groups_managing(message: types.Message):
        database.set_data_base_connection()
        user_groups = database.get_user_groups(database.get_user_id(message.from_user['id']))
        database.end_connection()
        if not user_groups:
            await message.reply(message_parser.message('run-managing-denied', validator.get_user_lang(message)))
            return
        await message.reply(message_parser.message('run-managing-successful', validator.get_user_lang(message)))
        bot.bot_dispatcher.register_message_handler(message_handler.handle_group_to_add_message)

    # manage /stop_managing command
    @staticmethod
    @bot.bot_dispatcher.message_handler(commands=['stop_managing'])
    async def stop_groups_managing(message: types.Message):
        await message.reply(message_parser.message('stop-managing', validator.get_user_lang(message)))

    # "add group {group invite link} {group tag}"
    @staticmethod
    @bot.bot_dispatcher.message_handler(lambda message: 'add group' in message.text.lower())
    async def add_group(message: types.Message):
        # try to get tuple of link and tag from message
        tup = validator.valid_add_group_message(message.text)

        # get user id from database
        database.set_data_base_connection()
        user_id = database.get_user_id(message.from_user['id'])
        database.end_connection()

        # if tg_link and tag is not possible to get (is none)
        if not tup:
            await message.reply(message_parser.message('add-group-denied', validator.get_user_lang(message)))
            return

        tg_link, tag = tup
        # if this group is already in database
        if validator.group_in_db(user_id, tg_link, tag):
            await message.reply(message_parser.message('add-group-denied', validator.get_user_lang(message)))
            return

        database.set_data_base_connection()
        database.set_new_group(tg_link, tag, user_id)
        database.end_connection()
        await message.reply(message_parser.message('add-group-successful', validator.get_user_lang(message)))  # added

    # "delete group {group tag}"
    @staticmethod
    @bot.bot_dispatcher.message_handler(lambda message: 'delete group' in message.text.lower())
    async def delete_group(message: types.Message):
        tag = validator.valid_delete_group_message(message.text)  # get current tag from messages
        database.set_data_base_connection()
        user_id = str(database.get_user_id(message.from_user['id']))
        database.end_connection()

        if tag and validator.tag_in_db(tag, user_id):  # check if tag exist and is it's in db
            # delete group from db
            database.set_data_base_connection()
            database.delete_group(user_id, tag)
            database.end_connection()
            # deleted
            await message.reply(message_parser.message('delete-group-successful', validator.get_user_lang(message)))
            return
        # not deleted
        await message.reply(message_parser.message('delete-group-denied', validator.get_user_lang(message)))

    # manage /my_groups command
    @staticmethod
    @bot.bot_dispatcher.message_handler(commands=['my_groups'])
    async def get_groups_list(message: types.Message):
        await message.reply(message_parser.all_user_groups(message.from_user['id'], validator.get_user_lang(message)))

    # manage /en command
    @staticmethod
    @bot.bot_dispatcher.message_handler(commands=['en'])
    async def set_language_en(message: types.Message):
        database.set_data_base_connection()
        database.update_user_lang(message.from_user['id'], 'en')
        database.end_connection()
        await message.reply(message_parser.message('en', 'en'))

    # manage /ua command
    @staticmethod
    @bot.bot_dispatcher.message_handler(commands=['ua'])
    async def set_language_ua(message: types.Message):
        database.set_data_base_connection()
        database.update_user_lang(message.from_user['id'], 'ua')
        database.end_connection()
        await message.reply(message_parser.message('ua', 'ua'))

    # manage /how_to_add_group command
    @staticmethod
    @bot.bot_dispatcher.message_handler(commands=['how_to_add_group'])
    async def send_how_to_add_group(message: types.Message):
        await message.reply(message_parser.message('how-to-add-group', validator.get_user_lang(message)))

    # manage /how_to_delete_group command
    @staticmethod
    @bot.bot_dispatcher.message_handler(commands=['how_to_delete_group'])
    async def send_how_to_delete_group(message: types.Message):
        await message.reply(message_parser.message('how-to-delete-group', validator.get_user_lang(message)))


# add message handling
