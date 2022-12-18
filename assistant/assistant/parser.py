from typing import List
from decorators import *
# from assistant.decorators import *


class Parsers:

    __commands: List[str] = [
        'hello',
        'close',
        'good bye',
        'exit',

        'note add',
        'note del',
        'note edit tag',
        'note edit',
        'note find by tag',
        'note find',
        'note show by tag',
        'note show',

        'contact add',
        'contact edit',
        'contact del',
        'contact find',
        'contact show',

        'contact birthday',

        'sort file',
        'help'
    ]

    @parser_handler
    def parse_user_input(self, user_input: str) -> tuple[str, str]:
        user_input_list = user_input.split(' ')
        for command in self.__commands:
            command_list = command.split(' ')
            if command == ' '.join(user_input_list[:len(command_list):]).lower():
                parser = getattr(self, '_' + command.replace(' ', '_'))
                return parser(' '.join(user_input_list[len(command_list)::]))
        raise ValueError("Unknown command!")

    @staticmethod
    def _hello(user_input: str):
        return 'hello', ''

    @staticmethod
    def _close(user_input: str):
        return 'exit', ''

    @staticmethod
    def _good_bye(user_input: str):
        return 'exit', ''

    @staticmethod
    def _exit(user_input: str):
        return 'exit', ''
    # --------------- N O T E --------------------

    @staticmethod
    def _note_add(note_name: str):
        if note_name == '':
            raise ValueError("Bad input")
        else:
            return "note add", note_name

    @staticmethod
    def _note_del(note_name: str):
        if note_name == '':
            raise ValueError("Bad input")
        else:
            return "note del", note_name

    @staticmethod
    def _note_edit_tag(note_name: str):
        if note_name == '':
            raise ValueError("Bad input")
        else:
            return "note edit tag", note_name

    @staticmethod
    def _note_edit(note_name: str):
        if note_name == '':
            raise ValueError("Bad input")
        else:
            return "note edit", note_name

    @staticmethod
    def _note_find_by_tag(user_input: str):
        return "note find by tag", user_input

    @staticmethod
    def _note_find(user_input: str):
        return "note find", user_input

    @staticmethod
    def _note_show_by_tag(user_input: str):
        return "note show by tag", user_input

    @staticmethod
    def _note_show(user_input: str):
        return "note show", ''

    # -------------- C O N T A C T ---------------------

    @staticmethod
    def _contact_add(username: str):
        if username == '':
            raise ValueError("Bad input")
        else:
            return "contact add", username

    @staticmethod
    def _contact_edit(username: str):
        if username == '':
            raise ValueError("Bad input")
        else:
            return "contact edit", username

    @staticmethod
    def _contact_del(username: str):
        if username == '':
            raise ValueError("Bad input")
        else:
            return "contact del", username

    @staticmethod
    def _contact_find(username: str):
        if username == '':
            raise ValueError("Bad input")
        else:
            return "contact find", username

    @staticmethod
    def _contact_show(user_input: str):
        return "contact show", ''

    @staticmethod
    def _contact_birthday(user_input: str):
        return "contact birthday", user_input

    @staticmethod
    def _sort_file(user_input: str):
        return "sort file", user_input

    @staticmethod
    def _help(user_input: str):
        return "help", ''
