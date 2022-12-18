from collections import UserDict
from datetime import datetime, timedelta
import pickle
from pathlib import Path


class Field:
    def __init__(self, value: str):
        self.__value = None

        self.value = value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        self.__value = value


class Birthday(Field):
    def __init__(self, value: datetime):
        super().__init__(value)

    @Field.value.setter
    def value(self, value):
        if len(value) == 0:
            raise ValueError('Name length must be greater than 0')
        if '.' in value:
            Field.value.fset(self, datetime.strptime(value, '%d.%m.%Y'))
        elif '/' in value:
            Field.value.fset(self, datetime.strptime(value, '%d/%m/%Y'))
        else:
            raise ValueError('Date must be in the format "dd/mm/yyyy" or "dd.mm.yyyy"')


class Name(Field):
    def __init__(self, value):
        super().__init__(value)

    @Field.value.setter
    def value(self, value):
        if len(value) > 0:
            Field.value.fset(self, value)
        else:
            raise ValueError('Name length must be greater than 0')


class Phone(Field):
    def __init__(self, value):
        super().__init__(value)

    @Field.value.setter
    def value(self, value):
        if len(value) == 0:
            raise ValueError('Phone length must be greater than 0')
        if len(value) == 9 and str(value).isdigit():
            value = '+380' + str(value)
            Field.value.fset(self, value)
        elif len(value[1::]) == 12 and str(value[1::]).isdigit() and value[0] == '+':
            Field.value.fset(self, value)
        else:
            raise ValueError('Phone must be in the format "+############" or "#########"')


class Address(Field):
    def __init__(self, value):
        super().__init__(value)

    @Field.value.setter
    def value(self, value):
        if len(value) > 0:
            Field.value.fset(self, value)
        else:
            raise ValueError('Address length must be greater than 0')


class Email(Field):
    def __init__(self, value):
        super().__init__(value)

    @Field.value.setter
    def value(self, value):
        user_name, email_box = value.split('@')
        if '@' not in value:
            raise ValueError('Email must contain the @ symbol')
        if len(user_name) <=1:
            raise ValueError('Length name in name@... must be more 1 symbol')
        Field.value.fset(self, value)


class Record:

    def __init__(self, name: Name, phone: Phone = None, birthday: Birthday = None, address: Address = None, email: Email = None):
        self.name: Name = name
        self.phone_list: list[Phone] = [phone] if phone is not None else []
        self.birthday: Birthday = birthday
        self.address: Address = address
        self.email: Email = email

    def __str__(self):
        result = f"{self.name.value}:"
        if len(self.phone_list) > 0:
            result += f" {', '.join(phone.value for phone in self.phone_list)};"
        if self.email is not None:
            result += f" e-mail: {self.email.value};"
        if self.address is not None:
            result += f" address: {self.address.value};"
        if self.birthday is not None:
            result += f" birthday: {self.birthday.value.strftime('%d.%m.%Y')};"
        result += '\n'
        return result

    def add_phone(self, phone: Phone):
        self.phone_list.append(phone)
        return 'Phone added.'

    def delete_phone(self, del_phone: Phone):
        try:
            for phone in self.phone_list:
                if phone.value == del_phone.value:
                    self.phone_list.remove(phone)
            return 'Number deleted successfully'
        except KeyError:
            return f'In field {self.name.value} there is no phone number to delete'
        except ValueError:
            return f'In field {self.name.value} there is no phone number to delete'

    def change_phone(self, old_phone: Phone, new_phone: Phone):
        try:
            self.delete_phone(old_phone)
            self.add_phone(new_phone)
            return 'Number changed successfully'
        except KeyError:
            return f'In field {self.name.value} there is no phone number to delete'

    def show_phone(self):
        return ' '.join([phone.value for phone in self.phone_list])

    def set_address(self, address: Address):
        self.address = address
        return 'Address added.'

    def set_email(self, email: Email):
        self.email = email
        return 'Email added.'

    def set_birthday(self, birthday: Birthday):
        self.birthday = birthday
        return 'Birthday added.'

    def days_to_birthday(self) -> int:
        if self.birthday is None:
            return None
        birthday = self.birthday.value
        try:
            birthday_this_year = birthday.replace(year=datetime.now().year)
            if birthday_this_year.date() < datetime.now().date():
                birthday_this_year = birthday_this_year.replace(year=datetime.now().year + 1)
            # processing on February 29 by increasing the date of the birthday by 1
        except ValueError:
            birthday += timedelta(days=1)
            birthday_this_year = birthday.replace(year=datetime.now().year)
            if birthday_this_year.date() < datetime.now().date():
                birthday_this_year = birthday_this_year.replace(year=datetime.now().year + 1)
        delta = birthday_this_year.date() - datetime.now().date()
        return delta.days


class AddressBook(UserDict):

    __path = Path('~').expanduser()
    __file_name = __path / 'contacts_book.pickle'
    __items_per_page = 20

    def __enter__(self):
        self.__load_book()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__save_book()

    def iterator(self, max_line: int = 5):
        result = ''
        count = 0
        total_count = 0
        for record in self.data.values():  # type: Record
            count += 1
            total_count += 1
            result = result + str(record)
            if count >= max_line or total_count >= len(self.data):
                yield result
                result = ''
                count = 0

    def save_book(self):
        self.__save_book()

    def add_record(self, name: Name, phone: Phone = None):
        if not (name.value in self.data.keys()):
            self.data[name.value] = Record(name=name, phone=phone)

    def del_record(self, name: Name):
        try:
            del self.data[name.value]
        except KeyError:
            raise ValueError('No record with that name')

    def edit_record(self, name: Name):
        if not (name.value in self.data.keys()):
            raise ValueError('No record with that name')

    def find_record(self, find_text: str):
        find_result = []
        for record in self.data.values():  # type: Record
            # find by name or phones
            if find_text.lower() in str(record.name.value).lower() or bool(list(filter(lambda x: find_text in x.value, record.phone_list))):
                find_result.append(record.name.value)
        if len(find_result) > 0:
            return f'Records where "{find_text}" were found: ' + ', '.join(find_result)
        return f'"{find_text}" matches not found'

    def show_record_with_birthday(self, day: int = 0):
        find_result = []
        for record in self.data.values():
            if int(record.days_to_birthday()) == int(day):
                find_result.append(record.name.value)
        if len(find_result) > 0:
            return f'Birthday records in {day} days: ' + ', '.join(find_result)
        return f'no records with birthdays after {day} days'

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
            print("Some problems! Don't save contact book")


if __name__ == '__main__':

    with AddressBook() as book:

        if len(book) == 0:
            print('Phone book is empty')
        try:
            max_line = 10
        except ValueError:
            max_line = len(book)
        result = 'Phone book:\n'
        num_page = 0
        for page in book.iterator(max_line=max_line):
            num_page += 1
            result += f'<< page {num_page} >>\n' if max_line < len(book) else ''
            result += page
        print(result)
