#import GUI package
import tkinter as tk
import matplotlib.pyplot as plt #for the figure
import numpy as np
import math

# ─── colour & font constants (match all other pages) ─────────────────────────
BG_MAIN    = "#D9D9D9"
BG_CARD    = "#EAEAEA"
BG_DARK    = "#353535"
BG_DARKER  = "#282828"
ACCENT     = "#00D5E4"
ACCENT2    = "#E47B00"
ACCENT3    = "#7BE400"
FG_LIGHT   = "#CCCCCC"
FG_DARK    = "#1E1E1E"
FG_MUTED   = "#5E5E5E"
FONT_MAIN  = ("Segoe UI", 12)
FONT_BOLD  = ("Segoe UI", 12, "bold")
FONT_TITLE = ("Segoe UI", 16, "bold")
FONT_SMALL = ("Segoe UI", 10)
FONT_KPI   = ("Segoe UI", 26, "bold")
FONT_KPI_S = ("Segoe UI", 11)

# palette for bar / pie charts (canvas-drawn)
CHART_COLORS = [
    "#00D5E4", "#E47B00", "#7BE400", "#D400E4",
    "#E4D400", "#0062E4", "#E40062", "#00E462",
]



class Statistics(tk.Frame):
    def __init__(self,parent,controller):
        super().__init__(parent,bg="#4822A1")
        self.controller = controller
