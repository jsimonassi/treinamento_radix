from datetime import datetime
import requests
from sqlalchemy import Column, Integer, DateTime, Float, ForeignKey, String
from common import Base
from constants import QUOTATION_API_URL
from models.Coin import Coin


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

    def as_dic(self):
        return {'id': self.id, 'coin_id': self.coinId, 'coin_value': self.coinValue, 'username': self.username,
                'created_at': self.createdAt, 'quoted_at': self.quotedAt, 'code_in': self.codeIn,
                'code_out': self.codeOut}

    @classmethod
    def get_quote_from_web(cls, session, start, end, code):
        coin = Coin.find_by_iso_cod(session, code)
        if coin:
            # Assumindo que é sempre BRL
            response = requests.get(QUOTATION_API_URL + 'daily/' + code + "-BRL" + '?start_date=' + start + '&end_date=' + end)
            map = response.json()[0]
            print(map)
            quoteDate = datetime.strptime(map['create_date'], '%Y-%m-%d %H:%M:%S')
            quote = QuoteHistory(coinId=coin.id, coinValue=map['bid'], codeIn=map['codein'], codeOut=map['code'],
                                 username='cache miss',
                                 createdAt=quoteDate)
            session.add(quote)
            session.commit()
            return [quote.as_dic()]
        return []

    @classmethod
    def get_all(cls, session):
        return session.query(QuoteHistory).all()

    @classmethod
    def get_quotes_by_date(cls, session, startDate, endDate, code):
        if startDate and endDate:
            startDateValue = datetime.strptime(startDate, '%d/%m/%Y')  # Ex: 29/06/2021
            endDateValue = datetime.strptime(endDate, '%d/%m/%Y')  # Ex: 29/06/2021
            return session.query(QuoteHistory).filter(QuoteHistory.createdAt > startDateValue) \
                .filter(QuoteHistory.createdAt < endDateValue).filter(QuoteHistory.codeOut == code).all()

        elif startDate:
            startDateValue = datetime.strptime(startDate, '%d/%m/%Y')
            return session.query(QuoteHistory).filter(QuoteHistory.createdAt > startDateValue).\
                filter(QuoteHistory.codeOut == code).all()

        elif endDate:
            endDateValue = datetime.strptime(endDate, '%d/%m/%Y')
            return session.query(QuoteHistory).filter(QuoteHistory.createdAt < endDateValue).\
                filter(QuoteHistory.codeOut == code).all()

        return session.query(QuoteHistory).filter(QuoteHistory.codeOut == code).all()
