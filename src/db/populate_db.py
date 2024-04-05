import mysql.connector
import csv

cnx = mysql.connector.connect(
    user='root', password='root', database='LIBRARY', charset='utf8')

cursor = cnx.cursor(prepared=True)

with open('./data/books_modified.csv', errors='ignore') as csvfile:
    author_id = 0

    readCSV = list(csv.reader(csvfile, delimiter='\t'))

    firstRow = True

    authorsSet = set()
    authorsDict = dict()

    for row in readCSV:
        if firstRow:
            firstRow = False
            continue

        query = 'Insert into BOOK values(%s,%s)'
        isbn = row[0]
        title = row[2]
        authors = row[3]

        cursor.execute(query, (isbn, title))

        authorList = authors.split(",")

        existing_author_id = 0

        for author in authorList:
            # print("** author: ", author)

            # if author == '':
            #     print("authorList: ", authorList)

            query1 = 'Insert into AUTHORS values(%s,%s)'
            query2 = 'Insert into BOOK_AUTHORS values(%s,%s)'

            try:

                if author in authorsDict:
                    existing_author_id = authorsDict[author]
                    # cursor.execute(query1, (existing_author_id, author))
                    cursor.execute(query2, (isbn, existing_author_id))
                else:
                    author_id += 1
                    authorsDict[author] = author_id
                    cursor.execute(query1, (author_id, author))
                    cursor.execute(query2, (isbn, author_id))

            except mysql.connector.Error as err:
                # TODO: handle error
                print("mySQL Error: ", err)
                pass

print("---- DB Populated! ----")

cnx.commit()
cursor.close()
cnx.close()
