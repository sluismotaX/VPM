from array import array
from logging import root
from msilib.schema import CustomAction
from re import L
from textwrap import fill
from tkinter.tix import COLUMN
from turtle import bgcolor, color, width
import accountService
from functools import partial
#---------------------------------------Visual------------------------------------------------------------------------

import tkinter
import tkinter.messagebox
import customtkinter

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"


class App(customtkinter.CTk):

    WIDTH = 1024
    HEIGHT = 520

    def __init__(self):
        super().__init__()
        self.title("Valorant Account Manager")
        self.geometry(f"{App.WIDTH}x{App.HEIGHT}")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)  # call .on_closing() when app gets closed

        accountService.updateData()
        # ========================

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.frame_left = customtkinter.CTkFrame(master=self,
                                                 width=180,
                                                 corner_radius=0)
        self.frame_left.grid(row=0, column=0, sticky="nswe")

        self.frame_right = customtkinter.CTkFrame(master=self)
        self.frame_right.grid(row=0, column=1, sticky="nswe", padx=20, pady=20)

        canvas = customtkinter.CTkCanvas(self.frame_right)

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

        scrollbar = customtkinter.CTkScrollbar(self.frame_right,orientation="vertical",command=canvas.yview)
        scrollbar.pack(side="right", fill="y")    
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)

        # ============ frame_info ============

        frameGroup = []
        index = 0

        for a in accountService.getAccounts():
            scrollable = customtkinter.CTkFrame(canvas)
            scrollable.bind(
                "<Configure>", 
                lambda e: canvas.configure(
                    scrollregion=canvas.bbox("all")
                )
            )

            canvas.create_window((0, index*100), window=scrollable, anchor="nw")

            labelTName = customtkinter.CTkLabel(master = scrollable, text="Nombre")
            labelTName.grid(row =0, column =0)
            

            labelVName = customtkinter.CTkLabel(master = scrollable, text=a.name)
            labelVName.grid(row=1, column =0)

            labelTTag = customtkinter.CTkLabel(master = scrollable, text="Tag")
            labelTTag.grid(row =0, column =1)

            labelVTag = customtkinter.CTkLabel(master = scrollable, text=a.tag)
            labelVTag.grid(row =1, column =1)

            lastData = accountService.lastInfo(a.id)

            labelTRank = customtkinter.CTkLabel(master = scrollable, text="Rank")
            labelTRank.grid(row =0, column =2)

            rank = lastData.tier + " ("+ lastData.elo+")"

            labelVRank = customtkinter.CTkLabel(master = scrollable, text= rank)
            labelVRank.grid(row =1, column =2) 

            labelTUsername = customtkinter.CTkLabel(master = scrollable, text="Username")
            labelTUsername.grid(row =0, column = 3)

            labelVUsername = customtkinter.CTkLabel(master = scrollable, text=a.username)
            labelVUsername.grid(row =1, column =3)

            labelTPassword = customtkinter.CTkLabel(master = scrollable, text="Password")
            labelTPassword.grid(row =0, column = 4)

            labelVPassword = customtkinter.CTkLabel(master = scrollable, text=a.password)
            labelVPassword.grid(row =1, column =4)

            button_1 = customtkinter.CTkButton(master=scrollable,
                                                text="Copiar",
                                                command=copy(a.p))
            button_1.grid(row=1, column=5)



            index +=1




        # ============ frame_right ==========
        
        self.optionmenu_1.set("Light")


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

