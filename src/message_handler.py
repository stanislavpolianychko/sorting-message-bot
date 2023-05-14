from aiogram import types
from src.bot import bot
from db.database import database
from src.validator import validator


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
                pass
                # resend message to some group

        # else statement
        # write why not resend message
        # looking for "some tag in message":
        # if tag of predefined group is in message text:
        # resending to added group
        # else: ask for group tag in c
        # there message should be parsed if it's possible and written to database
        await bot.bot_instance.send_message(chat_id=message.chat.id, text=f'You said: {message.text}')


message_handler = MessageHandler()
