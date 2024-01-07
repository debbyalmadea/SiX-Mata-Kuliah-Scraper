from sqlalchemy import Column, String, Integer
from lib.config.sqlalchemy import Base

dosen_count = 0


class Dosen(Base):
    __tablename__ = 'dosen'

    id = Column('id', Integer, primary_key=True)
    nama = Column('nama', String(50))

    def __init__(self, nama, id=None):
        global dosen_count
        self.id = id
        if id is None:
            dosen_count += 1
            self.id = dosen_count
        self.nama = nama

    def __repr__(self):
        return "<Dosen(id='%s', nama='%s')>" % (self.id, self.nama)
