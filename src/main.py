from src.bot import bot
from command_handler import CommandHandler
from db.database import database


# run bot
if __name__ == '__main__':
    database.create_tables()

    commands_handler = CommandHandler()
    bot.run_bot()

    database.drop_tables()
