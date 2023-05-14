import json
from db.database import database


class MessageParser:
    """
         Singleton message parser class, to get bot messages from json files.
            ...

            Methods
            -------
            message(self, message_name, lang)
                message_name: str (name in json file)
                lang: 'en'/'ua'

            all_user_groups(self, user_tg_id, lang)
                method to create message with user groups list:
                Parameters:
                    user_tg_id: str "user-tg-id"
                    lang: 'en'/'ua'
    """

    # creating singleton pattern
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    # init lang file
    def __init__(self):
        with open("trans/english_messages.json", 'r') as json_file:
            self._english_messages = json.loads(json_file.read())

        with open("ukrainian_messages.json", 'r') as json_file:
            self._ukrainian_messages = json.loads(json_file.read())

    def message(self, message_name, lang):
        if lang == 'ua':
            return self._ukrainian_messages[message_name]
        elif lang == 'en':
            return self._english_messages[message_name]

    def all_user_groups(self, user_tg_id, lang):
        database.set_data_base_connection()
        groups_list = [item[1] for item in database.get_user_groups(database.get_user_id(user_tg_id))]
        database.end_connection()

        message = self.message('all-groups', lang) if groups_list else self.message('no-groups-added', lang)
        for group_tag in groups_list:
            message += f'- "{group_tag}"\n'
        return message


message_parser = MessageParser()
