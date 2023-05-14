import re
import string as s
from db.database import database


class DataValidator:
    """
        Class, which include methods to validate data from
                user input and database.

            ...
            Methods
            -------
            tag_in_message(tag, message_text)
                check if tag is in message text
                Parameters:
                    tag:
                    message_text:
                :return if not return None

            valid_add_group_message(self, message)
                get necessary values from message text
                Parameters:
                    self
                    message
                :return (group_id: str, group_tag: str)

            user_is_new(current_user_id)
                check if user is not in db
                Parameters:
                    current_user_id: str "user-tg-id"
                :return bool value

            group_in_db(user_tg_id, tg_link, tag)
                check if group is in current user db
                Parameters:
                    user_tg_id: str "user-tg-id"
                    tag: str "group-tag"
                :return bool value

            valid_delete_group_message(message)
                validate command message
                Parameters:
                    message: str
                :return valid message or None

            tag_in_db(tag, user_id)
                tag is in db
                Parameters:
                    tag: str "group-tag"
                :return bool value
        """
    def __init__(self):
        self._valid_tag_letters = s.digits + s.ascii_letters + '_'

    @staticmethod
    def get_user_lang(message_inst):
        user_id = str(message_inst.from_user['id'])
        database.set_data_base_connection()
        lang = database.get_user_lang(user_id)
        database.end_connection()
        return lang

    @staticmethod
    def tag_in_message(tag, message_text):
        match = re.search(str(tag), message_text)
        if match:
            return match.group(1)
        return None

    @staticmethod
    def _get_group_id_from_link(link):
        group_id = None
        match = re.search(r"/\+(.*)$", link)

        if match:
            group_id = match.group(1)
        return group_id

    # valid add group message
    def valid_add_group_message(self, message):
        # check if command in message
        message = message.strip(' \n')
        if not message.startswith('add group'):
            return None

        # check messages items count
        message = message.lstrip('add group').strip(' \n')
        message = list(message.split(' '))
        if len(message) != 2:
            return None

        # it token is valid
        for item in message:
            item.strip(" \n")

        group_tag, link = message
        if any(letter not in self._valid_tag_letters for letter in group_tag):
            return None

        group_id = self._get_group_id_from_link(link)
        if not group_id:
            return None

        return group_id, group_tag

    # method check if user is not registered in db
    @staticmethod
    def user_is_new(current_user_id):
        # get all users tg ids from db
        database.set_data_base_connection()
        all_users_tg_ids = database.get_all_users_tg_id()
        database.end_connection()

        # return if curr user id in all users ids in list
        return current_user_id not in all_users_tg_ids

    # group in database of current user
    @staticmethod
    def group_in_db(user_tg_id, tg_link, tag):
        # get all user groups from db
        database.set_data_base_connection()
        all_user_groups = database.get_user_groups(user_tg_id)
        database.end_connection()

        # if group in this list -> true else -> false
        for item in all_user_groups:
            if tg_link == item[0] or tag == item[1]:
                return True
        return False

    # "delete group {group tag}" valid message
    @staticmethod
    def valid_delete_group_message(message):
        # check if command in message
        message = message.lower().strip(' \n')
        if not message.startswith('delete group'):
            return None
        message = message[13:]
        return message

    # tag in db
    @staticmethod
    def tag_in_db(tag, user_id):
        # get all user groups
        database.set_data_base_connection()
        users_groups = database.get_user_groups(user_id)
        database.end_connection()

        # return if tag in current groups tags
        return tag in [item[1] for item in users_groups]


validator = DataValidator()
