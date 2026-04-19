#import GUI package
import tkinter as tk
from tkinter import ttk

class SideBar_Menu:
    def __init__(self,frame):
        self.frame = frame
        self.default_active_btn_txt = "Αρχική"
        self.active_menu_btn = None

        #sidebar user label
        self.sidebar_bg_image = tk.PhotoImage(file= 'menu_bg_image.png')
        self.sidebar_lbl = tk.Label(
                            self.frame,
                            anchor = "center",
                            bg='#353535',               #match container
                            fg="#FFFFFF",
                            bd=0,
                            font = ("Segoe UI",12, "bold"),
                            image = self.sidebar_bg_image,
                            compound = "center",
                            text = "Διαχειριστής"
                            )
        self.sidebar_lbl.pack()
        
        #sidebar title label
        self.sidebar_title_lbl = tk.Label(
                            self.frame,
                            anchor = "w",
                            bg='#242424',
                            fg="#CCCCCC",
                            bd=0,
                            padx=20,
                            pady=10,
                            font = ("Segoe UI",12),
                            text = "ΜΕΝΟΥ ΠΛΟΗΓΗΣΗΣ"
                            )
        self.sidebar_title_lbl.pack(fill=tk.X)

        #menu buttons' text
        menu_buttons = ['Αρχική',
                        'Κατάλογος Βιβλίων',
                        'Δανεισμός Βιβλίων',
                        'Στατιστικά',
                        'Μέλη']

        #menu buttons creation with correct txt
        for i, item in enumerate(menu_buttons):
            btn_text = self.create_menu_button(frame, item)


    #create sidebar_menu_buttons function
    def create_menu_button(self,parent, text):
        
        menu_btn = tk.Button(
                            self.frame,
                            anchor = "w",
                            text = text,
                            bg="#353535",
                            activebackground="#282828",
                            fg="#CCCCCC",
                            activeforeground="#00D5E4",
                            bd=0,
                            highlightthickness=0,
                            padx=20,
                            pady=20,
                            font= ("Segoe UI",12),
                            cursor="hand2"
                            )
        menu_btn.pack(fill=tk.X)

        #change hover colours
        menu_btn.bind("<Enter>",lambda e: self.on_hover(menu_btn))
        menu_btn.bind("<Leave>",lambda e: self.on_leave(menu_btn))
        menu_btn.bind("<Button-1>",lambda e: self.on_click(menu_btn))

        #default active btn
        if text == self.default_active_btn_txt:
            self.on_click(menu_btn)

        return menu_btn
    
    #change colour on hover
    def on_hover(self,btn):
        if btn != self.active_menu_btn:
            btn.config(bg="#282828",fg="#00D5E4")

    #revert colour on hover exit 
    def on_leave(self,btn):
        if btn != self.active_menu_btn:
            btn.config(bg="#353535",fg="#CCCCCC")
    
    #change colour on btn click
    def on_click(self,btn):
        #reset previous active btn
        if self.active_menu_btn is not None:
            self.active_menu_btn.config(bg="#353535",fg="#CCCCCC")
        
        #set new active btn
        btn.config(bg="#282828",fg="#00D5E4")
        self.active_menu_btn = btn





