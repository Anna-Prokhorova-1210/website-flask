import sqlalchemy
from .db_session import SqlAlchemyBase


users_to_books = sqlalchemy.Table(
    'users_to_books',
    SqlAlchemyBase.metadata,
    sqlalchemy.Column('users', sqlalchemy.Integer,
                      sqlalchemy.ForeignKey('users.id')),
    sqlalchemy.Column('books', sqlalchemy.Integer,
                      sqlalchemy.ForeignKey('books.id'))
)


class Book(SqlAlchemyBase):
    __tablename__ = 'books'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    letter = sqlalchemy.Column(sqlalchemy.String, nullable=True)
