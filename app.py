import requests
import json
from sqlalchemy import *
from sqlalchemy.orm import *
from dbinit import *
import datetime

url = "https://api.henrikdev.xyz/valorant/v1/mmr/na/"
engine = create_engine("postgresql+psycopg2://valorantAppClient:valclient@localhost:5432/valorant", echo=True, future=True)
Session = sessionmaker(engine)
session = Session()


def registerAccount(user,name, tag, password):
    urlAc = url+name+'/'+tag
    x = requests.get(urlAc)
    y = json.loads(x.text)
    if(y["status"]=="404"):
        return false
    account = Account()
    account.name = y["data"]["name"]
    account.tag = y["data"]["tag"]
    account.username = user
    account.password = password
    session.add(account)
    session.commit()
    return true

def getAccount(id):
    account = session.get(Account,id)
    return account

def updateData():
    accounts = session.query(Account)
    for a in accounts:
        updateInfo(a)


def updateInfo(account):
    oldData = session.query(AccountData).filter_by(account_id = account.id).order_by(desc(AccountData.date)).first()
    if(oldData is not None):
        oldData.update = True
        session.add(oldData)
    name = account.name
    tag = account.tag
    urlAc = url+name+'/'+tag
    x = requests.get(urlAc)
    y = json.loads(x.text)
    if(y["status"]=="404"):
        return false
    accountData = AccountData()
    accountData.account_id = account.id
    accountData.date = datetime.datetime.now()
    accountData.update = False
    accountData.elo = y["data"]["elo"]
    accountData.tier = y["data"]["currenttierpatched"]
    accountData.change = y["data"]["mmr_change_to_last_game"]
    session.add(accountData)
    session.commit()
    return true
    
def getRank(playerData):
    y = json.loads(playerData)
    print(y["data"]["currenttierpatched"])

updateData()




