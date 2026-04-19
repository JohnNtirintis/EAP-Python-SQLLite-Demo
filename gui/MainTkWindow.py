#import GUI package
import tkinter as tk
from SideBar_Menu import *

class MainWindowGUI(tk.Tk):

    #create main window
    def __init__(self, callback=None):
        super().__init__()

        #title & icon config
        self.title("Σύστημα Διαχείρισης Δανειστικής Βιβλιοθήκης")
        app_image = tk.PhotoImage(file= 'app_icon.png')
        self.iconphoto(False, app_image)

        #size config
        self.geometry("1280x720+300+150")
        self.minsize(1280,720)

        #grid config
        self.grid_columnconfigure(0, weight=0) #sidebar
        self.grid_columnconfigure(1, weight=1) #main content
        self.grid_rowconfigure(0, weight=1)

        #create main content frame
        self.main_content_frame = tk.Frame(self, bg="#D9D9D9")
        self.main_content_frame.grid(row=0, column=1, sticky = 'nsew')

        #create sidebar frame
        self.sidebar_frame = tk.Frame(self, width = 295, bg='#353535')
        self.sidebar_frame.grid(row=0,column=0, sticky = 'ns')
        self.sidebar_frame.grid_propagate(False)

        #call Sidebar_Menu.py
        self.sidebarwidgets = SideBar_Menu(self.sidebar_frame)

if __name__ == "__main__":
    app = MainWindowGUI()
    app.mainloop()