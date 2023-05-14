from configparser import ConfigParser


class Configuration:
    """
        Singleton class for getting config parameters
                    from defined file.

        ...

        Attributes
        ----------
        parser: ConfigParser
            instance of ConfigParser class. used to parse config.ini file

        Methods
        -------
        bot(self):
            Parameters:
                self
            :return dict {key: str: value}, where key is "name of bot param"
        database(self):
            Parameters:
                self
            :return dict {key: str: value}, where key is "name of database param"
    """

    # part of the class to create singleton pattern
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, file_name):
        self.parser = ConfigParser()
        self.parser.read(file_name)

    # representation of all config file sections
    def __repr__(self):
        return str(self.parser.sections())

    # get data from config file and validate it
    def _get_valid_data(self, section, param_name):
        value = self.parser.get(section, param_name)
        if value.isdigit():
            return int(value)
        elif value in ('true', 'false'):
            return bool(value)
        return value

    @staticmethod
    def _get_valid_messages_dict(messages_dict):
        result_dict = {}
        for key, value in messages_dict.items():
            new_value = ''
            for letter in value:
                new_value += '\n' if letter == '|' else letter
            result_dict[key] = new_value
        return result_dict

    # get dictionary: section_dict = {param_name, validated_value}
    def _get_section_dict(self, section):
        return {name: self._get_valid_data(section, name) for name in self.parser.options(section)}

    # properties which present config parts
    @property
    def bot(self):
        """"""
        return self._get_section_dict('bot')

    @property
    def database(self):
        return self._get_section_dict('database')


# I'm using global link in the reason of config library fault
config = Configuration('/Users/admin/PycharmProjects/TelegramSortingBot/config/config.ini')
