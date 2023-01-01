from collections import UserDict
import pickle
from pathlib import Path

from assistant.assistant.database import crud_note


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
        result = f'\nTitle: {self.__name}\nTag: {tag_string}\n{self.__text_note}'
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

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__save_book()

    def save_book(self):
        self.__save_book()

    def __load_book(self):
        pass

    def __save_book(self):
        pass

    # -----------------------------------

    @staticmethod
    def convert_note_from_db(note_db) -> Note:
        note = Note(name=note_db.title, text_note=note_db.description)
        for tag in note_db.tags:
            note.add_tag(tag.name)
        return note

    def get_note_from_db(self, title: str) -> Note:
        note_db = crud_note.get_note_by_name(title=title)
        return self.convert_note_from_db(note_db)

    @staticmethod
    def put_note_to_db(note: Note):
        crud_note.create_note(title=note.name, description=note.text_note)

    def add_note(self, name: str, text_note: str = None):
        if name == '':
            raise ValueError('Name cannot be empty')
        if not crud_note.exist_note(title=name):
            note = Note(name=name, text_note=text_note)
            self.put_note_to_db(note=note)
            return f'Record "{name}" added to notebook'
        else:
            raise ValueError('This name already exists')

    @staticmethod
    def remove_note(name: str):
        if crud_note.exist_note(title=name):
            crud_note.remove_note(title=name)
            return f'Note "{name}" deleted to from notebook'
        else:
            raise ValueError(f'Note "{name}" not found')

    @staticmethod
    def edit_note_tag(name: str):
        if not crud_note.exist_note(title=name):
            raise ValueError(f'Note "{name}" not found')

    @staticmethod
    def edit_note_tag_add(name: str, tag: str):
        crud_note.create_tag(title_note=name, name=tag)
        return f'Tag <{tag}> in note {name} added'

    @staticmethod
    def edit_note_tag_del(name: str, tag: str):
        crud_note.remove_tag(note_title=name, tag_name=tag)
        return f'Tag <{tag}> in note {name} deleted'

    @staticmethod
    def edit_note_text(name: str, text_note: str, add_text: bool):
        if not crud_note.exist_note(title=name):
            raise ValueError(f'Note "{name}" not found')
        crud_note.update_note(title=name, description=text_note, add_text=add_text)
        return f'Text in note {name} changed'

    @staticmethod
    def find_note(find_text: str):
        find_result = []
        notes = crud_note.find_note(find_text=find_text)
        for note in notes:
            find_result.append(f'"{note.title}"')
        if len(find_result) > 0:
            return f'Notes where "{find_text}" were found: ' + ', '.join(find_result)
        return f'"{find_text}" matches not found'

    @staticmethod
    def find_note_by_tag(tag_name: str):
        find_result = []
        notes = crud_note.find_note_by_tag(tag_name=tag_name)
        for note in notes:
            find_result.append(f'"{note.title}"')
        if len(find_result) > 0:
            return f'Notes with tag "{tag_name}" were found: ' + ', '.join(find_result)
        return f'Note with tag "{tag_name}" not found'

    def show_note(self, note_title: str = ''):
        if note_title != '':
            return str(self.get_note_from_db(note_title))

        result = ''
        notes_db = crud_note.find_note(find_text='')
        for note_db in notes_db:
            note = self.convert_note_from_db(note_db=note_db)
            result += str(note) + '\n'
        return result

    @staticmethod
    def show_note_by_tag():
        result = ''
        tags_db = crud_note.tags_all()
        notes_db = crud_note.notes_all()

        for tag_db in tags_db:
            notes = []
            for note in tag_db.notes:
                notes.append(f'"{note.title}"')
            result += f'<{tag_db.name}>: ' + ', '.join(notes) + '\n'

        notes = []
        for note_db in notes_db:
            if not note_db.tags:
                notes.append(f'"{note_db.title}"')
        result += f'notes without tags: ' + ', '.join(notes) + '\n'

        return result


if __name__ == '__main__':
    with Notebook() as notebook:
        # r = notebook.get_note_from_db('Выдержать.')
        # print(r)
        #
        # r = notebook.add_note('test', 'Description')
        # print(r)
        #
        # print(crud_note.create_tag('test', 'asdfgh'))
        # print(crud_note.create_tag('Выдержать.', 'asdfgh'))
        #
        # r = notebook.show_note()
        # print(r)

        # notebook.edit_note_text('test', ' new Description', add_text=True)

        r = notebook.show_note_by_tag()
        print(r)

