# ─── imports ─────────────────────────
import tkinter as tk
from tkinter import ttk
from gui.Styles import *
from gui.SideBar_Menu import *
from gui.Dashboard_Page import Dashboard
from gui.Books_Page import Books
from gui.Statistics_Page import Statistics
from gui.Loans_Page import Loans
from gui.Members_Page import Members
from gui.Recommend_Page import Recommend
from gui.Rating_Page import Rating
from gui.Categories_Page import Categories
from gui.Book_Edit_Page import BookEdit


class MainTkWindow(tk.Tk):

    #=========================================
    #Main window
    #=========================================
    def __init__(self, service):
        super().__init__()
        self.service = service

        #title & icon config
        self.title("Σύστημα Διαχείρισης Δανειστικής Βιβλιοθήκης")
        app_image = tk.PhotoImage(file= 'gui/Assets/app_icon.png')
        self.iconphoto(False, app_image)

        #style
        setup_styles()


        #size config
        self.geometry("1440x840+200+50")
        self.minsize(1280,720)

        #grid config
        self.grid_columnconfigure(0, weight=0) #sidebar
        self.grid_columnconfigure(1, weight=1) #main content
        self.grid_rowconfigure(0, weight=1)

        #make all widgets focusable except buttons
        self.bind_all(
            "<Button-1>",
            lambda e: None
            if isinstance(e.widget, (tk.Button, ttk.Button))
            else e.widget.focus_set() if hasattr(e.widget, "focus_set") else None,
        )

        #create main content frame
        self.main_content_frame = tk.Frame(self, bg=BG_MAIN)
        self.main_content_frame.grid(row=0, column=1, sticky = 'nsew')
        self.main_content_frame.grid_rowconfigure(0,weight=1)
        self.main_content_frame.grid_columnconfigure(0,weight=1)

        #create sidebar frame
        self.sidebar_frame = tk.Frame(self, width = 295, bg=BG_DARK)
        self.sidebar_frame.grid(row=0,column=0, sticky = 'nsew')
        self.sidebar_frame.grid_propagate(False)

        #empty dictionary for pages
        self.pages = {}

        #page mapping dictionary - links title txt to class
        self.page_map = {
            "Αρχική": Dashboard,
            "Κατάλογος Βιβλίων": Books,
            "Δανεισμός Βιβλίων": Loans,
            "Στατιστικά": Statistics,
            "Μέλη": Members,
            "Πρόταση Βιβλίου" : Recommend,
            "Βαθμολογία" : Rating,
            "Κατηγορίες" : Categories,
            "Επεξεργασία Βιβλίου" : BookEdit,

            }
        
        #creates instances for each page and saves in dictionary
        for P in (Dashboard, Books, Categories, BookEdit, Loans, Rating, Statistics, Members, Recommend):
            if P in (Statistics, Categories, Books): # TODO: We might need to pass more files here. Unsure, needs testing - John
                page_instance = P(self.main_content_frame, self, service=self.service)
            else:
                page_instance = P(self.main_content_frame, self)
            self.pages[P] = page_instance
            page_instance.grid(row=0,column=0,sticky='nsew')

        #create Sidebar
        self.sidebar = SideBar_Menu(self.sidebar_frame,self.change_page)
        
        #default starting page
        self.change_page("Αρχική")

    #=========================================
    #Change_Page function
    #=========================================
    def change_page(self, page_name):
        target_page = self.page_map.get(page_name)
        frame = self.pages[target_page]
        frame.reset()
        frame.tkraise()
