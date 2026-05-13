# ─── imports ─────────────────────────
import tkinter as tk
from tkinter import ttk
from gui.Styles import *


class Categories(tk.Frame):
    def __init__(self, parent,app, service = None):
        super().__init__(parent, bg=BG_MAIN)
        self.app   = app
        self.service = service

        #make Categories expand fully
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        #frame creation and grid config
        self.categories_frame = tk.Frame(
                            self,
                            bg = BG_MAIN,
                            padx=30,
                            pady=20
                            )
        self.categories_frame.grid(row=0,column=0, sticky='nswe')

        self.categories_frame.grid_propagate(False)
        self.categories_frame.grid_columnconfigure(0, weight=1)
        self.categories_frame.grid_columnconfigure(1, weight=0)
        self.categories_frame.grid_columnconfigure(2, weight=0)
        self.categories_frame.grid_rowconfigure(0, weight=0)
        self.categories_frame.grid_rowconfigure(1, weight=0)
        self.categories_frame.grid_rowconfigure(2, weight=0)
        self.categories_frame.grid_rowconfigure(3, weight=0)

        #back button icon
        self.back_btn_icon = tk.PhotoImage(file= 'gui/Assets/back_btn_icon.png')
        #back button
        back_btn = tk.Button(
                            self.categories_frame,
                            anchor='w',
                            compound='left',
                            image=self.back_btn_icon,
                            text='Κατάλογος Βιβλίων',
                            bd=0,
                            width=160,
                            padx=10,
                            bg= BG_MAIN,
                            activebackground=BG_MAIN,
                            activeforeground=FG_MUTED,
                            fg= FG_MUTED,
                            font= FONT_MAIN,
                            command= lambda: self.app.change_page("Κατάλογος Βιβλίων"),
                            cursor="hand2"
                            )
        back_btn.grid(row=0,column=0,padx=5,pady=(0,10),sticky='w')

        #title
        category_label = tk.Label(
            self.categories_frame,
            anchor='w',
            text="Προσθήκη Κατηγορίας",
            bd=0,
            bg=BG_MAIN,
            fg=FG_MUTED,
            font=FONT_TITLE
            )
        category_label.grid(row=1, column=0,padx=15, pady=(0,15), sticky='nsew')

        #container
        container = tk.Frame(
            self.categories_frame,
            bg = BG_CARD,
            height=200,
            padx=10,
            pady=10
            )
        container.grid(row=2, columnspan=3,column=0, padx=15, pady=30, sticky='nsew')
        container.grid_propagate(False)
        container.grid_columnconfigure(0, weight=1)
        container.grid_columnconfigure(1, weight=1)
        container.grid_rowconfigure(0, weight=0)
        container.grid_rowconfigure(1, weight=0)


        list_lbl = tk.Label(
                    container,
                    anchor = "ne",
                    text= "Κατηγορίες:",
                    bd = 0,
                    bg = BG_CARD,
                    fg= FG_MUTED,
                    font= FONT_SUBHEADER_BOLD
                    )
        list_lbl.grid(row=0, column=0, sticky='w',padx=(15,0),pady=(15,5))

        entry_lbl = tk.Label(
                    container,
                    anchor = "ne",
                    text= "Νέα Κατηγορία:",
                    bd = 0,
                    bg = BG_CARD,
                    fg= FG_MUTED,
                    font= FONT_SUBHEADER_BOLD
                    )
        entry_lbl.grid(row=0, column=1, sticky='w',padx=(15,0),pady=(15,5))

        #new category entry box
        self.new_category = ttk.Entry(
                    container,
                    font = FONT_MAIN,
                    style="CustomEntry.TEntry",
                    width=40,
                    exportselection=False,
                    validate='focusout'
                    )
        self.new_category.grid(row=1, column=1, sticky='w',padx=15,pady=5)

        #category list
        self.cat_list = ttk.Combobox(
                        container,
                        state="readonly",
                        font=FONT_MAIN,
                        width=40,
                        values=[],
                        style="CustomCombobox.TCombobox"
                        )
        self.cat_list.grid(row=1, column=0, sticky="w", padx=15, pady=5)
        self.cat_list.bind("<<ComboboxSelected>>",lambda e: self.selection_to_entry())
        self._load_categories()

        #buttons
        self.edit_btn = ttk.Button(
                        self.categories_frame,
                        text = "ΠΡΟΣΘΗΚΗ",
                        width=18,
                        style="CustomButton.TButton",
                        cursor= 'hand2'
                        )
        self.edit_btn.grid(row=3, column=0,sticky='e',padx=5,pady=5)

        self.delete_btn = ttk.Button(
                        self.categories_frame,
                        text = "ΔΙΑΓΡΑΦΗ",
                        width=18,
                        style="CustomButton.TButton",
                        cursor= 'hand2'
                        )
        self.delete_btn.grid(row=3, column=1, sticky='e',padx=5,pady=5)

        self.clear_btn = ttk.Button(
                        self.categories_frame,
                        text = "ΚΑΘΑΡΙΣΜΟΣ",
                        width=18,
                        style="CustomButton.TButton",
                        cursor= 'hand2',
                        command= self.clear_cb
                        )
        self.clear_btn.grid(row=3, column=2,sticky='e',padx=(5,15),pady=5)
    
    #=========================================
    #Combobox Selection to Entry function
    #=========================================
    def selection_to_entry(self):
        entry = self.new_category
        cat_list = self.cat_list
        
        #get selection items
        selected = cat_list.get()

        #clear entry box
        entry.delete(0,'end')
        #insert list item to entry box
        entry.insert(0,selected)

        #change btn text
        self.edit_btn.config(text="ΕΝΗΜΕΡΩΣΗ")
    #=========================================
    #Clear Combobox Selection
    #=========================================
    def clear_cb(self):
        self.cat_list.set('')
        self.cat_list.select_clear()
        self.new_category.delete(0,'end')
        self.edit_btn.config(text="ΠΡΟΣΘΗΚΗ")

    #=========================================
    #Reset Content on Page Change
    #=========================================
    def reset(self):
        self.new_category.delete(0,'end')
        self.edit_btn.config(text="ΠΡΟΣΘΗΚΗ")
        self.clear_cb()
        self._load_categories()

    def _category_labels(self, categories):
        labels = []
        for c in categories or []:
            if isinstance(c, dict):
                name = c.get("name")
            else:
                name = getattr(c, "name", None)
            if name:
                labels.append(name)
        return labels

    def _load_categories(self):
        if not self.service:
            self.cat_list["values"] = []
            return
        labels = self._category_labels(self.service.list_categories())
        self.cat_list["values"] = labels
        if labels:
            self.cat_list.current(0)
