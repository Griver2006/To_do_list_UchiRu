import sqlalchemy as sqla
from sqlalchemy.orm import relationship
from .db_session import SqlAlchemyBase


class Categories(SqlAlchemyBase):
    __tablename__ = 'categories'

    id = sqla.Column(sqla.Integer, primary_key=True, nullable=False)
    name = sqla.Column(sqla.String, nullable=False)
    tasks = relationship('Tasks', backref='goal')