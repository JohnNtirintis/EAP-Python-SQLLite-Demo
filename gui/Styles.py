# styles.py
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

def setup_styles():
    style = ttk.Style()

    # Theme
    style.theme_use("clam")

    #Treeview
    style.configure("Custom.Treeview",
        background= BG_CARD,
        foreground= FG_DARK_BODY,
        rowheight=30,
        fieldbackground=BG_CARD,
        font=FONT_BOLD
        )
        
    style.configure("Custom.Treeview.Heading",
        font=FONT_TITLE,
        background="#EAEAEA",
        foreground="#5E5E5E",
        relief='flat'
        )
        
    style.layout('Custom.Treeview',
        [('Custom.Treeview.treearea', {'sticky': 'nsew'})]
        )
    
    #Scrollbar
    style.configure(
        "Dashboard.Vertical.TScrollbar",
        background=SIDEBAR_FG,
        troughcolor=BG_CARD,
        bordercolor=SIDEBAR_FG,
        arrowcolor = SIDEBAR_BG_DARK,
        gripcount=0,
        relief="flat",
        bd=0,
        width=5,
        lightcolor = SIDEBAR_FG,
        darkcolor = SIDEBAR_FG
        )
    
    style.map(
        "Dashboard.Vertical.TScrollbar",
        background=[
        ("active", SIDEBAR_FG),
        ("pressed", SIDEBAR_FG)]
        )
