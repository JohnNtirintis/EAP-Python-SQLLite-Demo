#import GUI package
import tkinter as tk
from tkinter import ttk

# ─── colour & font constants (match all other pages) ─────────────────────────
BG_MAIN = "#D9D9D9"
BG_CARD = "#EAEAEA"
SIDEBAR_BG_DARK = "#353535"
SIDEBAR_BG_DARKER = "#242424"
SIDEBAR_BG_HIGHLIGHT = "#282828"
SIDEBAR_FG_HIGHLIGHT = "#00D5E4"
SIDEBAR_FG = "#CCCCCC"
FG_DARK_BODY = "#1E1E1E"
FG_MUTED_HEADERS = "#5E5E5E"
BUTTON_BG = "#059CA7"
FONT_MAIN  = ("Segoe UI", 12)
FONT_BOLD  = ("Segoe UI", 12, "bold")
FONT_TITLE = ("Segoe UI", 18)
FONT_SMALL = ("Segoe UI", 10)


class SideBar_Menu(tk.Frame):
    def __init__(self,parent, page_select):
        super().__init__(parent)
        self.frame = parent
        self.default_active_btn_txt = "Αρχική"
        self.active_menu_btn = None
        self.page_select = page_select

        # make Sidebar expand fully
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)


        #sidebar user label
        self.sidebar_bg_image = tk.PhotoImage(file= 'menu_bg_image.png')
        self.sidebar_lbl = tk.Label(
                            self.frame,
                            anchor = "center",
                            bg=SIDEBAR_BG_DARK,               #match container
                            fg="#FFFFFF",
                            bd=0,
                            font = FONT_BOLD,
                            image = self.sidebar_bg_image,
                            compound = "center",
                            text = "Διαχειριστής"
                            )
        self.sidebar_lbl.pack()
        
        #sidebar title label
        self.sidebar_title_lbl = tk.Label(
                            self.frame,
                            anchor = "w",
                            bg=SIDEBAR_BG_DARKER,
                            fg=SIDEBAR_FG,
                            bd=0,
                            padx=20,
                            pady=10,
                            font = FONT_MAIN,
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
        for i, text in enumerate(menu_buttons):
           self.create_menu_button(text)

    #create sidebar_menu_buttons function
    def create_menu_button(self,text):
        
        menu_btn = tk.Button(
                            self.frame,
                            anchor = "w",
                            text = text,
                            bg=SIDEBAR_BG_DARK,
                            activebackground=SIDEBAR_BG_HIGHLIGHT,
                            fg=SIDEBAR_FG,
                            activeforeground=SIDEBAR_FG_HIGHLIGHT,
                            bd=0,
                            highlightthickness=0,
                            padx=20,
                            pady=20,
                            command=lambda: self.on_click(menu_btn),
                            font= FONT_MAIN,
                            cursor="hand2"
                            )
        menu_btn.pack(fill=tk.X)

        #change btn colours
        menu_btn.bind("<Enter>",lambda e: self.on_hover(menu_btn))
        menu_btn.bind("<Leave>",lambda e: self.on_leave(menu_btn))

        #default active btn
        if text == self.default_active_btn_txt:
            self.on_click(menu_btn)

        return menu_btn
    
    #change colour on hover
    def on_hover(self,btn):
        if btn != self.active_menu_btn:
            btn.config(bg=SIDEBAR_BG_HIGHLIGHT,fg=SIDEBAR_FG_HIGHLIGHT)

    #revert colour on hover exit 
    def on_leave(self,btn):
        if btn != self.active_menu_btn:
            btn.config(bg=SIDEBAR_BG_DARK,fg=SIDEBAR_FG)
    
    #change colour on btn click
    def on_click(self,btn):
        #reset previous active btn
        if self.active_menu_btn is not None:
            self.active_menu_btn.config(bg=SIDEBAR_BG_DARK,fg=SIDEBAR_FG)
        
        #set new active btn
        btn.config(bg=SIDEBAR_BG_HIGHLIGHT,fg=SIDEBAR_FG_HIGHLIGHT)
        self.active_menu_btn = btn

        #get page name
        self.page_select(btn.cget("text"))





