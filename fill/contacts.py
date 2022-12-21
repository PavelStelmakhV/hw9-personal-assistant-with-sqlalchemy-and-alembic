from faker import Faker

from assistant.assistant.database.models import Contact, Note, Tag, NoteTag
from assistant.assistant.database.db import session


fake = Faker('ru-RU')
count_contact = 20


def create_contact():
    for _ in range(count_contact):
        contact = Contact(
            full_name=fake.name(),
            email=fake.email(),
            cell_phone=fake.phone_number(),
            address=fake.street_address(),
            birthday=fake.date_between(start_date="-50y", end_date='-15y')
        )
        session.add(contact)
    session.commit()


if __name__ == '__main__':
    create_contact()
