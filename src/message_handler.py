from aiogram import types
from src.bot import bot
from db.database import database
from src.validator import validator
from trans.message_parser import message_parser


class MessageHandler:
    """
        Class to handle all commands
            inputted by user

             ...
            Methods
            -------
            @staticmethod
            handle_group_to_add_message(message):
                method resend messages to defined group by the tag
                Parameters:
                    message: types.Message
    """
    @staticmethod
    async def handle_group_to_add_message(message: types.Message):
        database.set_data_base_connection()
        user_group_tags = [item[1] for item in database.get_user_groups(database.get_user_id(message.from_user['id']))]
        database.end_connection()

        for tag in user_group_tags:
            if validator.tag_in_message(tag, message.text):
                group_id = database.get_group_id(tag, message.from_user['id'])
                await bot.send_message(chat_id=group_id, text=message.text)
                await message.reply(message_parser.message(validator.get_user_lang(message),
                                                           'message-resend-successful'))
                return

        await bot.bot_instance.send_message(
            chat_id=message.chat.id, text=message_parser.message(validator.get_user_lang(message),
                                                                 'message-resend-denied'))


message_handler = MessageHandler()
