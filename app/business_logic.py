from .dto import (
    CreateCategoryDTO, CategoryResponseDTO,
    CreateBookDTO, UpdateBookDTO, BookResponseDTO,
    CreateMemberDTO, UpdateMemberDTO, MemberResponseDTO,
    CreateLoanDTO, ReturnLoanDTO, LoanResponseDTO
)

from .validation import MemberValidator


class BusinessLogic:
    def __init__(self, dal):
        self.dal = dal
        self.member_validator = MemberValidator()

    # ---------------------------------------------------------
    # MEMBERS
    # ---------------------------------------------------------
    def list_members(self):
        return self.dal.list_members()

    def add_member(self, **kwargs):
        # Create DTO
        dto = CreateMemberDTO(**kwargs)

        # Validate DTO
        self.member_validator.validate_create(dto)

        # Pass to DAL
        return self.dal.add_member(dto)

    def update_member(self, member_id, **kwargs):
        dto = UpdateMemberDTO(**kwargs)

        # If you later add validate_update, call it here
        # self.member_validator.validate_update(dto)

        return self.dal.update_member(member_id, dto)

    def delete_member(self, member_id):
        return self.dal.delete_member(member_id)

    def get_member(self, member_id):
        return self.dal.get_member(member_id)

    # ---------------------------------------------------------
    # CATEGORIES
    # ---------------------------------------------------------
    def add_category(self, name, description=""):
        dto = CreateCategoryDTO(name=name)
        return self.dal.add_category(dto)

    def list_categories(self):
        return self.dal.list_categories()

    def delete_category(self, category_id):
        return self.dal.delete_category(category_id)

    # ---------------------------------------------------------
    # BOOKS
    # ---------------------------------------------------------
    def add_book(self, **kwargs):
        dto = CreateBookDTO(**kwargs)
        return self.dal.add_book(dto)

    def list_books(self):
        return self.dal.list_books()

    def search_books(self, keyword):
        return self.dal.search_books(keyword)

    def update_book(self, book_id, **kwargs):
        dto = UpdateBookDTO(**kwargs)
        return self.dal.update_book(book_id, dto)

    def delete_book(self, book_id):
        return self.dal.delete_book(book_id)

    # ---------------------------------------------------------
    # LENDING
    # ---------------------------------------------------------
    def borrow_book(self, member_id, book_id):
        dto = CreateLoanDTO(member_id=member_id, book_id=book_id)
        return self.dal.borrow_book(dto)

    def return_book(self, loan_id, rating=None):
        dto = ReturnLoanDTO(loan_id=loan_id, rating=rating)
        return self.dal.return_book(dto)

    def list_loans(self):
        return self.dal.list_loans()

    # ---------------------------------------------------------
    # RATINGS (optional future feature)
    # ---------------------------------------------------------
    def add_or_update_rating(self, member_id, book_id, rating):
        return self.dal.add_or_update_rating(member_id, book_id, rating)
