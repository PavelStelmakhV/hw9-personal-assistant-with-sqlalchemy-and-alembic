from faker import Faker

from assistant.assistant.database.models import Tag
from assistant.assistant.database.db import session

fake = Faker('ru-RU')
count_tags = 10


def create_tags():
    for _ in range(count_tags):
        tag = Tag(
            name=fake.word()
        )
        session.add(tag)
    session.commit()


if __name__ == '__main__':
    create_tags()
    session.close()

