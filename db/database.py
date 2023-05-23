import psycopg2 as db
from config.config import config


class DataBase:
    """
        Class for reading and writing
            database data.

            ...
            Methods
            -------
            set_data_base_connection(self):
                used to set connection to db

            end_connection(self):
                unplug db connection

            set_new_user(self, user_tg_id):
                Parameters:
                    self
                    user_tg_id: str "user-tg-id"

            get_user_id(self, user_tg_id):
                Parameters:
                    self
                    user_tg_id: str "user-tg-id"
                :return int(user_num_id)

            get_all_users_tg_id(self):
                Parameters:
                    self
                :return list["user-tg-id", ]

            set_new_group(self, telegram_link, tag, user_id):
                insert new group into groups table
                Parameters:
                    self
                    telegram_link: str "user-tg-id"
                    tag: str "group-tag"

            get_user_groups(self, user_id):
                Parameters:
                    self
                    user_id: int (primary key of user)

            delete_group(self, user_id, tag):
                delete group by tag and user id
                Parameters:
                    self
                    user_id: int (primary key of user)
                    tag: str "group-tag"

            create_tables(self):
                create user and groups table

            drop_tables(self):
                drop all tables in database (user and groups)
    """
    def __init__(self):
        # future connection instance
        self._connection = None

        # configure values
        self._host = config.database['host']
        self._user = config.database['user']
        self._password = config.database['password']
        self._name = config.database['name']

    # open database
    def set_data_base_connection(self):
        try:
            # connection to database server
            self._connection = db.connect(
                host=self._host,
                user=self._user,
                password=self._password,
                database=self._name
            )
            # perform request
            self._connection.autocommit = True
        except Exception as ex:
            print(ex)

    # close database
    def end_connection(self):
        if self._connection:
            self._connection.close()

    # create table user[id: unique id, user_tg_id(int): user_id(str)]
    def _create_user_table(self):
        with self._connection.cursor() as cursor:
            cursor.execute(
                """CREATE TABLE users(
                    id SERIAL PRIMARY KEY,
                    user_tg_id VARCHAR(50) NOT NULL,
                    lang VARCHAR(10) NOT NULL);"""
            )

    # set new user into a table
    def set_new_user(self, user_tg_id):
        with self._connection.cursor() as cursor:
            cursor.execute(
                f"""INSERT INTO users (user_tg_id, lang) 
                VALUES ('{user_tg_id}', 'en');"""
            )

    # get current user id by telegram id
    def get_user_id(self, user_tg_id):
        with self._connection.cursor() as cursor:
            cursor.execute(
                f"""SELECT id FROM users
                    WHERE user_tg_id = '{user_tg_id}';"""
            )
            return cursor.fetchone()[0]

    def update_user_lang(self, user_tg_id, lang):
        with self._connection.cursor() as cursor:
            cursor.execute(
                f"""UPDATE users SET lang = '{lang}'
                    WHERE user_tg_id = '{user_tg_id}';"""
            )

    def get_user_lang(self, user_tg_id):
        print(user_tg_id)
        with self._connection.cursor() as cursor:
            cursor.execute(
                f"""SELECT lang FROM users
                    WHERE user_tg_id = '{user_tg_id}';"""
            )
            print(cursor.fetchone())
            return cursor.fetchone[0]

    # get list of all users
    def get_all_users_tg_id(self):
        with self._connection.cursor() as cursor:
            cursor.execute(
                """SELECT user_tg_id FROM users;"""
            )
            return [item[0] for item in cursor.fetchall()]

        # GROUPS TABLE QUERIES
    # create table user[id: unique id, telegram_link(str), user_id(int)]
    def _create_groups_table(self):
        with self._connection.cursor() as cursor:
            cursor.execute(
                """CREATE TABLE groups (
                    id SERIAL PRIMARY KEY,
                    telegram_link VARCHAR(50) NOT NULL,
                    tag VARCHAR(50) NOT NULL,
                    user_id INTEGER REFERENCES users(id)
                    );"""
            )

    # set new group into a table
    def set_new_group(self, telegram_link, tag,  user_id):
        with self._connection.cursor() as cursor:
            cursor.execute(
                f"""INSERT INTO groups (telegram_link, tag, user_id) VALUES
                    ('{telegram_link}', '{tag}', '{user_id}');"""
            )

    # get list of groups
    def get_user_groups(self, user_id):
        with self._connection.cursor() as cursor:
            cursor.execute(
                f"""SELECT telegram_link, tag FROM groups
                    WHERE user_id = '{user_id}';"""
            )
            return cursor.fetchall()

    # get group id by the tag
    @staticmethod
    def get_group_id(tag, user_id):
        database.set_data_base_connection()
        all_groups = database.get_user_groups(user_id)
        database.end_connection()
        for group in all_groups:
            if group[1] == tag:
                return group[0]

    # delete some group by tag from table
    def delete_group(self, user_id, tag):
        with self._connection.cursor() as cursor:
            cursor.execute(
                f"""DELETE FROM groups 
                    WHERE user_id = {user_id}
                    AND tag = '{tag}';"""
            )

    # create all tables
    def create_tables(self):
        self.set_data_base_connection()
        self._create_user_table()
        self._create_groups_table()
        self.end_connection()

    def _delete_users_table(self):
        with self._connection.cursor() as cursor:
            cursor.execute(
                """DROP TABLE users;"""
            )

    def _delete_groups_table(self):
        with self._connection.cursor() as cursor:
            cursor.execute(
                """DROP TABLE groups;"""
            )

    # drop all database tables
    def drop_tables(self):
        self.set_data_base_connection()
        self._delete_groups_table()
        self._delete_users_table()
        self.end_connection()


database = DataBase()
