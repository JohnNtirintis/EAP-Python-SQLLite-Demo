# styles.py
import tkinter as tk
from tkinter import ttk

# ─── colour & font constants (match all other pages) ─────────────────────────
BG_MAIN = "#D9D9D9"
BG_CARD = "#EAEAEA"
BG_DARK = "#353535"
BG_DARKER = "#242424"
BG_BLACK_ACCENT = "#282828"
ACCENT = "#00D5E4"
FG_LIGHT = "#CCCCCC"
FG_DARK = "#1E1E1E"
FG_MUTED = "#5E5E5E"
ACCENT_DARK = "#059CA7"
FONT_MAIN  = ("Segoe UI", 12)
FONT_BOLD  = ("Segoe UI", 12, "bold")
FONT_TITLE = ("Segoe UI", 18)
FONT_SMALL = ("Segoe UI", 10)
FONT_SUBHEADER = ("Segoe UI", 14)
FONT_SUBHEADER_BOLD = ("Segoe UI", 14, 'bold')

# ── Chart palette (light-mode friendly) ──────────────────────────────
CHART_COLORS = [
    "#01696f", "#00D5E4", "#da7101", "#437a22",
    "#006494", "#7a39bb", "#a12c7b", "#a13544",
    "#d19900", "#0c4e54", "#2e5c10", "#275f8e",
]

# ── Matplotlib surfaces (light theme) ────────────────────────────────
MPL_BG   = BG_CARD
MPL_GRID = "#C8C8C8" 
MPL_TEXT = FG_MUTED

def setup_styles():
    style = ttk.Style()

    # Theme
    style.theme_use("clam")

    #Treeview
    style.configure("Custom.Treeview",
        background= BG_CARD,
        foreground= FG_DARK,
        rowheight=30,
        fieldbackground=BG_CARD,
        font=FONT_BOLD
        )
    
    style.map(
        "Custom.Treeview",
        background=[('selected', ACCENT_DARK)]
        )
        
    style.configure("Custom.Treeview.Heading",
        font=FONT_SUBHEADER,
        background=BG_CARD,
        foreground=FG_MUTED,
        relief='flat'
        )
        
    style.layout('Custom.Treeview',
        [('Custom.Treeview.treearea', {'sticky': 'nsew'})]
        )
    
    #Scrollbar
    style.configure(
        "Vertical.TScrollbar",
        background=FG_LIGHT,
        troughcolor=BG_CARD,
        bordercolor=FG_LIGHT,
        arrowcolor = BG_DARK,
        gripcount=0,
        relief="flat",
        bd=0,
        width=5,
        lightcolor = FG_LIGHT,
        darkcolor = FG_LIGHT
        )
    
    style.map(
        "Vertical.TScrollbar",
        background=[
        ("active", FG_LIGHT),
        ("pressed", FG_LIGHT)]
        )
    
    style.configure(
        "Horizontal.TScrollbar",
        background=FG_LIGHT,
        troughcolor=BG_CARD,
        bordercolor=FG_LIGHT,
        arrowcolor = BG_DARK,
        gripcount=0,
        relief="flat",
        bd=0,
        width=5,
        lightcolor = FG_LIGHT,
        darkcolor = FG_LIGHT
        )
    
    style.map(
        "Horizontal.TScrollbar",
        background=[
        ("active", FG_LIGHT),
        ("pressed", FG_LIGHT)]
        )
    
    #entries
    style.configure("CustomEntry.TEntry",
                    padding=5,
                    fg=FG_DARK,
                    selectbackground=ACCENT,
                    selectforeground=FG_DARK,
                    bd=0,
                    relief='flat'
                    )
    
    style.map(
        "CustomEntry.TEntry",
        bg=[
            ("focus", BG_CARD),
            ("!focus", BG_CARD),
            ("disabled", FG_MUTED)],
        bordercolor=[
            ("focus", ACCENT),
            ("!focus", BG_DARK),
            ("disabled", FG_MUTED),
            ("invalid", "#a13544")]
    )
    
    #buttons
    style.configure("CustomButton.TButton",
                    padding=8,
                    font = FONT_BOLD,
                    background=ACCENT_DARK,
                    foreground=FG_DARK,
                    relief='flat'
                    )
    
    style.map(
        "CustomButton.TButton",
        background=[
        ("disabled", FG_MUTED),
        ("pressed", ACCENT_DARK),
        ("active", ACCENT_DARK)],
        foreground=[
        ("disabled", FG_LIGHT),]
        )