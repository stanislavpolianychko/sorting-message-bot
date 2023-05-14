from config.config import config
from aiogram import Bot, Dispatcher, executor
import logging


class SortingBot:
    """
        Singleton class to create
            bot instance.
            ...

            Attributes
            ----------
            bot_instance: Bot
                instance of bot from aiogram library
            bot_dispatcher: Dispatcher
                instance of bots dispatcher from aiogram library

            Methods
            -------
            run_bot(self):
                method to start bot. and make it work endless
    """

    # creating singleton pattern
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    # initialise all bot variables, and main "bot_dispatcher"
    def __init__(self):
        self._token = config.bot['token']
        logging.basicConfig(level=logging.INFO)
        self.bot_instance = Bot(self._token)
        self.bot_dispatcher = Dispatcher(self.bot_instance)

    # run endless loop of the bot
    def run_bot(self):
        executor.start_polling(self.bot_dispatcher, skip_updates=True)


bot = SortingBot()
