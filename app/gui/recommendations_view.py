import tkinter as tk
from tkinter import ttk, messagebox


class RecommendationsView(ttk.Frame):
    """
    Recommendations tab — DTO compatible.
    """

    def __init__(self, parent, logic):
        super().__init__(parent)
        self.logic = logic

        # ---------------------------------------------------------
        # SECTION: Member selection
        # ---------------------------------------------------------
        top_frame = ttk.LabelFrame(self, text="Member")
        top_frame.pack(fill="x", padx=10, pady=10)

        ttk.Label(top_frame, text="Member:").grid(row=0, column=0, sticky="e", padx=5, pady=3)

        self.combo_member = ttk.Combobox(
            top_frame,
            width=40,
            values=self._member_list(),
            state="readonly"
        )
        self.combo_member.grid(row=0, column=1, sticky="w")

        ttk.Button(top_frame, text="Get recommendations", command=self.get_recommendations).grid(
            row=0, column=2, padx=10
        )

        # ---------------------------------------------------------
        # SECTION: Recommendations table
        # ---------------------------------------------------------
        table_frame = ttk.Frame(self)
        table_frame.pack(fill="both", expand=True, padx=10, pady=10)

        columns = ("id", "title", "author", "category", "available", "score")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=15)

        self.tree.heading("id", text="ID")
        self.tree.heading("title", text="Title")
        self.tree.heading("author", text="Author")
        self.tree.heading("category", text="Category")
        self.tree.heading("available", text="Available")
        self.tree.heading("score", text="Score")

        self.tree.column("id", width=40)
        self.tree.column("title", width=180)
        self.tree.column("author", width=150)
        self.tree.column("category", width=120)
        self.tree.column("available", width=80)
        self.tree.column("score", width=80)

        self.tree.pack(fill="both", expand=True)

    # ---------------------------------------------------------
    # Helpers
    # ---------------------------------------------------------
    def _member_list(self):
        """Return dropdown list of members."""
        return [f"{m.id} - {m.full_name}" for m in self.logic.list_members()]

    def _parse_id(self, text):
        return int(text.split(" - ")[0])

    # ---------------------------------------------------------
    # Recommendation logic
    # ---------------------------------------------------------
    def get_recommendations(self):
        try:
            member_text = self.combo_member.get()
            if not member_text:
                raise ValueError("Select a member.")

            member_id = self._parse_id(member_text)

            results = self.logic.recommend_books(member_id)
            # results is list[RecommendationDTO]

            # Clear table
            self.tree.delete(*self.tree.get_children())

            for r in results:
                book = r.book  # BookResponseDTO

                self.tree.insert(
                    "",
                    "end",
                    values=(
                        book.id,
                        book.title,
                        book.author,
                        book.category_name,
                        book.available_copies,
                        round(r.score, 2),
                    ),
                )

        except Exception as e:
            messagebox.showerror("Error", str(e))
