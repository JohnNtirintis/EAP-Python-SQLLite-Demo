#import GUI package
import tkinter as tk
from SideBar_Menu import *
from Dashboard import Dashboard
from Books_Page import Books
from Statistics_Page import Statistics
from Loans_Page import Loans
from Members_Page import Members

class MainWindowGUI(tk.Tk):

    #create main window
    def __init__(self):
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
        self.main_content_frame.grid_rowconfigure(0,weight=1)
        self.main_content_frame.grid_columnconfigure(0,weight=1)

        #create sidebar frame
        self.sidebar_frame = tk.Frame(self, width = 295, bg='#353535')
        self.sidebar_frame.grid(row=0,column=0, sticky = 'ns')
        self.sidebar_frame.grid_propagate(False)

        #empty dictionary for pages
        self.pages = {}

        #page mapping dictionary - links title txt to class
        self.page_map = {
            "Αρχική": Dashboard,
            "Κατάλογος Βιβλίων": Books,
            "Δανεισμός Βιβλίων": Loans,
            "Στατιστικά": Statistics,
            "Μέλη": Members
            }
        
        #creates instances for each page and saves in dictionary
        for P in (Dashboard,Books,Loans,Statistics,Members):
            page_instance = P(self.main_content_frame, self)
            self.pages[P] = page_instance
            page_instance.grid(row=0,column=0,sticky='nsew')

        #create Sidebar
        self.sidebar = SideBar_Menu(self.sidebar_frame,self.change_page)
        
        #default starting page
        self.change_page("Αρχική")

    #change page function
    def change_page(self, page_name):
        target_page = self.page_map.get(page_name)
        frame = self.pages[target_page]
        frame.tkraise()

if __name__ == "__main__":
    app = MainWindowGUI()
    app.mainloop()