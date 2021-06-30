from fastapi import FastAPI
from typing import Optional
from models.Coin import Coin
from models.QuoteHistory import QuoteHistory
from main import session

app = FastAPI()


@app.get("/coins")
def get_coins():
    response = []
    for coin in Coin.get_all(session=session):
        response.append(coin.as_dic())
    return response


@app.get("/quotes")
def get_quotes(start: Optional[str] = None, end: Optional[str] = None, code_out: Optional[str] = None):
    response = []
    for quote in QuoteHistory.get_quotes_by_date(session=session, startDate=start, endDate=end, code=code_out):
        response.append(quote.as_dic())
    if len(response) <= 0: #Cache miss
        response = QuoteHistory.get_quote_from_web(session=session, start='20180901', end='20180930', code='USD')
    return response
