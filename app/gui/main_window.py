import tkinter as tk
from tkinter import ttk

from app.gui.members_view import MembersView
from app.gui.catalog_view import CatalogView
from app.gui.lending_view import LendingView
from app.gui.statistics_view import StatisticsView
from app.gui.recommendations_view import RecommendationsView


class MainWindow(tk.Tk):
    """
    Κεντρικό παράθυρο της εφαρμογής.
    Περιέχει tabs:
    - Members
    - Catalog
    - Lending
    - Statistics
    - Recommendations
    """

    def __init__(self, logic):
        super().__init__()

        self.logic = logic
        self.title("Library Lending Management")
        self.geometry("1200x750")

        # Notebook (tabs)
        notebook = ttk.Notebook(self)
        notebook.pack(fill="both", expand=True)

        # --- MEMBERS TAB ---
        members_tab = MembersView(notebook, logic)
        notebook.add(members_tab, text="Members")

        # --- CATALOG TAB ---
        catalog_tab = CatalogView(notebook, logic)
        notebook.add(catalog_tab, text="Catalog")

        # --- LENDING TAB ---
        lending_tab = LendingView(notebook, logic)
        notebook.add(lending_tab, text="Lending")

        # --- STATISTICS TAB ---
        statistics_tab = StatisticsView(notebook, logic)
        notebook.add(statistics_tab, text="Statistics")

        # --- RECOMMENDATIONS TAB ---
        recommendations_tab = RecommendationsView(notebook, logic)
        notebook.add(recommendations_tab, text="Recommendations")
