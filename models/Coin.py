from sqlalchemy import Column, Integer, String
from common import Base


class Coin(Base):
    __tablename__ = 'coins'

    id = Column(Integer, primary_key=True)
    abbreviation = Column(String)
    isoCod = Column(String, unique=True)
    name = Column(String)

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            if key == 'id':
                self.id = value
            elif key == 'abbreviation':
                self.abbreviation = value
            elif key == 'isoCod':
                self.isoCod = value
            elif key == 'name':
                self.name = value

    def __repr__(self):
        return "Coin:'%s', isoCod='%s', abbreviation='%s', id='%d'" % (
            self.name, self.isoCod, self.abbreviation, self.id)

    def as_dic(self):
        return {'id': self.id, 'abbreviation': self.abbreviation, 'iso_cod': self.isoCod, 'name': self.name}

    @classmethod
    def find_by_name(cls, session, name):
        return session.query(Coin).filter_by(name=name).all()

    @classmethod
    def find_by_iso_cod(cls, session, iso_cod):
        print(iso_cod)
        return session.query(Coin).filter(Coin.isoCod == iso_cod).first()

    @classmethod
    def get_all(cls, session):
        return session.query(Coin).all()
