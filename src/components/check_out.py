import tkinter as tk
from tkinter import simpledialog

from datetime import timedelta

from db.init import cnx, cursor
from utils import todays_date, get_todays_date


class CheckOut:
    def __init__(self, arg1, arg2):
        self.selected_book = arg1
        self.search_books = arg2

        self.check_out_book()

    def check_out_book(self):
        if self.selected_book is None:
            tk.messagebox.showinfo("Attention!", "Select a book first!")
            return None

        self.borrower_card_id = simpledialog.askstring(
            "Check Out Book", "Enter borrower's Card ID")

        query = "SELECT EXISTS(SELECT Card_id from BORROWERS " + \
            "WHERE Card_id = '" + self.borrower_card_id + "') "

        cursor.execute(query)
        result = cursor.fetchall()

        borrower_found = (result[0][0] == 1)

        if not borrower_found:
            tk.messagebox.showinfo("Error", "Borrower does not exist!")
            return None
        else:
            count = 0

            query = "SELECT Date_in from BOOK_LOANS " + \
                "WHERE Card_id = '" + self.borrower_card_id + "' "

            cursor.execute(query)
            result = cursor.fetchall()

            for attr in result:
                date_in = attr[0]
                if date_in is None:
                    count += 1

            if count >= 3:
                tk.messagebox.showinfo(
                    "Not Allowed!", "Borrower has loaned 3 books already!")
                return None
            else:
                query = "INSERT INTO BOOK_LOANS (Isbn, Card_id, Date_out, Due_date) " + \
                    "VALUES ('" + self.selected_book + "', '" + \
                    self.borrower_card_id + "', '" + str(get_todays_date()) + "', '" + \
                    str(get_todays_date() + timedelta(days=14)) + "') "

                cursor.execute("SET FOREIGN_KEY_CHECKS=0")
                cursor.execute(query)
                cursor.execute("SET FOREIGN_KEY_CHECKS=1")
                cnx.commit()

                query = "SELECT MAX(Loan_ID) FROM BOOK_LOANS"

                cursor.execute(query)
                result = cursor.fetchall()

                loan_id = result[0][0]

                query = "INSERT INTO FINES (Loan_ID, Fine_amt, Paid) " + \
                    "VALUES ('" + str(loan_id) + "', '0.00', '0') "

                cursor.execute(query)
                cnx.commit()

                self.search_books()

                tk.messagebox.showinfo(
                    "Done", "Book checked-out successfully!")
