from sqlalchemy import and_, or_

from assistant.assistant.database.db import session
from assistant.assistant.database.models import Note, Tag, NoteTag
from sqlalchemy.sql.sqltypes import DateTime


def get_count():
    return session.query(Note).count()


def exist_note(title: str) -> bool:
    return session.query(Note).filter(Note.title == title).count()


# def exist_tag(name: str) -> bool:
#     return session.query(Tag).filter(Tag.name == name).count()


def get_note_by_num(num=0):
    note = session.query(Note).offset(num).limit(1).all()
    return note


def get_note_by_name(title):
    note = session.query(Note).filter(Note.title == title).first()
    return note


def create_note(title, description=None):
    note = Note(title=title, description=description)
    session.add(note)
    session.commit()
    return note


def update_note(title, description=None, add_text=False):
    note = session.query(Note).filter(Note.title == title).first()
    if add_text:
        description = note.description + '\n' + description
    note.description = description
    session.add(note)
    session.commit()
    return note


def create_tag(title_note: str, name: str):
    note = session.query(Note).filter(Note.title == title_note).first()
    tag = session.query(Tag).filter(Tag.name == name).first()
    if tag is None:
        tag = Tag(name=name)
        session.add(tag)
        session.commit()
    note_tag = NoteTag(note_id=note.id, tag_id=tag.id)
    session.add(note_tag)
    session.commit()


def remove_note(title):
    note = session.query(Note).filter(Note.title == title).first()
    for tag in note.tags:
        remove_tag(tag_name=tag.name, note_title=note.title)
    session.query(Note).filter(Note.title == title).delete()
    session.commit()


def remove_tag(tag_name: str, note_title: str):
    note = session.query(Note).filter(Note.title == note_title).first()
    tag = session.query(Tag).filter(Tag.name == tag_name).first()
    if session.query(NoteTag).filter(NoteTag.tag_id == tag.id).count() < 2:
        session.query(Tag).filter(Tag.name == tag.name).delete()
    session.query(NoteTag).filter(and_(NoteTag.tag_id == tag.id, NoteTag.note_id == note.id)).delete()
    session.commit()


def find_note(find_text: str):
    notes = session.query(Note).filter(or_(Note.title.like(f'%{find_text}%'), Note.description.like(f'%{find_text}%'))).all()
    return notes


def tags_all():
    return session.query(Tag).all()


def notes_all():
    return session.query(Note).all()


def find_note_by_tag(tag_name: str):
    if len(tag_name) > 0:
        tag = session.query(Tag).filter(Tag.name == tag_name).first()
        return tag.notes
    else:
        notes = session.query(Note).filter(Note.tags == None).all()
        return notes


if __name__ == '__main__':

    notes = session.query(Note).all()
    tags = find_tag('')
    for note_ in notes:
        print(note_.id, note_.tags)


