# ─── imports ─────────────────────────
import tkinter as tk
from tkinter import ttk
from gui.Styles import *


class Rating(tk.Frame):
    def __init__(self,parent,app):
        super().__init__(parent,bg=BG_MAIN)
        self.app = app

        #make Rating expand fully
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        #frame creation and grid config
        self.rating_frame = tk.Frame(
                            self,
                            bg = BG_MAIN,
                            padx=30,
                            pady=20
                            )
        self.rating_frame.grid(row=0,column=0, sticky='nswe')

        self.rating_frame.grid_propagate(False)
        self.rating_frame.grid_columnconfigure(0, weight=1)
        self.rating_frame.grid_rowconfigure(0, weight=0)
        self.rating_frame.grid_rowconfigure(1, weight=1)
        self.rating_frame.grid_rowconfigure(2, weight=1)
        self.rating_frame.grid_rowconfigure(3, weight=0)
        self.rating_frame.grid_rowconfigure(4, weight=0)

        #back button icon
        self.back_btn_icon = tk.PhotoImage(file= 'gui/Assets/back_btn_icon.png')
        #back button
        back_btn = tk.Button(
                            self.rating_frame,
                            anchor='w',
                            compound='left',
                            image=self.back_btn_icon,
                            text='Δανεισμός Βιβλίων',
                            bd=0,
                            width=160,
                            padx=10,
                            bg= BG_MAIN,
                            activebackground=BG_MAIN,
                            activeforeground=FG_MUTED,
                            fg= FG_MUTED,
                            font= FONT_MAIN,
                            command= lambda: self.app.change_page("Δανεισμός Βιβλίων"),
                            cursor="hand2"
                            )
        back_btn.grid(row=0,column=0,padx=5,pady=(0,10),sticky='w')

        #rating title 
        rating_label = tk.Label(
                            self.rating_frame,
                            anchor='center',
                            text='Βαθμολόγησε το Βιβλίο:',
                            bd=0,
                            bg= BG_MAIN,
                            fg= FG_MUTED,
                            font= FONT_TITLE_BOLD
                            )
        rating_label.grid(row=1,column=0, pady=(30,15))

        #submit button
        self.submit_button = ttk.Button(
                        self.rating_frame,
                        text = "ΥΠΟΒΟΛΗ",
                        width=18,
                        style="CustomButton.TButton",
                        cursor= 'hand2'
                        )
        self.submit_button.grid(row=4, column=0, sticky='e',padx=15,pady=130)

        #rating entry
        self.rating_var = tk.DoubleVar()
        self.rating_entry = ttk.Entry(
                self.rating_frame,
                font = FONT_TITLE_BOLD,
                width=5,
                justify='center',
                style="CustomEntry.TEntry",
                textvariable=self.rating_var,
                exportselection=False,
                validate='focusout'       
                )
        self.rating_entry.grid(row=3, column=0, pady=20)
        #call star update on entry text change
        self.rating_var.trace_add("write", lambda *args: self.star_update())

        
        #rating text
        rating_label = tk.Label(
                        self.rating_frame,
                        text="/ 5",
                        anchor='e',
                        bd=0,
                        bg= BG_MAIN,
                        fg= FG_DARK,
                        font= FONT_TITLE_BOLD
                        )
        rating_label.grid(row=3, column=0,padx=(140,0), pady=20)

        #Stars Canvas
        self.star_empty = tk.PhotoImage(file="gui/Assets/star_empty.png")  
        self.star_full = tk.PhotoImage(file="gui/Assets/star_full.png")
        self.star_half = tk.PhotoImage(file="gui/Assets/star_half.png")

        self.star_canvas = tk.Canvas(
                        self.rating_frame,
                        bd=0,
                        highlightthickness=0,
                        bg= BG_MAIN,
                        height=120,
                        width=700
                        )
        self.star_canvas.grid(row=2, column=0)
        self.star_canvas.create_image

        self.stars=[]

        x_pos=100//2
        y_pos = 96//2

        for i in range(5):
            img = self.star_canvas.create_image(x_pos,y_pos,image=self.star_empty,anchor='center')
            self.stars.append(img)
            x_pos+=150

    #star image states
    def set_star(self,index,state):
        if state == "full":
            img = self.star_full
        elif state == "half":
            img = self.star_half
        else:
            img = self.star_empty

        self.star_canvas.itemconfig(self.stars[index], image=img)

    #star update
    def star_update(self):
        #check entry input
        try:
            rating = float(self.rating_var.get())
        #rating=0 if empty entry box
        except tk.TclError:
            rating = 0.0
        
        #clear stars
        for i in range(5):
            self.set_star(i, "empty")

        full_stars = int(rating)
        has_half = (rating - full_stars) != 0.0

        for i in range(full_stars):
            self.set_star(i,'full')
        if has_half and full_stars<5:
            self.set_star(full_stars,'half')

    #=========================================
    #Reset Entries & Selection on Page Change
    #=========================================    
    def reset(self):
        self.rating_var.set(0.0)
        self.star_update()