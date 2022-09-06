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


#---------------------------------------Visual------------------------------------------------------------------------

import tkinter
import tkinter.messagebox
import customtkinter

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

class App(customtkinter.CTk):

    WIDTH = 780
    HEIGHT = 520

    def __init__(self):
        super().__init__()
        self.title("Valorant Account Manager")
        self.geometry(f"{App.WIDTH}x{App.HEIGHT}")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)  # call .on_closing() when app gets closed

        # ========================

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.frame_left = customtkinter.CTkFrame(master=self,
                                                 width=180,
                                                 corner_radius=0)
        self.frame_left.grid(row=0, column=0, sticky="nswe")

        self.frame_right = customtkinter.CTkFrame(master=self)
        self.frame_right.grid(row=0, column=1, sticky="nswe", padx=20, pady=20)

        # ============ frame_left ============

        self.frame_left.grid_rowconfigure(0, minsize=10)   # empty row with minsize as spacing
        self.frame_left.grid_rowconfigure(5, weight=1)  # empty row as spacing
        self.frame_left.grid_rowconfigure(8, minsize=20)    # empty row with minsize as spacing
        self.frame_left.grid_rowconfigure(11, minsize=10)  # empty row with minsize as spacing

        self.label_1 = customtkinter.CTkLabel(master=self.frame_left,
                                              text="Usuario",
                                              text_font=("Roboto Medium", -16))  # font name and size in px
        self.label_1.grid(row=1, column=0, pady=10, padx=10)

        self.button_1 = customtkinter.CTkButton(master=self.frame_left,
                                                text="Registrar",
                                                command=self.register)
        self.button_1.grid(row=2, column=0, pady=10, padx=20)

        self.label_mode = customtkinter.CTkLabel(master=self.frame_left, text="Appearance Mode:")
        self.label_mode.grid(row=9, column=0, pady=0, padx=20, sticky="w")

        self.optionmenu_1 = customtkinter.CTkOptionMenu(master=self.frame_left,
                                                        values=["Light", "Dark", "System"],
                                                        command=self.change_appearance_mode)
        self.optionmenu_1.grid(row=10, column=0, pady=10, padx=20, sticky="w")

        # ============ frame_right ============

        self.frame_right.rowconfigure((0, 1, 2, 3), weight=1)
        self.frame_right.rowconfigure(7, weight=10)
        self.frame_right.columnconfigure((0, 1), weight=1)
        self.frame_right.columnconfigure(2, weight=0)

        self.frame_info = customtkinter.CTkFrame(master=self.frame_right)
        self.frame_info.grid(row=0, column=0, columnspan=2, rowspan=4, pady=20, padx=20, sticky="nsew")

        # ============ frame_info ============

        self.frame_info.rowconfigure(0, weight=1)
        self.frame_info.columnconfigure(0, weight=1)

        self.label_info_1 = customtkinter.CTkLabel(master=self.frame_info,
                                                   text="CTkLabel: Lorem ipsum dolor sit,\n" +
                                                        "amet consetetur sadipscing elitr,\n" +
                                                        "sed diam nonumy eirmod tempor" ,
                                                   height=100,
                                                   corner_radius=6,  # <- custom corner radius
                                                   fg_color=("white", "gray38"),  # <- custom tuple-color
                                                   justify=tkinter.LEFT)
        self.label_info_1.grid(column=0, row=0, sticky="nwe", padx=15, pady=15)

        self.progressbar = customtkinter.CTkProgressBar(master=self.frame_info)
        self.progressbar.grid(row=1, column=0, sticky="ew", padx=15, pady=15)

        # ============ frame_right ==========
        
        self.optionmenu_1.set("Dark")

    def button_event(self):
        print("Button pressed")

    def change_appearance_mode(self, new_appearance_mode):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def on_closing(self, event=0):
        self.destroy()

    def register(self):
        register = Register()
        register.mainloop()


class Register(customtkinter.CTk):

    WIDTH = 350
    HEIGHT = 300

    def __init__(self):
        super().__init__()
        self.title("Account Registration")
        self.geometry(f"{Register.WIDTH}x{Register.HEIGHT}")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)  

    def on_closing(self, event=0):
        self.destroy()



if __name__ == "__main__":
    app = App()
    app.mainloop()

