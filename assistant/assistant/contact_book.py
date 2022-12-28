from collections import UserDict
from datetime import datetime, timedelta

from database import crud_contact


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
    def __init__(self, value):
        super().__init__(value)

    @Field.value.setter
    def value(self, value):
        if len(value) == 0:
            raise ValueError('Birthday length must be greater than 0')
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
    def __init__(self, value, verify=True):
        self.verify = verify
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
        elif not self.verify:
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
        if len(user_name) <= 1:
            raise ValueError('Length name in name@... must be more 1 symbol')
        Field.value.fset(self, value)


class Record:

    def __init__(self, name: Name = None, phone: Phone = None, birthday: Birthday = None, address: Address = None,
                 email: Email = None):
        self.name: Name = name
        self.email: Email = email
        self.phone_list: list[Phone] = [phone] if phone is not None else []
        self.birthday: Birthday = birthday
        self.address: Address = address
        self.id_ = self._get_id_()

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
        # result += '\n'
        return result

    def put_record_to_db(self):
        contact = crud_contact.create_contact(
            full_name=self.name.value,
            email=self.email.value,
            address=self.address.value,
            birthday=self.birthday.value
        )
        self.id_ = contact.id
        for phone in self.phone_list:
            crud_contact.create_phone(contact_id=contact.id, cell_phone=phone.value)

    def _get_id_(self):
        contact = crud_contact.get_contact_by_name(self.name.value if self.name is not None else None)
        if contact is not None:
            return contact.id
        else:
            return -1

    def exist_record(self):
        return False if self._get_id_() < 0 else True

    def get_record_from_db(self, num_contact: int = None):
        if self.id_ < 0:
            contact = crud_contact.get_contact_by_num(num=num_contact)[0]
        else:
            contact = crud_contact.get_contact_by_id(self.id_)
        self.extract_contact(contact)

    def extract_contact(self, contact):
        self.name = Name(contact.full_name)
        for phone in contact.phones:
            self.phone_list.append(Phone(phone.cell_phone, verify=False))
        if contact.email != "":
            self.email = Email(contact.email)
        if contact.address != "":
            self.address = Address(contact.address)
        if contact.birthday != "":
            str_date = contact.birthday.strftime('%d.%m.%Y')
            self.birthday = Birthday(str_date)

    def add_phone(self, new_phone: Phone):
        self.phone_list.append(new_phone)
        crud_contact.create_phone(contact_id=self.id_, cell_phone=new_phone.value)
        return 'Phone added.'

    def remove_phone(self, old_phone: Phone):
        try:
            for phone in self.phone_list:
                if phone.value == old_phone.value:
                    self.phone_list.remove(phone)
                    crud_contact.delete_phone(contact_id=self.id_, cell_phone=old_phone.value)
            return 'Number deleted successfully'
        except KeyError:
            return f'In field {self.name.value} there is no phone number to delete'
        except ValueError:
            return f'In field {self.name.value} there is no phone number to delete'

    def change_phone(self, old_phone: Phone, new_phone: Phone):
        try:
            self.remove_phone(old_phone)
            self.add_phone(new_phone)
            return 'Number changed successfully'
        except KeyError:
            return f'In field {self.name.value} there is no phone number to delete'

    def show_phone(self):
        return ' '.join([phone.value for phone in self.phone_list])

    def set_address(self, address: Address):
        self.address = address
        crud_contact.update_contact(id_=self.id_, address=address.value)
        return 'Address added.'

    def set_email(self, email: Email):
        self.email = email
        crud_contact.update_contact(id_=self.id_, email=email.value)
        return 'Email added.'

    def set_birthday(self, birthday: Birthday):
        self.birthday = birthday
        crud_contact.update_contact(id_=self.id_, birthday=birthday.value)
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

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    @staticmethod
    def iterator(max_line: int = 5):
        result = ''
        count = 0
        total_line_bd = crud_contact.get_count()
        for num_contact in range(total_line_bd):
            record = Record()
            record.get_record_from_db(num_contact=num_contact)
            count += 1
            result = result + str(record)
            if count >= max_line or num_contact >= total_line_bd-1:
                yield result
                result = ''
                count = 0

    @staticmethod
    def get_id_record(name: Name):
        contact = crud_contact.get_contact_by_name(name.value)
        if contact is not None:
            return contact.id
        else:
            return -1

    @staticmethod
    def add_record(name: Name, phone=None, address=None, email=None, birthday=None):
        record = Record(name=name, phone=phone, address=address, email=email, birthday=birthday)
        if record.exist_record():
            return f'Contact with the same name already exists: {str(record)}'
        record.put_record_to_db()
        return f'Add contact {str(record)}'

    # --------------------------
    @staticmethod
    def edit_record(operation: str, name: Name, new_phone: Phone = None, old_phone: Phone = None,
                    email: Email = None, address: Address = None, birthday: Birthday = None):
        record = Record(name)
        record.get_record_from_db()
        match operation:
            case '_add_phone':
                record.add_phone(new_phone=new_phone)
            case '_del_phone':
                record.remove_phone(old_phone=old_phone)
            case '_change_phone':
                record.change_phone(old_phone=old_phone, new_phone=new_phone)
            case '_add_email':
                record.set_email(email=email)
            case '_add_address':
                record.set_address(address=address)
            case '_add_birthday':
                record.set_birthday(birthday=birthday)
        return f'Edited contact {str(record)}'

    @staticmethod
    def remove_record(name: Name):
        contact = crud_contact.get_contact_by_name(full_name=name.value)
        crud_contact.remove_contact(contact.id)
        return f'Deleted contact {contact.full_name}'

    @staticmethod
    def find_record(find_text: str):
        contacts = crud_contact.find_contact(find_text=find_text)
        find_result = []
        for contact in contacts:
            record = Record()
            record.extract_contact(contact)
            find_result.append(str(record))
        if len(find_result) > 0:
            return f'Records where "{find_text}" were found:\n' + '\n'.join(find_result)
        return f'"{find_text}" matches not found'

    @staticmethod
    def show_record_with_birthday(day: int = 0):
        contacts = crud_contact.find_contact(find_text='')
        find_result = []
        for contact in contacts:
            record = Record()
            record.extract_contact(contact)
            if int(record.days_to_birthday()) == int(day):
                find_result.append(str(record))
        if len(find_result) > 0:
            return f'Birthday records in {day} days:\n' + '\n'.join(find_result)
        return f'no records with birthdays after {day} days'


if __name__ == '__main__':

    with AddressBook() as book:

        if crud_contact.get_count() == 0:
            print('Phone book is empty')

        # max_line = 7
        # result_ = 'Phone book:\n'
        # num_page = 0
        # for page in book.iterator(max_line=max_line):
        #     num_page += 1
        #     result_ += f'<< page {num_page} >>\n' if max_line < crud_contact.get_count() else ''
        #     result_ += page
        # print(result_)

        # r = book.add_record(name=Name('Misha_6'), phone=Phone('+380961234567'), address=Address('За углом'),
        #                 email=Email('qwerty@ukr.net'), birthday=Birthday('10.11.2000'))
        # print(r)
        # r = book.edit_record(name=Name('Misha_6'), operation='_del_phone', old_phone=Phone('+380501111111'))
        # print(r)

        # r = book.remove_record(name=Name('Misha_6'))
        # print(r)
        print(book.show_record_with_birthday(18))
