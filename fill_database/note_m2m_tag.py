import random

from assistant.assistant.database.models import Note, Tag, NoteTag
from assistant.assistant.database.db import session


def create_relationship():
    notes = session.query(Note).all()
    tags = session.query(Tag).all()

    for tag in tags:
        note = random.choice(notes)
        rel = NoteTag(tag_id=tag.id, note_id=note.id)
        session.add(rel)
    session.commit()


if __name__ == '__main__':
    create_relationship()
    session.close()

