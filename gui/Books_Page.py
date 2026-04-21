#import GUI package
import tkinter as tk
import matplotlib.pyplot as plt #for the figure
import numpy as np


class Books(tk.Frame):
    def __init__(self,parent,controller):
        super().__init__(parent,bg="#22A12D")
        self.controller = controller