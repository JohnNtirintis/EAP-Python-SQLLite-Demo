# ─── imports ─────────────────────────
import tkinter as tk
from tkinter import ttk
from gui.Styles import *
from gui.Loans_Page import add_placeholder_var,remove_placeholder_var,search_results
from gui.Dashboard_Page import autosize_content
from gui.Book_Edit_Page import BookEdit

class Books(tk.Frame):
    def __init__(self, parent, app, service = None):
        super().__init__(parent, bg=BG_MAIN)
        self.app = app
        self.service = service

        #make Books page expand fully
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        #frame creation and grid config 
        self.books_frame = tk.Frame(
                    self,
                    bg = BG_MAIN,
                    padx = 30,
                    pady = 20
                    )
        self.books_frame.grid(row=0,column=0,sticky='nsew')

        self.books_frame.grid_rowconfigure(0, weight=0)
        self.books_frame.grid_rowconfigure(1, weight=0)
        self.books_frame.grid_rowconfigure(2, weight=1)
        self.books_frame.grid_columnconfigure(0, weight=0)
        self.books_frame.grid_columnconfigure(1, weight=1)
        self.books_frame.grid_columnconfigure(2, weight=0)
        self.books_frame.grid_columnconfigure(3, weight=0)

        #page title 
        books_catalog_label = tk.Label(
                            self.books_frame,
                            anchor='w',
                            text='Κατάλογος Βιβλίων',
                            bd=0,
                            bg= BG_MAIN,
                            fg= FG_MUTED,
                            font= FONT_TITLE
                            )
        books_catalog_label.grid(row=0,column=0,padx=15, pady=(5,10), sticky='nsew')

        #searchbar
        self.searchbar_book_var = tk.StringVar()
        self.searchbar_book = ttk.Entry(
                    self.books_frame,
                    font = FONT_MAIN,
                    style="CustomEntry.TEntry",
                    width=50,
                    exportselection=False,
                    textvariable=self.searchbar_book_var
                    )
        self.searchbar_book.grid(row=1, columnspan=2,column=0, sticky='w',padx=(15,10),pady=15)

        #default searchbar text
        self.searchbar_book_var.set("Αναζήτηση...")

        #default change on focus in/out
        self.searchbar_book.bind("<FocusIn>", lambda e: remove_placeholder_var(self.searchbar_book_var))
        self.searchbar_book.bind("<FocusOut>", lambda e: add_placeholder_var(self.searchbar_book_var))

        self.booksdata = self._load_books()

        #show filtered results based on query
        self.searchbar_book.bind("<Return>", lambda e: search_results(self.booksdata,self.searchbar_book_var,
                                                                    self.books_table))
        
        #add category button
        self.add_cat_button = ttk.Button(
                        self.books_frame,
                        text = "ΠΡΟΣΘΗΚΗ ΚΑΤΗΓΟΡΙΑΣ",
                        width=22,
                        style="CustomButton.TButton",
                        command= lambda: self.app.change_page("Κατηγορίες"),
                        cursor= 'hand2'
                        )
        self.add_cat_button.grid(row=1, column=2,sticky='e',padx=10,pady=15)

        #add/edit book button
        self.book_button = ttk.Button(
                        self.books_frame,
                        width=20,
                        text="ΠΡΟΣΘΗΚΗ ΒΙΒΛΙΟΥ",
                        style="CustomButton.TButton",
                        cursor= 'hand2',
                        command=lambda: self.app.change_page("Επεξεργασία Βιβλίου")
                        )
        self.book_button.grid(row=1, column=3, sticky='e',padx=(5,15),pady=15)

        self.SORT_OPTIONS = ["Αύξουσα σειρά", "Φθίνουσα σειρά"]
        self.sort_var = tk.StringVar(value=self.SORT_OPTIONS[0])
        self.cat_vars: dict[str, tk.BooleanVar] = {}
        self.book_catalog()
        self.book_catalog_filter()

    #=========================================
    #Book Catalog Filter function
    #=========================================  
    def book_catalog_filter(self):
        #container
        container = tk.Frame(
                    self.books_frame,
                    bd=0,
                    bg= BG_CARD,
                    width=100,
                    padx=15,
                    pady=10
                    )
        container.grid(row=2, column=0, padx=15, pady=10, sticky='nsew')
        container.grid_propagate(False)
        container.grid_rowconfigure(0, weight=0)
        container.grid_rowconfigure(1, weight=0)
        container.grid_rowconfigure(2, weight=0)
        container.grid_columnconfigure(0, weight=1)

        #title
        filter_title_lbl = tk.Label(
                        container,
                        anchor = "center",
                        bg=BG_CARD,
                        fg=FG_MUTED,
                        bd=0,
                        font = FONT_SUBHEADER,
                        text = "Φίλτρα Αναζήτησης"
                        )
        filter_title_lbl.grid(row=0,column=0,sticky='w',pady=(10,20))

        #sorting
        sort_container = tk.Frame(
                    container,
                    bg= BG_CARD
                    )
        sort_container.grid(row=1, column=0, pady=10, sticky='nsew')
        sort_container.grid_rowconfigure(0,weight=0)
        sort_container.grid_rowconfigure(1,weight=0)
        sort_container.grid_columnconfigure(0,weight=0)

        sorting_lbl = tk.Label(
                        sort_container,
                        anchor = "center",
                        bg=BG_CARD,
                        fg=FG_MUTED,
                        bd=0,
                        font = FONT_BOLD,
                        text = "Ταξινόμηση κατά"
                        )
        sorting_lbl.grid(row=0,column=0,sticky='w',pady=10)

        sort_menu = ttk.Combobox(
                    sort_container,
                    textvariable= self.sort_var,
                    values= self.SORT_OPTIONS,
                    state='readonly',
                    style="CustomCombobox.TCombobox",
                    width=18
                    )
        sort_menu.grid(row=1,column=0,sticky="nswe", ipady=3, pady=5)

        #category filter
        cat_container = tk.Frame(
                    container,
                    bg= BG_CARD
                    )
        cat_container.grid(row=2, column=0, pady=10, sticky='nsew')
        cat_container.grid_columnconfigure(0,weight=0)
        cat_container.grid_columnconfigure(1,weight=0)
        cat_container.grid_rowconfigure(0,weight=0)

        cat_lbl = tk.Label(
                        cat_container,
                        anchor = "center",
                        bg=BG_CARD,
                        fg=FG_MUTED,
                        bd=0,
                        font = FONT_BOLD,
                        text = "Κατηγορία"
                        )
        cat_lbl.grid(row=0,column=0,sticky='w',padx=(0,5),pady=10)

        self.arrow_up = tk.PhotoImage(file='gui/Assets/arrow_up.png')
        self.arrow_down = tk.PhotoImage(file='gui/Assets/arrow_down.png')
        self.cat_arrow = tk.Label(
                        cat_container,
                        anchor = "center",
                        bg=BG_CARD,
                        bd=0,
                        image= self.arrow_down
                        )
        self.cat_arrow.grid(row=0,column=1, sticky='w',padx=5,pady=10)
        self.cat_expanded = False
        #call toggle funtion
        self.cat_arrow.bind("<Button-1>", lambda e: self.cat_toggle())

        #checkboxes
        self.checkboxes_container = tk.Frame(
                                    container,
                                    bg= BG_CARD,
                                    padx=10
                                    )
        self.checkboxes_container.grid(row=3,column=0,sticky='nsew')

    #=========================================
    #Categories Toggle Visibility
    #=========================================
    def cat_toggle(self):
        #if expanded
        if self.cat_expanded ==True:
            self.checkboxes_container.grid_remove()
            self.cat_arrow.config(image= self.arrow_down)
            self.cat_expanded = False
        #if not expanded
        else:
            self.refresh_category_checkboxes()
            self.checkboxes_container.grid()
            self.cat_arrow.config(image= self.arrow_up)
            self.cat_expanded = True

    #=========================================
    #Category Checkboxes
    #=========================================
    def refresh_category_checkboxes(self):
        #clear chckboxes
        for w in self.checkboxes_container.winfo_children():
            w.destroy()

        self.cats = self.service.list_categories() if self.service else []
        #keep checked boxes
        old  = {k: v.get() for k, v in self.cat_vars.items()}
        self.cat_vars = {}

        for c in self.cats:
            if isinstance(c, dict):
                name = c.get("name")
            else:
                name = getattr(c, "name", None)
            if not name:
                continue
            var  = tk.BooleanVar(value=old.get(name, False))
            self.cat_vars[name] = var
            checkbox = ttk.Checkbutton(
                self.checkboxes_container, 
                text=name,
                variable=var,
                style= "CustomCheckbox.TCheckbutton",
                # command=self.apply_filters()
                )
            checkbox.pack(fill="x", pady=1)

    #=========================================
    #Book Catalog Table function
    #=========================================
    def book_catalog(self):
        #container
        container = tk.Frame(
                    self.books_frame,
                    bd=0,
                    bg= BG_CARD,
                    padx=10,
                    pady=10
                    )
        container.grid(row=2, columnspan=3, column=1, padx=(5,15), pady=10, sticky='nsew')
        container.grid_propagate(False)
        container.grid_rowconfigure(0, weight=1)
        container.grid_rowconfigure(1, weight=0)
        container.grid_columnconfigure(0, weight=1)
        container.grid_columnconfigure(1, weight=0)

        #table
        columns=("ID","Τίτλος βιβλίου","Συγγραφέας","Έτος έκδοσης","ISBN","Κατηγορία","Απόθεμα","Βαθμολογία")
        self.books_table = ttk.Treeview(
                            container,
                            columns=columns,
                            show="headings",
                            selectmode='browse',
                            style="Custom.Treeview"
                            )
        self.books_table.grid(row=0, column=0, sticky='nsew',padx=(15,5),pady=(0,5))
        self.books_table.bind("<<TreeviewSelect>>", self.update_book_button_state)
        self.books_table.bind("<FocusOut>", lambda e: self.reset())
       
        #vertical scrollbar
        v_scrollbar = ttk.Scrollbar(
                        container, 
                        orient='vertical',
                        command=self.books_table.yview,
                        style="Vertical.TScrollbar"
                        )
        v_scrollbar.grid(row=0, column=1, sticky='ns')
        self.books_table.config(yscrollcommand=v_scrollbar.set)

        #horizontal scrollbar
        h_scrollbar = ttk.Scrollbar(
                        container, 
                        orient='horizontal',
                        command=self.books_table.xview,
                        style="Horizontal.TScrollbar"
                        )
        h_scrollbar.set(0.2,0.5)
        h_scrollbar.grid(row=1, column=0, sticky='we',padx=(15,0))
        self.books_table.config(xscrollcommand=h_scrollbar.set)

        for col in columns:
            self.books_table.heading(col, text=col, anchor='w')
            self.books_table.column(col, 
                                anchor="w", 
                                width=120 if col != "ID" else 80, 
                                minwidth=150 if col != "ID" else 80,
                                stretch=True if col != "ID" else False)

        self.populate_data(self.booksdata)

    #=========================================
    #Populate Data function
    #=========================================
    def populate_data(self,books):
        self.books_table.delete(*self.books_table.get_children())
        
        rev   = self.sort_var.get() == self.SORT_OPTIONS[1]
        books = sorted(books,
                       key=lambda b: (b.get("title") or "").lower(),
                       reverse=rev)
        
        for i, b in enumerate(books):
            avail      = int(b.get("available_copies", 0))
            total      = int(b.get("total_copies", 0))
            copies_str = f"{avail}/{total} τμχ"
            rat        = b.get("avg_rating") or b.get("rating")
            rat_str    = f"{rat}/5" if rat else "—"

            self.books_table.insert("", "end", iid=str(b["id"]),
                                values=(
                                 f"{b['id']:04d}",
                                 b.get("title", ""),
                                 b.get("author", ""),
                                 b.get("published_year", ""),
                                 b.get("isbn", ""),
                                 b.get("category_name", ""),
                                 copies_str,
                                 rat_str,)
                                )
    
        #call autosizing function
        autosize_content(self.books_table)
    
    #=========================================
    #Update Button Text on Selection function
    #=========================================
    def update_book_button_state(self, event=None):
        selected = self.books_table.selection()
        if not selected:
            self.book_button.config(text="ΠΡΟΣΘΗΚΗ ΒΙΒΛΙΟΥ")
        else:
            self.book_button.config(text="ΕΝΗΜΕΡΩΣΗ ΒΙΒΛΙΟΥ")

    #=========================================
    #Edit Book Button prefill function
    #=========================================
    # def edit_book(self):
    #     item = self.books_table.selection()[0]
    #     values = self.books_table.item(item,"values")

    #     book_id, title, author, year, isbn, category_name, copies_str, rating = values

    #     # copies_str = "2/5 τμχ"
    #     available, total = copies_str.split()[0].split("/")
    #     total = int(total)

    #     self.selected_values = {
    #     "id": int(book_id),
    #     "title": title,
    #     "author": author,
    #     "published_year": year,
    #     "isbn": isbn,
    #     "category_name": category_name,
    #     "total_copies": total,
    #     }

    #     #change page
    #     self.app.change_page("Επεξεργασία Βιβλίου")

    #     #call prefill function
    #     self.app.pages[BookEdit].prefill(self.selected_values)

    #=========================================
    #Reset Selections on Page Change function
    #=========================================
    def reset(self):
        self.books_table.selection_set(())
        self.searchbar_book_var.set("Αναζήτηση...")
        self.booksdata = self._load_books()
        self.populate_data(self.booksdata)

    def _books_to_dicts(self, books):
        normalized = []
        for b in books or []:
            if isinstance(b, dict):
                normalized.append(b)
            else:
                normalized.append({
                    "id": getattr(b, "id", None),
                    "title": getattr(b, "title", ""),
                    "author": getattr(b, "author", ""),
                    "published_year": getattr(b, "published_year", None),
                    "isbn": getattr(b, "isbn", ""),
                    "category_name": getattr(b, "category_name", ""),
                    "available_copies": getattr(b, "available_copies", 0),
                    "total_copies": getattr(b, "total_copies", 0),
                })
        return normalized

    def _load_books(self):
        if not self.service:
            return []
        return self._books_to_dicts(self.service.list_books())
