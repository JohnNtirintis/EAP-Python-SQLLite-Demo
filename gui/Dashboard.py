#import GUI package
import tkinter as tk
import matplotlib.pyplot as plt #for the figure
import numpy as np


class Dashboard(tk.Frame):
    def __init__(self,parent,controller):
        super().__init__(parent,bg="#D9D9D9")
        self.controller = controller

        #frame creation and grid config 
        self.overallData_frame = tk.Frame(
                            self,
                            bg = "#D9D9D9",
                            padx = 30,
                            pady = 30
                            )
        self.overallData_frame.grid(row=0, column=0, sticky='nsew')
        
        self.overallData_frame.grid_columnconfigure(0, weight=1)
        self.overallData_frame.grid_columnconfigure(1, weight=1)
        self.overallData_frame.grid_columnconfigure(2, weight=1)
        self.overallData_frame.grid_rowconfigure(1, weight=1)
        self.overallData_frame.grid_rowconfigure(2, weight=1)

        #images
        self.books_icon = tk.PhotoImage(file= 'books_icon.png')
        self.loaned_books_icon = tk.PhotoImage(file= 'loaned_books_icon.png')
        self.members_icon = tk.PhotoImage(file= 'members_icon.png')
        
        #data info list
        overalll_data_info = [(self.books_icon,"Συνολικά Βιβλία",235),
                            (self.members_icon,"Συνολικά Μέλη",75),
                            (self.loaned_books_icon,"Δανεισμένα Βιβλία",17)]
        
        #create loop of data info with corresponding img/text/value
        for col, (img,item,value) in enumerate(overalll_data_info):
            self.create_overall_card(col,item,img,value)
        

    #create  overall data function
    def create_overall_card(self,col,text,icon,value):
        
        #container
        container = tk.Frame(
                    self.overallData_frame,
                    bg = "#EAEAEA",
                    width=280,
                    height=80,
                    )
        container.grid(row=0, column=col, padx=15, pady=10, sticky='nsew')
        
        #container grid config
        container.grid_columnconfigure(0, weight=1)
        container.grid_columnconfigure(1, weight=1)
        container.grid_rowconfigure(0, weight=1)
        container.grid_rowconfigure(1, weight=1)
        container.grid_propagate(False)
        
        #create icon
        data_icon = tk.Label(
                    container,
                    anchor = "w",
                    image= icon,
                    bg = "#EAEAEA"
                    )
        
        data_icon.grid(row=0,rowspan=2, column=0, sticky='w', padx=(20,5))

        #create text label
        data_lbl = tk.Label(
                    container,
                    anchor = "ne",
                    text= text,
                    bd = 0,
                    bg = "#EAEAEA",
                    fg= "#5E5E5E",
                    font=("Segoe UI",14)
                    )
        data_lbl.grid(row=0, column=1, sticky='e', padx=(0,20), pady=(10,0))

        #create value label
        data_value = tk.Label(
                    container,
                    anchor = "ne",
                    text= value,
                    bd = 0,
                    bg = "#EAEAEA",
                    fg= "#1E1E1E",
                    font=("Segoe UI",20)
                    )
        data_value.grid(row=1, column=1, sticky='e', padx=(0,20), pady=(0,10))

    # def create_figure(self):  
    #     plt.title(label='Δανεισμοί',
    #             fontdict={'fontsize': ['20']},
    #             loc='left',
    #             y=1.0,
    #             pad=5
    #             )