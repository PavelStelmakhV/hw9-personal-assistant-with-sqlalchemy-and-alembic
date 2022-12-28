from sqlalchemy import and_, or_

from assistant.assistant.database.db import session
from assistant.assistant.database.models import Contact, Phone
from sqlalchemy.sql.sqltypes import DateTime


def get_count():
    return session.query(Contact).count()


def get_contact_by_num(num=0):
    contact = session.query(Contact).offset(num).limit(1).all()
    return contact


def get_contact_by_name(full_name):
    contact = session.query(Contact).filter(Contact.full_name == full_name).first()
    return contact


def get_contact_by_id(id_: int):
    return session.query(Contact).get(id_)


def create_contact(full_name, email=None, address=None, birthday=None):
    contact = Contact(full_name=full_name, email=email, address=address, birthday=birthday)
    session.add(contact)
    session.commit()
    return contact


def create_phone(contact_id: int, cell_phone: str):
    phone = Phone(cell_phone=cell_phone, contact_id=contact_id)
    session.add(phone)
    session.commit()


def delete_phone(contact_id: int, cell_phone: str):
    phone = session.query(Phone).filter(and_(Phone.cell_phone == cell_phone, Phone.contact_id == contact_id)).first()
    session.delete(phone)
    session.commit()

# ----------------------------------------------------------------------------------


def update_contact(id_: int, email: str = None, address: str = None, birthday: DateTime = None):
    contact = session.query(Contact).get(id_)
    if email is not None:
        contact.email = email
    if address is not None:
        contact.address = address
    if birthday is not None:
        contact.birthday = birthday
    session.add(contact)
    session.commit()
    return contact


def remove_contact(contact_id: int):
    session.query(Contact).filter(Contact.id == contact_id).delete()
    session.query(Phone).filter(Phone.contact_id == contact_id).delete()
    session.commit()


def find_contact(find_text: str):
    contact = session.query(Contact).filter(Contact.full_name.like(f'%{find_text}%')).all()
    return contact


if __name__ == '__main__':
    # contacts = session.query(Contact).offset(0).limit(0).all()
    # contacts = session.query(Contact).filter(Contact.full_name == 'Misha_6').first()
    # print(contacts.id)
    # for c in contacts:
    #     print(f'{c.full_name}, {c.email}, {[t.cell_phone for t in c.phones]}')
    print(find_contact(''))

