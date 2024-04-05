import tkinter as tk


class Constants:

    APP_TITLE = "Library Management System"
    CHECKIN_WINDOW_TITLE = "Book Check-in"
    BORROWER_WINDOW_TITLE = "Add New Borrower"
    FINES_TITLE = "Pay Fines"

    LATE_FEE_PER_DAY = 0.25

    STICKY_TOP = tk.N

    SINGLE_EXPAND = 1
    DOUBLE_EXPAND = 2
    TRIPLE_EXPAND = 3

    BUTTON_ID = "<ButtonRelease-1>"

    MAIN_FRAME_CONFIG = {
        "width": 1000,
        "height": 480,
    }

    HEADING_LABEL_CONFIG = {
        "text": "Library Management System",
        "font": ("Times", 20, "bold", "underline"),
    }

    BOOK_SEARCH_BOX_CONFIG = {
        "width": 60,
        "highlightthickness": 1
    }

    SEARCH_BUTTON_CONFIG = {
        "text": "Search",
        "font": ("Times", 15, "bold"),
        "width": 8
    }

    SEARCH_RESULTS_TABLE_CONFIG = {
        "columns": [
            "ISBN", "Book Title", "Author(s)", "Availability"]
    }

    SEARCH_RESULTS_TABLE_HEADING_1 = {
        "column": "#0",
        "text": "ISBN",
    }
    SEARCH_RESULTS_TABLE_HEADING_2 = {
        "column": "#1",
        "text": "Book Title",
    }
    SEARCH_RESULTS_TABLE_HEADING_3 = {
        "column": "#2",
        "text": "Author(s)",
    }
    SEARCH_RESULTS_TABLE_HEADING_4 = {
        "column": "#3",
        "text": "Availability",
    }

    CHECKOUT_BUTTON_CONFIG = {
        "text": "Check Out Book",
        "font": ("Times", 13, "normal"),
    }
    CHECKIN_BUTTON_CONFIG = {
        "text": "Check In Book",
        "font": ("Times", 13, "normal"),
    }
    UPDATE_FINES_BUTTON_CONFIG = {
        "text": "Update Fines",
        "font": ("Times", 13, "normal"),
    }
    PAY_FINES_BUTTON_CONFIG = {
        "text": "Pay Fines",
        "font": ("Times", 13, "normal"),
    }
    INCREMENT_DAY_BUTTON_CONFIG = {
        "text": "Increment Day",
        "font": ("Times", 13, "normal"),
    }
    ADD_BORROWER_BUTTON_CONFIG = {
        "text": "Add New Borrower",
        "font": ("Times", 13, "normal"),
    }

    ADD_BORROWER_TEXT_CONFIG = {
        "HEADING": "Enter Details: ",
        "LABEL_1": "First Name",
        "LABEL_2": "Last Name",
        "LABEL_3": "SSN",
        "LABEL_4": "Street Address",
        "LABEL_5": "City",
        "LABEL_6": "State",
        "LABEL_7": "Phone Number",
        "BUTTON": "Add",
    }

    CHECKIN_WINDOW_HEADING_CONFIG = {
        "text": "Search below: \n(Using Book's ISBN, Borrower's Card ID or Borrower's Name)",
        "font": ("Times", 15, "normal"),
    }
    CHECKIN_WINDOW_INPUT_CONFIG = {
        "width": 60,
        "highlightthickness": 1
    }
    CHECKIN_WINDOW_SEARCH_BUTTON_CONFIG = {
        "text": "Search",
        "font": ("Times", 15, "bold"),
    }
    CHECKIN_WINDOW_BUTTON_CONFIG = {
        "text": "Check In",
        "font": ("Times", 15, "bold"),
    }

    CHECKIN_RESULTS_TABLE_COLUMNS = [
        "Loan ID", "ISBN", "Borrower's Card ID", "Title"]

    CHECKIN_RESULTS_TABLE_HEADINGS = {
        1: {
            "column": "#0",
            "text": "Loan ID"
        },
        2: {
            "column": "#1",
            "text": "ISBN"
        },
        3: {
            "column": "#3",
            "text": "Borrower's Card ID"
        },
        4: {
            "column": "#4",
            "text": "Book Title"
        },
    }

    PAY_FINES_WINDOW_HEADING_CONFIG = {
        "text": "Enter borrower's Card ID: ",
        "font": ("Times", 15, "bold"),
    }
    SHOW_FINES_BUTTON_CONFIG = {
        "text": "Show Fines",
        "font": ("Times", 15, "bold"),
    }
    PAY_FINE_BUTTON_CONFIG = {
        "text": "Pay Fine",
        "font": ("Times", 15, "bold"),
    }
