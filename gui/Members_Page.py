#import GUI package
import tkinter as tk
import matplotlib.pyplot as plt #for the figure
import numpy as np


class Members(tk.Frame):
    def __init__(self,parent,controller):
        super().__init__(parent,bg="#85A122")
        self.controller = controller