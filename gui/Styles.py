# styles.py

#Use this single universal import block on every page

#from gui.styles import (
#    BG_MAIN, BG_CARD, BG_FILTER, BG_DARK, BG_DARKER,
#    ACCENT, FG_LIGHT, FG_DARK, FG_MUTED,
#    FONT_MAIN, FONT_BOLD, FONT_TITLE, FONT_SEC, FONT_SMALL,
#    FONT_TREE, FONT_THEAD, FONT_CRUMB,
#    CHART_COLORS, MPL_BG, MPL_GRID, MPL_TEXT,
#)

import tkinter as tk
from tkinter import ttk

# ─── colour & font constants (match all other pages) ─────────────────────────
BG_MAIN = "#D9D9D9"
BG_CARD = "#EAEAEA"
BG_FILTER = "#CFCFCF"         
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
FONT_SEC   = ("Segoe UI", 13, "bold")    
FONT_TREE  = ("Segoe UI", 11)            
FONT_THEAD = ("Segoe UI", 11, "bold")    
FONT_CRUMB = ("Segoe UI", 10)            

# ── Chart palette (light-mode friendly) ──────────────────────────────
CHART_COLORS = [                         # ← new: statistics charts
    "#01696f", "#00D5E4", "#da7101", "#437a22",
    "#006494", "#7a39bb", "#a12c7b", "#a13544",
    "#d19900", "#0c4e54", "#2e5c10", "#275f8e",
]

# ── Matplotlib surfaces (light theme) ────────────────────────────────
MPL_BG   = "#EAEAEA"                     # ← new
MPL_GRID = "#C8C8C8"                     # ← new
MPL_TEXT = "#1E1E1E"                     # ← new

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

# ── Short aliases so all GUI pages use consistent names ──────────────
BG_DARK   = SIDEBAR_BG_DARK
BG_DARKER = SIDEBAR_BG_HIGHLIGHT
ACCENT    = SIDEBAR_FG_HIGHLIGHT
FG_LIGHT  = SIDEBAR_FG
FG_DARK   = FG_DARK_BODY
FG_MUTED  = FG_MUTED_HEADERS
