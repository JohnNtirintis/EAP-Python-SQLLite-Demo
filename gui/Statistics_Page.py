#import GUI package
import tkinter as tk
import matplotlib.pyplot as plt #for the figure
import numpy as np


class Statistics(tk.Frame):
    def __init__(self,parent,controller):
        super().__init__(parent,bg="#4822A1")
        self.controller = controller