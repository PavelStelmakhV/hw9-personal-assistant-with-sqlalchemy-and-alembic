from sqlalchemy import and_

from assistant.assistant.database.db import session
from assistant.assistant.database.models import Contact


def create_contact(full_name, email, cell_phone, address, birthday):
    contact = Contact(full_name=full_name, email=email, cell_phone=cell_phone, address=address, birthday=birthday)
    session.add(contact)
    session.commit()


def get_contact(full_name):
    contact = session.query(Contact).filter(Contact.full_name == full_name).all()
    return contact


def update_phone(full_name, old_phone, new_phone=''):
    todo = session.query(Contact).filter(and_(Contact.full_name == full_name, Contact.cell_phone == old_phone))
    todo.update({'cell_phone': new_phone, 'description': description})
    session.commit()
    return todo.first()


def remove_contact(full_name):
    contact = session.query(Contact).filter(Contact.full_name == full_name)
    contact.delete()
    session.commit()
    return contact
