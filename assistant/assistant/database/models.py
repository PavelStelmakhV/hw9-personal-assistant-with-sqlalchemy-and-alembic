from sqlalchemy import Column, Integer, String, ForeignKey, Date, Table
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import DateTime
from datetime import datetime

from assistant.assistant.database.db import Base


class Contact(Base):
    __tablename__ = 'contacts'
    id = Column(Integer, primary_key=True)
    full_name = Column(String(120), nullable=False)
    email = Column('email', String(100))
    address = Column('address', String(100))
    birthday = Column('birthday', Date)
    phones = relationship('Phone', back_populates='contact')


class Phone(Base):
    __tablename__ = 'phones'
    id = Column(Integer, primary_key=True)
    cell_phone = Column('cell_phone', String(100))
    contact_id = Column('contact_id', ForeignKey('contacts.id', ondelete='CASCADE'))
    contact = relationship('Contact', back_populates='phones')


class Note(Base):
    __tablename__ = 'notes'
    id = Column(Integer, primary_key=True)
    title = Column(String(250), nullable=False)
    description = Column(String(500), nullable=False)
    created = Column(DateTime, default=datetime.now())
    tags = relationship('Tag', secondary='notes_to_tags', back_populates='notes')


class Tag(Base):
    __tablename__ = 'tags'
    id = Column(Integer, primary_key=True)
    name = Column(String(25), nullable=False, unique=True)
    notes = relationship('Note', secondary='notes_to_tags', back_populates='tags')


class NoteTag(Base):
    __tablename__ = 'notes_to_tags'
    id = Column(Integer, primary_key=True)
    note_id = Column('note_id', ForeignKey('notes.id', ondelete='CASCADE'))
    tag_id = Column('tag_id', ForeignKey('tags.id', ondelete='CASCADE'))


