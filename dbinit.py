from unicodedata import name
from sqlalchemy import *
from sqlalchemy.orm import *

engine = create_engine("postgresql+psycopg2://valorantAppClient:valclient@localhost:5432/valorant", echo=True, future=True)

Base = declarative_base()

class Account(Base):
    __tablename__ = 'account'
    id = Column(Integer, primary_key=True)
    name = Column(String(30))
    tag = Column(String(10))
    username = Column(String(30))
    password = Column(String(128))

class AccountData(Base):
    __tablename__ = 'accountData'
    id = Column(Integer, primary_key=True)
    account_id = Column(Integer, ForeignKey('account.id'), nullable=False)
    account = relationship(Account)
    tier = Column(String(30))
    change = Column(String(3))
    elo = Column(String(10))
    date = Column(DateTime)
    update = Column(Boolean)

if __name__ == '__main__':
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    