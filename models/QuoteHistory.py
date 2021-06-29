from sqlalchemy import Column, Integer, DateTime, Float, ForeignKey, String
from common import Base


class QuoteHistory(Base):
    __tablename__ = "quote_history"

    id = Column(Integer, primary_key=True)
    coinId = Column(Integer, ForeignKey('coins.id'))
    coinValue = Column(Float)
    username = Column(String)
    createdAt = Column(DateTime)
    quotedAt = Column(DateTime)
    codeIn = Column(String)
    codeOut = Column(String)

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            if key == 'id':
                self.id = value
            elif key == 'coinId':
                self.coinId = value
            elif key == 'coinValue':
                self.coinValue = value
            elif key == 'username':
                self.username = value
            elif key == 'createdAt':
                self.createdAt = value
            elif key == 'quotedAt':
                self.quotedAt = value
            elif key == 'codeIn':
                self.codeIn = value
            elif key == 'codeOut':
                self.codeOut = value

    def __repr__(self):
        return "QuoteHistory(id='%d', coinId='%d', coinValue='%f', username=%s, codeIn=%s, codeOut=%s)" % (
            self.id, self.coinId, self.coinValue, self.username, self.codeIn, self.codeOut)

    @classmethod
    def get_all(cls, session):
        return session.query(QuoteHistory).all()