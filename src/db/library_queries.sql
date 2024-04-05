-- tr -cd '[:print:]\t\n' < /Users/dakshkhetan/Desktop/books.csv > books_modified.csv
-- Reference: https://stackoverflow.com/questions/15034944/trying-to-delete-non-ascii-characters-only

DROP DATABASE IF EXISTS LIBRARY;
CREATE DATABASE LIBRARY;
USE LIBRARY;


CREATE TABLE BOOK (
  Isbn     CHAR(20)      NOT NULL, 
  Title    VARCHAR(255)  NOT NULL,
  PRIMARY KEY (Isbn)
);

CREATE TABLE AUTHORS (
  Author_id   INT(11)       NOT NULL, 
  Name        VARCHAR(255)  NOT NULL,
  PRIMARY KEY (Author_id)
);

CREATE TABLE BOOK_AUTHORS (
  Isbn        CHAR(20)    NOT NULL,
  Author_id   INT(11)     NOT NULL,
  PRIMARY KEY (Isbn, Author_id),
  FOREIGN KEY (Isbn)      REFERENCES BOOK(Isbn),
  FOREIGN KEY (Author_id) REFERENCES AUTHORS(Author_id)
);


ALTER TABLE BOOK 
  ADD UNIQUE INDEX BOOK_Index_Isbn (Isbn);


CREATE TABLE BORROWERS (
  Card_id     VARCHAR(20)   NOT NULL,
  Ssn         CHAR(11)      NOT NULL,
  First_name  VARCHAR(20)   NOT NULL,
  Last_name   VARCHAR(20)   NOT NULL,
  Address     VARCHAR(255)  NOT NULL,
  Phone       CHAR(20)      NOT NULL,
  PRIMARY KEY (Card_id)
);

SET GLOBAL local_infile = 1;

LOAD DATA LOCAL INFILE '/Users/dakshkhetan/Workspace/UTDallas/Academics/Fall 2022/CS 6360/Individual Project/dxk210078_cs6360/library-management-system/data/borrowers.csv' INTO TABLE BORROWERS 
  FIELDS TERMINATED BY ',' 
  LINES TERMINATED BY '\n' 
  IGNORE 1 LINES 
  (@col1, @col2, @col3, @col4, @col5, @col6, @col7, @col8, @col9) 
  SET Card_id = @col1,
      Ssn = @col2,
      First_name = @col3,
      Last_name = @col4,
      Address = CONCAT(@col6, ", ", @col7, ", ", @col8),
      Phone = @col9;


CREATE TABLE BOOK_LOANS (
  Loan_id   INT(11)     NOT NULL    AUTO_INCREMENT,
  Isbn      CHAR(20)    NOT NULL,
  Card_id   VARCHAR(20) NOT NULL,
  Date_out  DATETIME,
  Due_date  DATETIME,
  Date_in   DATETIME,
  PRIMARY KEY (Loan_id)
);


ALTER TABLE BOOK_LOANS 
  ADD CONSTRAINT BookLoans_FK_Isbn 
  FOREIGN KEY (Isbn) 
  REFERENCES BOOK(Isbn);

ALTER TABLE BOOK_LOANS 
  ADD CONSTRAINT BookLoans_FK_CardNo 
  FOREIGN KEY (Card_id) 
  REFERENCES BORROWERS(Card_id);

CREATE TABLE FINES(
  Loan_id   INT(11),
  Fine_amt  DECIMAL(5,2),
  Paid      BOOLEAN
);

ALTER TABLE FINES 
  ADD CONSTRAINT Fines_FK_LoanID 
  FOREIGN KEY (Loan_id) 
  REFERENCES BOOK_LOANS(Loan_id);

