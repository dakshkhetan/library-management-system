import tkinter as tk

from db.init import cnx, cursor

from constants import Constants


class Borrower:
    def __init__(self, master):
        self.parent = master

        self.initialise_ui()

    def initialise_ui(self):
        self.label__heading = tk.Label(
            self.parent, text=Constants.ADD_BORROWER_TEXT_CONFIG["HEADING"], font=("Times", 15, "bold"))
        self.label__first_name = tk.Label(
            self.parent, text=Constants.ADD_BORROWER_TEXT_CONFIG["LABEL_1"])
        self.input__first_name = tk.Entry(self.parent)
        self.label__last_name = tk.Label(
            self.parent, text=Constants.ADD_BORROWER_TEXT_CONFIG["LABEL_2"])
        self.input__last_name = tk.Entry(self.parent)
        self.label__ssn = tk.Label(
            self.parent, text=Constants.ADD_BORROWER_TEXT_CONFIG["LABEL_3"])
        self.input__ssn = tk.Entry(self.parent)
        self.label__address = tk.Label(
            self.parent, text=Constants.ADD_BORROWER_TEXT_CONFIG["LABEL_4"])
        self.input__address = tk.Entry(self.parent)
        self.label__city = tk.Label(
            self.parent, text=Constants.ADD_BORROWER_TEXT_CONFIG["LABEL_5"])
        self.input__city = tk.Entry(self.parent)
        self.label__state = tk.Label(
            self.parent, text=Constants.ADD_BORROWER_TEXT_CONFIG["LABEL_6"])
        self.input__state = tk.Entry(self.parent)
        self.label__phone_number = tk.Label(
            self.parent, text=Constants.ADD_BORROWER_TEXT_CONFIG["LABEL_7"])
        self.input__phone_number = tk.Entry(self.parent)
        self.btn__add_borrower = tk.Button(self.parent, text=Constants.ADD_BORROWER_TEXT_CONFIG["BUTTON"], font=("Times", 15, "normal"),
                                           command=self.add_borrower)

        self.label__heading.grid(
            column=0, row=0, pady=22, padx=22)
        self.label__first_name.grid(column=0, row=1, pady=6, padx=12)
        self.input__first_name.grid(column=0, row=2, pady=6, padx=12)
        self.label__last_name.grid(column=0, row=3, pady=6, padx=12)
        self.input__last_name.grid(column=0, row=4, pady=6, padx=12)
        self.label__ssn.grid(column=0, row=5, pady=6, padx=12)
        self.input__ssn.grid(column=0, row=6, pady=6, padx=12)
        self.label__address.grid(column=0, row=7, pady=6, padx=12)
        self.input__address.grid(column=0, row=8, pady=6, padx=12)
        self.label__city.grid(column=0, row=9, pady=6, padx=12)
        self.input__city.grid(column=0, row=10, pady=6, padx=12)
        self.label__state.grid(column=0, row=11, pady=6, padx=12)
        self.input__state.grid(column=0, row=12, pady=6, padx=12)
        self.label__phone_number.grid(column=0, row=13, pady=6, padx=12)
        self.input__phone_number.grid(column=0, row=14, pady=6, padx=12)
        self.btn__add_borrower.grid(column=0, row=15, pady=6, padx=12)

    def add_borrower(self):
        ssn = str(self.input__ssn.get())

        query = "SELECT EXISTS(SELECT SSN FROM BORROWERS " + \
            "WHERE BORROWERS.SSN = '" + ssn + "') "

        cursor.execute(query)
        result = cursor.fetchall()

        is_ssn_present = (result[0][0] == 1)

        if is_ssn_present:
            tk.messagebox.showinfo("Error", "Borrower already exists!")
            # self.parent.destroy()
            return

        first_name = self.input__first_name.get()
        last_name = self.input__last_name.get()
        phone_number = self.input__phone_number.get()

        street_address = self.input__address.get()
        city = self.input__city.get()
        state = self.input__state.get()
        address = street_address + ", " + city + ", " + state

        query = "SELECT MAX(Card_id) from BORROWERS"

        cursor.execute(query)
        result = cursor.fetchall()

        max_card_no = result[0][0]
        max_card_num = int(max_card_no[2:])
        next_card_num = max_card_num + 1
        new_card_no = "ID" + str(next_card_num).zfill(6)

        print("\n** new_card_no: ", new_card_no, "\n")

        query = "INSERT INTO BORROWERS (Card_id, Ssn, First_name, Last_name, Address, Phone) " + \
            "VALUES ('" + new_card_no + "', '" + ssn + "', '" + first_name + "', '" + \
            last_name + "', '" + address + "', '" + phone_number + "') "

        cursor.execute(query)
        cnx.commit()

        tk.messagebox.showinfo("Info", "Borrower added successfully!")

        self.parent.destroy()
