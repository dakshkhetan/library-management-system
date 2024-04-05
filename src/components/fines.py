import tkinter as tk

from db.init import cnx, cursor

from constants import Constants


class Fines:
    def __init__(self, master):
        self.parent = master

        self.total_fine_text = tk.StringVar()
        self.initialise_ui()

    def initialise_ui(self):
        self.label__borrower_card_id = tk.Label(
            self.parent, **Constants.PAY_FINES_WINDOW_HEADING_CONFIG)
        self.input__borrower_card_id = tk.Entry(self.parent)
        self.btn__show_fines = tk.Button(
            self.parent, **Constants.SHOW_FINES_BUTTON_CONFIG, command=self.display_total_fine)
        self.label__fine_amount = tk.Label(
            self.parent, textvariable=self.total_fine_text)
        self.btn__pay_fines = tk.Button(
            self.parent, **Constants.PAY_FINE_BUTTON_CONFIG, command=self.pay_fine)

        self.label__borrower_card_id.grid(column=0, row=0, pady=18, padx=18)
        self.input__borrower_card_id.grid(column=0, row=1, pady=18, padx=18)
        self.btn__show_fines.grid(column=0, row=2, pady=18, padx=18)
        self.label__fine_amount.grid(column=0, row=3, pady=18, padx=18)
        self.btn__pay_fines.grid(column=0, row=4, pady=18, padx=18)

    def display_total_fine(self):
        print("\n*** SHOW FINES called! ***")

        borrower_card_id = self.input__borrower_card_id.get()

        query = "SELECT EXISTS(SELECT Card_id FROM BORROWERS " + \
            "WHERE Card_id = '" + borrower_card_id + "') "

        cursor.execute(query)
        result = cursor.fetchall()

        borrower_not_found = (result[0][0] == 0)

        if borrower_not_found:
            tk.messagebox.showinfo("Error", "Borrower not found!")
        else:
            query = "SELECT FINES.Fine_amt, FINES.Paid FROM FINES " + \
                "JOIN BOOK_LOANS ON FINES.Loan_ID = BOOK_LOANS.Loan_ID " + \
                "WHERE BOOK_LOANS.Card_id = '" + borrower_card_id + "' "

            cursor.execute(query)
            result = cursor.fetchall()

            print("\n** result: ", result)

            total_fine_amount = 0

            for elem in result:
                fine_amount = float(elem[0])
                is_fine_paid = (elem[1] == 1)

                print("\n** is_fine_paid:", is_fine_paid)
                print("** fine_amount:", fine_amount)

                if not is_fine_paid:
                    total_fine_amount += fine_amount

        total_fine_amount = round(total_fine_amount, 2)
        self.total_fine_text.set(f"Total Fine: ${total_fine_amount}")

    def pay_fine(self):
        print("\n*** PAY FINES called! ***")

        borrower_card_id = self.input__borrower_card_id.get()

        query = "SELECT EXISTS(SELECT Card_id FROM BORROWERS " + \
            "WHERE Card_id = '" + borrower_card_id + "') "

        cursor.execute(query)
        result_exists = cursor.fetchall()

        borrower_not_found = (result_exists[0][0] == 0)

        if borrower_not_found:
            tk.messagebox.showinfo("Error", "Borrower does not exist in data")
        else:
            query = "SELECT FINES.Loan_ID FROM FINES " + \
                "JOIN BOOK_LOANS ON FINES.Loan_ID = BOOK_LOANS.Loan_ID " + \
                "WHERE BOOK_LOANS.Card_id = '" + borrower_card_id + "' "

            cursor.execute(query)
            result_loan_ids = cursor.fetchall()

            print("\n** result: ", result_loan_ids)

            for attr in result_loan_ids:
                print("\n** attr: ", attr)

                loan_id = str(attr[0])

                query = "SELECT Date_in FROM BOOK_LOANS " + \
                    "WHERE Loan_id = '" + loan_id + "' "

                cursor.execute(query)
                result_book_date_in = cursor.fetchall()

                print("\n** result_book_date_in: ", result_book_date_in)

                if result_book_date_in[0][0] is None:
                    tk.messagebox.showinfo(
                        "Error", "Book(s) has not been returned yet.")
                    return

            for attr in result_loan_ids:
                loan_id = str(attr[0])

                cursor.execute("UPDATE FINES " +
                               "SET Paid = 1 " +
                               "WHERE Loan_ID = '" + loan_id + "' ")
                cnx.commit()

            tk.messagebox.showinfo("Info", "Fines paid successfully!")
            self.parent.destroy()
