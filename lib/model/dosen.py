from sqlalchemy import Column, String, Integer
from lib.config.sqlalchemy import Base


class Dosen(Base):
    __tablename__ = 'dosen'

    id = Column('id', Integer, primary_key=True)
    nama = Column('nama', String(50))

    def __init__(self, id, nama):
        self.id = id
        self.nama = nama

    def __repr__(self):
        return "<Dosen(id='%s', nama='%s')>" % (self.id, self.nama)
