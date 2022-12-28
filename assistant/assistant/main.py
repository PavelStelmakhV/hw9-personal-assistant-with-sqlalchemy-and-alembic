# from assistant import contact_book
# from assistant import note_book
# from assistant import help
# from assistant import sort
# from assistant import parser
# from assistant.decorators import *

# import contact_book
from contact_book import Name, Phone, Address, Birthday, Email, AddressBook, Record
import note_book
import help
import sort
import parser
from decorators import *

from abc import ABC, abstractmethod


class AbstractInputOutput(ABC):

    @abstractmethod
    def user_input(self, pre_input: str = '') -> str:
        pass

    @abstractmethod
    def user_output(self, text_output: str = ''):
        pass


class CLIInputOutput(AbstractInputOutput):

    def user_input(self, pre_input: str = '') -> str:
        result = input(f'{pre_input}')
        return result

    def user_output(self, text_output: str = ''):
        print(text_output)


class InputOutput:
    def __init__(self):
        self.contactbook: AddressBook = None
        self.notebook: note_book.Notebook = None
        self._sortfolder = sort.SortFolder()
        self._parsers = parser.Parsers()
        self._help = help.Help()
        self._io: AbstractInputOutput = CLIInputOutput()

    @command_handler
    def hello_handler(self, *args) -> str:
        return 'How can I help you?'

    @command_handler
    def exit_handler(self, *args):
        raise SystemExit('Good bye!')

    @command_handler
    def note_add_handler(self, argument: str) -> str:
        input_text = self._io.user_input('Input text note:')
        return self.notebook.add_note(argument, input_text)

    @command_handler
    def note_del_handler(self, argument: str) -> str:
        return self.notebook.del_note(argument)

    @command_handler
    def note_edit_tag_handler(self, argument: str) -> str:
        self.notebook.edit_note_tag(argument)
        flag = self._io.user_input('input add or delete tag (a/d)')
        if flag == 'a':
            tag = self._io.user_input('input new tag: ')
            return self.notebook.edit_note_tag_add(argument, tag)
        else:
            tag = self._io.user_input('input remove tag: ')
            return self.notebook.edit_note_tag_del(argument, tag)
    # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

    @command_handler
    def note_edit_handler(self, name_note: str) -> str:
        self._io.user_output(self.notebook[name_note])
        text_note = self._io.user_input('>')
        flag = self._io.user_input('input add or overwrite text (a/o)')
        if flag == 'a':
            add_text = True
        elif flag == 'o':
            add_text = False
        return self.notebook.edit_note_text(name_note, text_note, add_text)

    @command_handler
    def note_find_by_tag_handler(self, argument: str) -> str:
        return self.notebook.find_note_by_tag(argument)

    @command_handler
    def note_find_handler(self, argument: str) -> str:
        return self.notebook.find_note(argument)

    @command_handler
    def note_show_by_tag_handler(self, argument: str) -> str:
        return self.notebook.show_note_by_tag()

    @command_handler
    def note_show_handler(self, argument: str) -> str:
        return self.notebook.show_note()
    # -------------------------------------------------

    @command_handler
    def contact_add_handler(self, argument: str) -> str:
        name = Name(argument)
        phone = self._get_phone()
        address = self._get_address()
        email = self._get_email()
        birthday = self._get_birthday()
        result = self.contactbook.add_record(name=name, phone=phone, address=address, email=email, birthday=birthday)
        return result

    @command_handler
    def _get_phone(self, new_old: str = None) -> Phone:
        num_phone = self._io.user_input(f'Input {new_old} phone (format +XXXXXXXXXXXX): ')
        if num_phone is not None:
            return Phone(num_phone)

    @command_handler
    def _get_address(self) -> Address:
        address = self._io.user_input('Input address: ')
        if address is not None:
            return Address(address)

    @command_handler
    def _get_email(self) -> Email:
        email = self._io.user_input('Input email: ')
        if email is not None:
            return Email(email)

    @command_handler
    def _get_birthday(self) -> Birthday:
        birthday = self._io.user_input('Input birthday: ')
        if birthday is not None:
            return Birthday(birthday)

    # --------------------------------------------
    @command_handler
    def contact_edit_handler(self, argument: str) -> str:
        name = Name(argument)
        record = Record(name)
        if not record.exist_record():
            return f'Contact with this name does not exist.'

        self._io.user_output('1. Add phone\n2. Delete phone\n3. Change phone\n4. Change address\n5. Change E-mail'
                             '\n6. Change birthday')
        num_choose = self._io.user_input('Choose a number: ')
        operation_with_record = ['_add_phone', '_remove_phone', '_change_phone', '_add_address', '_add_email',
                                 '_add_birthday']
        self._io.user_output(operation_with_record[int(num_choose)-1])
        command_function = getattr(self, operation_with_record[int(num_choose)-1])
        result = command_function(name)

        return f'Edited record {argument}. {result}'
    # ------------------------------------------------------------

    @command_handler
    def _add_phone(self, name: Name) -> str:
        new_phone = self._get_phone(new_old='new')
        if new_phone is not None:
            return self.contactbook.edit_record(operation='_add_phone', name=name, new_phone=new_phone)

    @command_handler
    def _remove_phone(self, name: Name) -> str:
        old_phone = self._get_phone(new_old='removable')
        if old_phone is not None:
            return self.contactbook.edit_record(operation='_change_phone', name=name, old_phone=old_phone)

    @command_handler
    def _change_phone(self, name: Name) -> str:
        old_phone = self._get_phone(new_old='removable')
        new_phone = self._get_phone(new_old='new')
        if (old_phone is not None) and (new_phone is not None):
            return self.contactbook.edit_record(operation='_del_phone', name=name, old_phone=old_phone,
                                                new_phone=new_phone)

    @command_handler
    def _add_address(self, name: Name) -> str:
        address = self._get_address()
        if address is not None:
            return self.contactbook.edit_record(operation='_add_phone', name=name, address=address)

    @command_handler
    def _add_email(self, name: Name) -> str:
        email = self._get_email()
        if email is not None:
            return self.contactbook.edit_record(operation='_add_phone', name=name, email=email)

    @command_handler
    def _get_birthday(self, name: Name) -> str:
        birthday = self._get_birthday()
        if birthday is not None:
            return self.contactbook.edit_record(operation='_add_phone', name=name, birthday=birthday)

    #*********************************************

    @command_handler
    def contact_del_handler(self, argument: str) -> str:
        return self.contactbook.remove_record(name=Name(argument))

    @command_handler
    def contact_find_handler(self, argument: str) -> str:
        return self.contactbook.find_record(argument)

    @command_handler
    def contact_show_handler(self, *args) -> str:
        if len(self.contactbook) == 0:
            return 'Phone book is empty'
        try:
            max_line = int(args[0])
        except ValueError:
            max_line = len(self.contactbook)
        result = 'Phone book:\n'
        num_page = 0
        for page in self.contactbook.iterator(max_line=max_line):
            num_page += 1
            result += f'<< page {num_page} >>\n' if max_line < len(self.contactbook) else ''
            result += page
        return result

    @command_handler
    def contact_birthday_handler(self, argument) -> str:
        return self.contactbook.show_record_with_birthday(int(argument))

    @command_handler
    def sort_file_handler(self, argument: str) -> str:
        return self._sortfolder.sort_files(argument)

    @command_handler
    def help_handler(self, *args):
        return self._help.show()

    def setup_phonebook(self, phonebook):
        self.contactbook = phonebook

    def setup_notebook(self, notebook):
        self.notebook = notebook

    def loop_input_output(self):
        while True:
            user_input = self._io.user_input('Command: ')

            result = self._parsers.parse_user_input(user_input=user_input)
            if len(result) != 2:
                self._io.user_output(result)
                continue
            command, argument = result
            command_function = getattr(self, command.replace(" ", "_") + "_handler")

            try:
                command_response = command_function(argument)
                self._io.user_output(command_response)
            except SystemExit as e:
                self._io.user_output(str(e))
                break

    def run(self):

        with contact_book.AddressBook() as phonebook:
            self.setup_phonebook(phonebook)
            with note_book.Notebook() as notebook:
                self.setup_notebook(notebook)
                self.loop_input_output()


def main():

    input_output = InputOutput()
    input_output.run()


if __name__ == '__main__':

    main()
