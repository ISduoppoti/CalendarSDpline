import json
import tkinter as tk
import customtkinter as ctk
from datetime import datetime
from calendar import monthrange

class UICalendar():
    def __init__(self, root, year, month):
        self.root = root
        self.year = year
        self.month = month

        self.frame_main = ctk.CTkFrame(self.root, fg_color= 'transparent')
        self.frame_main.pack(expand= True)

        self.label_date = ctk.CTkLabel(self.frame_main,
                                       text= f'{self.year}-{self.month}-...',
                                       corner_radius= 8)
        self.label_date.grid(row = 0, column= 1)

        self.arrow_left = ctk.CTkButton(self.frame_main,
                                        text= '<',
                                        width= 30,
                                        fg_color = 'transparent',
                                        border_width= 1,
                                        border_color= '#2FA572',
                                        corner_radius= 8,
                                        command= lambda: self.prepare_date(-1))
        self.arrow_left.grid(row= 1, column= 0, sticky='nsew')

        self.framecalendar = ctk.CTkFrame(self.frame_main, fg_color= 'transparent')
        self.framecalendar.grid(row = 1, column = 1)

        self.arrow_right = ctk.CTkButton(self.frame_main,
                                         text= '>',
                                         width= 30,
                                         fg_color = 'transparent',
                                         border_width= 1,
                                         border_color= '#2FA572',
                                         corner_radius= 8,
                                         command= lambda: self.prepare_date(1))
        self.arrow_right.grid(row= 1, column= 2, sticky='nsew')

        self.get_calendar()


    def get_days(self, year, month):
        return monthrange(year, month)[1]
    

    def on_press(self, c):
        self.btns_list[c].configure(border_color= 'red')
        self.data[str(self.year)][str(self.month)][c] = 1

        with open("data.json",'w+') as file:
            json.dump(self.data, file, indent=4)


    def prepare_date(self, step):
        if step == 1:
            if self.month == 12:
                self.year += 1
                self.month = 1
            else:
                self.month += 1
        else: #if step == -1
            if self.month == 1:
                self.year -= 1
                self.month = 12
            else:
                self.month -= 1

        for btn in self.btns_list:
            btn.grid_forget()

        self.label_date.configure(text= f'{self.year}-{self.month}-...')

        self.get_calendar()


    def get_calendar(self):

        self.load_json()

        self.btns_list = []

        for i in range(self.get_days(self.year, self.month)):
            row = i // 6

            self.btns_list.append(ctk.CTkButton(self.framecalendar,
                                   text= i+1,
                                   width= 130,
                                   height= 60,
                                   fg_color= 'transparent',
                                   border_width= 1,
                                   border_color= '#2A654B',
                                   command= lambda c=i: self.on_press(c)))
            self.btns_list[i].grid(row= row, column= i - (row * 6), padx = 3, pady = 3)

        try:
            for i, btn in enumerate(self.btns_list):
                if self.data[str(self.year)][str(self.month)][i] == 1:
                    btn.configure(border_color = 'red')
                else: None

        except KeyError:
            print('CREATING A NEW YEAR!!!!!!!!@#@#@#@#@#@#@')
            self.complete_json()


    def load_json(self):
        with open('data.json', 'r') as file:
            self.data = json.load(file)


    def complete_json(self):
        from objdict import ObjDict

        help_data = ObjDict()

        for i in range(12):
            help_data[str(i+1)] = [0 for _ in range(self.get_days(self.year, i+1))]

            new_data = ObjDict(self.data)

            new_data[str(self.year)] = help_data

        with open("data.json",'w+') as file:
            json.dump(new_data, file, indent=4)


def main():
    ctk.set_default_color_theme('green')

    root = ctk.CTk()
    root.geometry('900x500')
    root.resizable(0, 0)
    

    UICalendar(root, datetime.now().year, datetime.now().month)

    root.mainloop()

main()