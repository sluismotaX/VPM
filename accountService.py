from lib2to3.refactor import get_all_fix_names
from modulefinder import Module
import requests
import json
from sqlalchemy import *
from sqlalchemy.orm import *
import datetime
from models import *

url = "https://api.henrikdev.xyz/valorant/v1/mmr/na/"
engine = create_engine("postgresql+psycopg2://valorantAppClient:valclient@localhost:5432/valorant", echo=True, future=True)
Session = sessionmaker(engine)
session = Session()

def registerAccount(user,name, tag, password):
    urlAc = url+name+'/'+tag
    x = requests.get(urlAc)
    y = json.loads(x.text)
    if(y["status"]=="404"):
        return False
    else:
        account = Account()
        account.name = y["data"]["name"]
        account.tag = y["data"]["tag"]
        account.username = user
        account.password = password
        session.add(account)
        session.commit()
        return True

def getAccount(id):
    account = session.get(Account,id)
    return account

def getAccounts():
    return session.query(Account)

def updateData():
    accounts = getAccounts()
    for a in accounts:
        updateInfo(a)

def lastInfo(id):
    return session.query(AccountData).filter_by(account_id = id).order_by(desc(AccountData.date)).first()

def updateInfo(account):
    oldData = lastInfo(account.id)
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

