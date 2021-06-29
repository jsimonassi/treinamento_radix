from sqlalchemy import create_engine
from common import Base
from sqlalchemy.orm import sessionmaker
from models.Coin import Coin
from models.QuoteHistory import QuoteHistory
from datetime import datetime
import requests
from Constants import QUOTATION_API_URL

Session = sessionmaker()


def convertCoinToReal(user, coin):  # Isso deveria converter um determinado valor? Ou só obter a cotação?
    response = requests.get(QUOTATION_API_URL + coin.isoCod + "-BRL")
    map = response.json()[coin.isoCod + 'BRL']
    quote = QuoteHistory(coinId=coin.id, coinValue=map['bid'], codeIn=map['codein'], codeOut=map['code'], username=user,
                         createdAt=datetime.now())
    session.add(quote)
    session.commit()
    return quote.coinValue


def convertRealToCoin(user, coin):
    response = requests.get(QUOTATION_API_URL + "BRL-" + coin.isoCod)
    map = response.json()['BRL' + coin.isoCod]
    quote = QuoteHistory(coinId=coin.id, coinValue=map['bid'], codeIn=map['codein'], codeOut=map['code'], username=user,
                         createdAt=datetime.now())
    session.add(quote)
    session.commit()
    return quote.coinValue


if __name__ == "__main__":

    engine = create_engine('sqlite:///database.sqlite', echo=False)
    Base.metadata.create_all(engine)
    Session.configure(bind=engine)
    session = Session()

    while True:
        print("\nConverter moeda(X) para real --------- 1")
        print("Converter real para moeda (X) -------- 2")
        print("Adicionar moeda ---------------------- 3")
        print("Ler histórico de cotações------------- 4")
        print("Sair --------------------------------- 0")
        opt = int(input("Escolha uma opção: "))

        if opt == 1:
            currentCoins = Coin.get_all(session)
            if len(currentCoins) <= 0:
                print("Nenhuma moeda encontrada!")
            else:
                for i in range(len(currentCoins)):
                    print(str(currentCoins[i]) + "--------------- " + str(i))
                index = int(input("Escolha uma moeda: "))
                username = input("\nQual o seu nome?")
                print(convertCoinToReal(username, currentCoins[index]))

        elif opt == 2:
            currentCoins = Coin.get_all(session)
            if len(currentCoins) <= 0:
                print("Nenhuma moeda encontrada!")
            else:
                for i in range(len(currentCoins)):
                    print(str(currentCoins[i]) + "--------------- " + str(i))
                index = int(input("Escolha uma moeda: "))
                username = input("\nQual o seu nome?")
                print(convertRealToCoin(username, currentCoins[index]))

        elif opt == 3:
            newCoin = Coin()
            newCoin.name = input("Nome da moeda: ")
            newCoin.isoCod = input("isoCod (Ex: BRL): ")
            newCoin.abbreviation = input("abbreviation (Ex: R$): ")
            session.add(newCoin)
            session.commit()

        elif opt == 4:
            quotes = QuoteHistory.get_all(session)
            for qt in quotes:
                print(qt)

        else:
            break
