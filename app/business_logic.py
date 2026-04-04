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
        dto = CreateMemberDTO(**kwargs)
        self.member_validator.validate_create(dto)
        return self.dal.add_member(dto)

    def update_member(self, member_id, **kwargs):
        dto = UpdateMemberDTO(**kwargs)
        return self.dal.update_member(member_id, dto)

    def delete_member(self, member_id):
        return self.dal.delete_member(member_id)

    def get_member(self, member_id):
        return self.dal.get_member(member_id)

    # ---------------------------------------------------------
    # CATEGORIES
    # ---------------------------------------------------------
    def add_category(self, name, description=""):
        dto = CreateCategoryDTO(name=name, description=description)
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
        dto = ReturnLoanDTO(loan_id=loan_id)
        result = self.dal.return_book(dto)

        if rating is not None:
            self.dal.add_or_update_rating(result.member_id, result.book_id, rating)

        return result

    def list_loans(self):
        return self.dal.list_loans()

    # ---------------------------------------------------------
    # RATINGS
    # ---------------------------------------------------------
    def add_or_update_rating(self, member_id, book_id, rating):
        return self.dal.add_or_update_rating(member_id, book_id, rating)


    # ---------------------------------------------------------
    # STATISTICS
    # ---------------------------------------------------------
    def count_loans_by_member_in_period(self, member_id, start_date, end_date):
        return self.dal.count_loans_by_member_in_period(member_id, start_date, end_date)

    def member_category_distribution_in_period(self, member_id, start_date, end_date):
        return self.dal.member_category_distribution_in_period(member_id, start_date, end_date)

    def category_distribution_in_period(self, start_date, end_date):
        return self.dal.category_distribution_in_period(start_date, end_date)

    def member_loan_history(self, member_id):
        return self.dal.member_loan_history(member_id)

    def loans_per_author(self):
        return self.dal.loans_per_author()

    def loans_per_age(self):
        return self.dal.loans_per_age()

    def loans_per_gender(self):
        return self.dal.loans_per_gender()

