from faker import Faker

from assistant.assistant.database.models import Note
from assistant.assistant.database.db import session

fake = Faker('ru-RU')
count_notes = 20


def create_note():
    for _ in range(count_notes):
        note = Note(
            title=fake.sentence(nb_words=2),
            description=fake.paragraph(nb_sentences=3, variable_nb_sentences=False),
            created=fake.date_between(start_date="-2y")
        )
        session.add(note)
    session.commit()


if __name__ == '__main__':
    create_note()
    session.close()
