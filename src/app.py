import tkinter as tk
from tkinter import ttk

from db.init import cnx, cursor

from components.borrower import Borrower
from components.check_out import CheckOut
from components.check_in import CheckIn
from components.fines import Fines

from constants import Constants
from utils import todays_date, change_day, get_todays_date, get_date_diff


class LibraryApp:
    def __init__(self, master):
        self.parent = master
        self.parent.title(Constants.APP_TITLE)

        self.data = None
        self.selected_book = None
        self.borrower_card_id = None

        # self.display_date = tk.StringVar()

        self.initialise_ui()

    def initialise_ui(self):
        self.frame__main = tk.Frame(self.parent, **Constants.MAIN_FRAME_CONFIG)
        self.frame__main.grid(column=0, row=0)
        self.frame__main.grid_rowconfigure(
            index=0, weight=Constants.SINGLE_EXPAND)
        self.frame__main.grid_columnconfigure(
            index=0, weight=Constants.SINGLE_EXPAND)
        self.frame__main.grid_propagate(False)

        self.frame__search = tk.Frame(self.frame__main)
        self.frame__search.grid(column=0, row=1,  sticky=Constants.STICKY_TOP)
        self.frame__search.grid_rowconfigure(
            index=1, weight=Constants.SINGLE_EXPAND)

        self.label__heading = tk.Label(
            self.frame__search, **Constants.HEADING_LABEL_CONFIG)
        self.label__heading.grid(column=0, row=0)
        self.label__heading.grid_rowconfigure(
            index=0, weight=Constants.SINGLE_EXPAND)
        self.label__heading.grid_columnconfigure(
            index=0, weight=Constants.SINGLE_EXPAND)

        self.input__search_box = tk.Entry(
            self.frame__search, **Constants.BOOK_SEARCH_BOX_CONFIG)
        self.input__search_box.config(
            highlightbackground="gray", highlightcolor="gray")
        # self.input__search_box.insert(0, 'Enter search string here...')
        self.input__search_box.grid(
            column=0, row=1,  pady=18, ipadx=50)
        self.input__search_box.grid_rowconfigure(
            index=1, weight=Constants.SINGLE_EXPAND)

        self.btn__search_books = tk.Button(
            self.frame__search, **Constants.SEARCH_BUTTON_CONFIG, command=self.search_books)
        self.btn__search_books.grid(column=0, row=2)
        self.btn__search_books.grid_rowconfigure(
            index=2, weight=Constants.TRIPLE_EXPAND, minsize=50)

        self.frame__results = tk.Frame(self.frame__main)
        self.frame__results.grid(
            column=0, row=2, sticky=Constants.STICKY_TOP, pady=15)
        self.frame__results.grid_rowconfigure(
            index=2, weight=Constants.SINGLE_EXPAND)

        self.table__results = ttk.Treeview(
            self.frame__results, **Constants.SEARCH_RESULTS_TABLE_CONFIG)
        self.table__results.grid(column=0, row=0)
        self.table__results.grid_rowconfigure(
            index=0, weight=Constants.SINGLE_EXPAND)
        self.table__results.heading(**Constants.SEARCH_RESULTS_TABLE_HEADING_1)
        self.table__results.heading(**Constants.SEARCH_RESULTS_TABLE_HEADING_2)
        self.table__results.heading(**Constants.SEARCH_RESULTS_TABLE_HEADING_3)
        self.table__results.heading(**Constants.SEARCH_RESULTS_TABLE_HEADING_4)
        self.table__results.bind(
            Constants.BUTTON_ID, self.select_book_for_checkout)

        self.frame__toggles_menu = tk.Frame(self.frame__main)
        self.frame__toggles_menu.grid(
            column=0, row=3, sticky=Constants.STICKY_TOP)
        self.frame__toggles_menu.grid_rowconfigure(
            index=3, weight=Constants.SINGLE_EXPAND)

        self.btn__check_out_book = tk.Button(
            self.frame__toggles_menu, **Constants.CHECKOUT_BUTTON_CONFIG, command=self.check_out_book)
        self.btn__check_out_book.grid(column=0, row=0, pady=11, padx=11)
        self.btn__check_out_book.grid_rowconfigure(
            index=0, weight=Constants.SINGLE_EXPAND)
        self.btn__check_out_book.grid_columnconfigure(
            index=0, weight=Constants.SINGLE_EXPAND)

        self.btn__check_in_book = tk.Button(
            self.frame__toggles_menu, **Constants.CHECKIN_BUTTON_CONFIG, command=self.check_in_book)
        self.btn__check_in_book.grid(column=1, row=0, pady=11, padx=11)

        self.btn__check_out_book.grid_rowconfigure(
            index=0, weight=Constants.SINGLE_EXPAND)
        self.btn__check_out_book.grid_columnconfigure(
            index=1, weight=Constants.SINGLE_EXPAND)

        self.btn__update_fines_data = tk.Button(
            self.frame__toggles_menu, **Constants.UPDATE_FINES_BUTTON_CONFIG, command=self.update_fines)
        self.btn__update_fines_data.grid(column=0, row=1, padx=11, pady=11)

        self.btn__pay_fines = tk.Button(
            self.frame__toggles_menu, **Constants.PAY_FINES_BUTTON_CONFIG, command=self.pay_fines)
        self.btn__pay_fines.grid(column=1, row=1, pady=9, padx=9)

        self.btn__increment_date = tk.Button(
            self.frame__toggles_menu, **Constants.INCREMENT_DAY_BUTTON_CONFIG, command=change_day)
        self.btn__increment_date.grid(column=2, row=1, pady=9, padx=9)

        self.btn__add_borrower = tk.Button(
            self.frame__toggles_menu, **Constants.ADD_BORROWER_BUTTON_CONFIG, command=self.add_borrower)
        self.btn__add_borrower.grid(column=2, row=0, pady=9, padx=9)

    def search_books(self):
        user_search_input = self.input__search_box.get()

        query = "SELECT BOOK.Isbn, Title, GROUP_CONCAT(Name SEPARATOR ', ') AS Name FROM BOOK " + \
            "LEFT JOIN (SELECT BOOK_AUTHORS.Isbn, AUTHORS.Name FROM BOOK_AUTHORS " + \
            "LEFT JOIN AUTHORS ON BOOK_AUTHORS.Author_ID = AUTHORS.Author_ID) AS T " + \
            "ON BOOK.Isbn = T.Isbn " + \
            "WHERE BOOK.Isbn LIKE '%" + user_search_input + "%' " + \
            "OR Title LIKE '%" + user_search_input + "%' " + \
            "OR Name LIKE '%" + user_search_input + "%' " + \
            "GROUP BY BOOK.Isbn; "

        cursor.execute(query)
        result = cursor.fetchall()

        self.data = result

        self.display_books_result_table()

    def display_books_result_table(self):
        records = self.data

        # clear the table before inserting (displaying) new data
        self.table__results.delete(*self.table__results.get_children())

        print("\n** Search results: ", self.data, "\n")

        for record in records:
            print("\n** record: ", record)

            isbn, title, authors = record

            query = "SELECT EXISTS(SELECT Isbn FROM BOOK_LOANS " + \
                "WHERE Isbn = '" + isbn + "') AS Is_Available "

            cursor.execute(query)
            result = cursor.fetchall()

            is_book_available = (result[0][0] == 0)

            if is_book_available:
                availability = "Available"
            else:
                query = "SELECT Date_in from BOOK_LOANS " + \
                    "WHERE Isbn = '" + isbn + "' "

                cursor.execute(query)
                result = cursor.fetchall()

                print("\n** Date_in result: ", result)
                print("** Date_in result[-1][0]: ", result[-1][0])

                # fetching the last record i.e. [-1] of checked out book
                last_record = result[-1][0]

                if last_record is None:
                    availability = "Not Available"
                else:
                    availability = "Available"

            print("\n** Book availability: ", availability)
            print("\n----------------")

            self.table__results.insert("", "end", text=isbn,
                                       values=(title, authors, availability))

    def select_book_for_checkout(self, arg):
        selected_record_id = self.table__results.focus()
        selected_record = self.table__results.item(selected_record_id)
        selected_record_text = selected_record['text']  # Book's ISBN
        # selected_record_values = selected_record['values']    # Book's Title, Author(s), Availability
        self.selected_book = selected_record_text

    def check_out_book(self):
        self.widget__check_out = CheckOut(
            self.selected_book, self.search_books)

    def check_in_book(self):
        self.widget__check_in = tk.Toplevel(self.parent)
        self.widget__check_in.title(Constants.CHECKIN_WINDOW_TITLE)
        self.app__check_in = CheckIn(self.widget__check_in, self.search_books)

    # TODO: add a reset today's date button

    def add_borrower(self):
        self.widget__add_borrower = tk.Toplevel(self.parent)
        self.widget__add_borrower.title(Constants.BORROWER_WINDOW_TITLE)
        self.app__add_borrower = Borrower(self.widget__add_borrower)

    def update_fines(self):
        query = "SELECT Loan_ID, Date_in, Due_date FROM BOOK_LOANS"

        cursor.execute(query)
        result = cursor.fetchall()

        print("\n*** UPDATE FINES called! ***")
        print("\n** result: ", result)

        for record in result:
            loan_id, date_in, date_due = record

            if date_in is None:
                date_in = get_todays_date()

            diff = get_date_diff(date_in, date_due)

            fine = int(diff.days) * \
                Constants.LATE_FEE_PER_DAY if diff.days > 0 else 0

            print("\n** todays_date: ", todays_date)
            print("** date_in: ", date_in)
            print("** date_due: ", date_due)
            print("** date_in.date(): ", date_in.date())
            print("** date_due.date(): ", date_due.date())
            print("** diff: ", diff)
            print("** diff.days: ", diff.days)
            print("** fine (x0.25): ", fine, "\n")

            query = "UPDATE FINES " + \
                "SET FINES.Fine_amt = '" + str(fine) + "' " + \
                "WHERE FINES.Loan_ID = '" + str(loan_id) + "' "

            cursor.execute(query)
            cnx.commit()

        tk.messagebox.showinfo("Info", "Fines have been computed!")

    def pay_fines(self):
        self.widget__pay_fines = tk.Toplevel(self.parent)
        self.widget__pay_fines.title(Constants.FINES_TITLE)
        self.app__pay_fines = Fines(self.widget__pay_fines)
