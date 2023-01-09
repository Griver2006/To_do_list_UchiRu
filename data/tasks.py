import sqlalchemy as sqla
from .db_session import SqlAlchemyBase


class Tasks(SqlAlchemyBase):
    __tablename__ = 'tasks'

    id = sqla.Column(sqla.Integer, primary_key=True, nullable=False)
    task_description = sqla.Column(sqla.String, nullable=False)
    category_id = sqla.Column(sqla.Integer, sqla.ForeignKey('categories.id'), nullable=True)
    date = sqla.Column(sqla.Date, nullable=False)
    finished = sqla.Column(sqla.Boolean, default=False)