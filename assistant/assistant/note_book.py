from collections import UserDict
import pickle
from pathlib import Path


class Note:
    def __init__(self, name: str, text_note: str = None):
        self.__name = None
        self.__text_note = None
        self.tags: list = []

        self.__name = name
        self.__text_note = text_note

    def __str__(self):
        tag_string = ''
        if len(self.tags) > 0:
            tag_string = '><'.join(self.tags)
            tag_string = '<' + tag_string + '>'
        result = f'\nNote: {self.__name}\nTag: {tag_string}\n{self.__text_note}'
        return result

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name: str):
        self.__name = name

    @property
    def text_note(self):
        return self.__text_note

    @text_note.setter
    def text_note(self, text_note: str):
        self.__text_note = text_note

    def edit_text_note(self, new_text: str, add_text=True):
        # new_text = input('Input text:')
        if add_text:
            self.text_note += new_text
        else:
            self.text_note = new_text

    def add_tag(self, value: str):
        if not (value in self.tags):
            self.tags.append(value)

    def del_tag(self, value: str):
        try:
            self.tags.remove(value)
        except ValueError:
            return f"{value} does not exists"


class Notebook(UserDict):
    __path = Path('~').expanduser()
    __file_name = __path / 'note_book.pickle'

    def __enter__(self):
        self.__load_book()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__save_book()

    def save_book(self):
        self.__save_book()

    def __load_book(self):
        try:
            with open(self.__file_name, 'rb') as file:
                book = pickle.load(file)
                self.data.update(book)
        except FileNotFoundError:
            pass

    def __save_book(self):
        try:
            with open(self.__file_name, 'wb') as file:
                pickle.dump(self.data, file, protocol=pickle.HIGHEST_PROTOCOL)
        except Exception:
            print("Some problems! Don't save notebook")

    def add_note(self, name: str, text_note: str = None):
        if name == '':
            raise ValueError('Name cannot be empty')
        if not (name in self.data.keys()):
            self.data[name] = Note(name=name, text_note=text_note)
            return f'Record "{name}" added to notebook'
        else:
            raise ValueError('This name already exists')

    def del_note(self, name: str):
        if name in self.data:
            del self.data[name]
            return f'Record "{name}" deleted to from notebook'
        else:
            raise ValueError(f'Note "{name}" not found')

    def edit_note_tag(self, name: str):
        if not(name in self.data.keys()):
            raise ValueError(f'Note "{name}" not found')

    def edit_note_tag_add(self, name: str, tag: str):
        self.data[name].add_tag(tag)
        return f'Tag <{tag}> in note {name} added'

    def edit_note_tag_del(self, name: str, tag: str):
        self.data[name].del_tag(tag)
        return f'Tag <{tag}> in note {name} deleted'

    def edit_note_text(self, name: str, text_note: str, add_text: bool):
        if not(name in self.data.keys()):
            raise ValueError(f'Note "{name}" not found')
        self.data[name].edit_text_note(text_note, add_text=add_text)
        return f'Text in note {name} changed'

    def find_note(self, find_text: str):
        find_result = []
        for note in self.data.values():  # type: Note
            # find by name or text
            if find_text.lower() in str(note.name).lower() or find_text.lower() in str(note.text_note).lower():
                find_result.append(f'"{note.name}"')
        if len(find_result) > 0:
            return f'Notes where "{find_text}" were found: ' + ', '.join(find_result)
        return f'"{find_text}" matches not found'

    def find_note_by_tag(self, find_tag: str):
        find_result = []
        for note in self.data.values():  # type: Note
            # find by name or text
            if find_tag in note.tags:
                find_result.append(f'"{note.name}"')
            if find_tag == '' and len(note.tags) == 0:
                find_result.append(f'"{note.name}"')
        if len(find_result) > 0:
            return f'Notes with tag "{find_tag}" were found: ' + ', '.join(find_result)
        return f'Note with tag "{find_tag}" not found'

    def show_note(self):
        result = ''
        for note in self.data.values():
            result += str(note) + '\n'
        return result

    def show_note_by_tag(self):
        result = ''
        result_dict = {}
        for note in self.data.values():
            if len(note.tags) == 0:
                if not ('' in result_dict.keys()):
                    result_dict[''] = []
                result_dict[''].append(f'"{note.name}"')
            for tag in note.tags:
                if not (tag in result_dict.keys()):
                    result_dict[tag] = []
                result_dict[tag].append(f'"{note.name}"')
        for key, value in result_dict.items():
            result += f'<{key}>: ' + ', '.join(value) + '\n'
        return result
