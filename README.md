# Library Management System

## Installation and execution:

1. Clone the repository to the desired location.
2. Start and run the MySQL server on your machine.
3. Change and update the MySQL root username and password inside the files:
   -> `library_app_setup.sh` (under the “./src/scripts” directory)
   -> `init.py` & `populate_db.py` (under the “./src/db” directory)
4. Update the path to `borrowers.csv` file inside the `library_queries.sql` file (under the “./src/db” directory).
5. Run the “./src/scripts/library_app_setup.sh” script using the following command in your terminal:
   `bash src/scripts/library_app_setup.sh`
6. After the script has completed its execution, the application will automatically launch.
   If you want to manually relaunch the application, run the following command in the terminal:
   `python3 src/index.py`

### Info:

**Platform**: macOS Ventura (v13.0)

**Language**: Python (v3.9)

**Frameworks**: NONE

**Database**: MySQL (v8.0)

**Software Libraries**: Tkinter (GUI Toolkit for Python), MySQL Connector for Python (v8.0)

---
