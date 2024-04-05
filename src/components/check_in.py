import tkinter as tk
from tkinter import ttk

from db.init import cnx, cursor

from constants import Constants
from utils import todays_date, get_todays_date


class CheckIn:
    def __init__(self, master, arg):
        self.parent = master

        self.selected_book_loan_id = None
        self.search_books = arg

        self.initialise_ui()

    def initialise_ui(self):
        self.label__search_field = tk.Label(
            self.parent, **Constants.CHECKIN_WINDOW_HEADING_CONFIG)
        self.input__search_field = tk.Entry(
            self.parent, **Constants.CHECKIN_WINDOW_INPUT_CONFIG)
        self.btn__search = tk.Button(
            self.parent, **Constants.CHECKIN_WINDOW_SEARCH_BUTTON_CONFIG, command=self.search_book_loans)
        self.btn__check_in = tk.Button(
            self.parent, **Constants.CHECKIN_WINDOW_BUTTON_CONFIG, command=self.check_in_selected_book)

        self.table__results = ttk.Treeview(
            self.parent, columns=Constants.CHECKIN_RESULTS_TABLE_COLUMNS)

        self.table__results = ttk.Treeview(
            self.parent, columns=Constants.CHECKIN_RESULTS_TABLE_COLUMNS)
        self.table__results.heading(
            **Constants.CHECKIN_RESULTS_TABLE_HEADINGS[1])
        self.table__results.heading(
            **Constants.CHECKIN_RESULTS_TABLE_HEADINGS[2])
        self.table__results.heading(
            **Constants.CHECKIN_RESULTS_TABLE_HEADINGS[3])
        self.table__results.heading(
            **Constants.CHECKIN_RESULTS_TABLE_HEADINGS[4])
        self.table__results.bind(
            Constants.BUTTON_ID, self.select_book_for_checkin)

        self.label__search_field.grid(column=0, row=0, pady=18, padx=18)
        self.input__search_field.grid(column=0, row=1)
        self.input__search_field.config(
            highlightbackground="gray", highlightcolor="gray")
        self.btn__search.grid(column=0, row=2, pady=18, padx=18)
        self.table__results.grid(column=0, row=3)
        self.btn__check_in.grid(column=0, row=4, pady=18, padx=18)

    def search_book_loans(self):
        user_search_input = self.input__search_field.get()

        query = "SELECT BOOK_LOANS.Loan_ID, BOOK_LOANS.Isbn, BOOK_LOANS.Card_id, " + \
                "BOOK.Title, BOOK_LOANS.Date_in FROM BOOK_LOANS " + \
                "JOIN BORROWERS ON BOOK_LOANS.Card_id = BORROWERS.Card_id " + \
                "JOIN BOOK ON BOOK_LOANS.Isbn = BOOK.Isbn " + \
                "WHERE BOOK_LOANS.Isbn LIKE '%" + user_search_input + "%' " + \
                "OR BORROWERS.First_name LIKE '%" + user_search_input + "%' " + \
                "OR BORROWERS.Last_name LIKE '%" + user_search_input + "%' " + \
                "OR BOOK_LOANS.Card_id LIKE '%" + user_search_input + "%' "

        cursor.execute(query)
        result = cursor.fetchall()

        # clear the table before inserting (displaying) new data
        self.table__results.delete(*self.table__results.get_children())

        for record in result:
            print("\n** record: ", record)

            loan_id, isbn, card_id, title, date_in = record

            if date_in is None:
                self.table__results.insert("", "end", text=str(loan_id),
                                           values=(isbn, card_id, title))

    def select_book_for_checkin(self, arg):
        selected_record_id = self.table__results.focus()
        selected_record = self.table__results.item(selected_record_id)
        selected_record_text = selected_record['text']  # Loan ID
        # selected_record_values = selected_record['values']  # ISBN, Card ID, Title
        self.selected_book_loan_id = selected_record_text

    def check_in_selected_book(self):
        if self.selected_book_loan_id is None:
            tk.messagebox.showinfo(
                "Attention!", "Select a book to check in first!")
            # self.parent.destroy()
            return None

        query = "SELECT Date_in FROM BOOK_LOANS " + \
            "WHERE Loan_ID = '" + str(self.selected_book_loan_id) + "' "

        cursor.execute(query)
        result = cursor.fetchall()

        book_checked_in_date = result[0][0]

        if book_checked_in_date is None:
            query = "UPDATE BOOK_LOANS " + \
                "SET BOOK_LOANS.Date_in = '" + str(get_todays_date()) + "' " + \
                "WHERE BOOK_LOANS.Loan_ID = '" + \
                    str(self.selected_book_loan_id) + "' "

            cursor.execute(query)
            cnx.commit()

            self.search_books()

            tk.messagebox.showinfo("Done", "Book checked-in successfully!")

            self.parent.destroy()
        else:
            # self.parent.destroy()
            return None
