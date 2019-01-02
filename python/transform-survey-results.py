import csv

transformed_results = []

with open('results-survey876599_nohead.csv', newline='', encoding="utf-8") as csvfile:
    result_reader = csv.reader(csvfile, delimiter=',', quotechar='"')
    for row in result_reader:
        print(row[0])
        prefix = row[:18]
        suffix = row[-4:]
        if row[18]:
            for first_book_cell_index in range(18, len(row)-4, 4):
                print("FIRST: " + row[first_book_cell_index])
                if(row[first_book_cell_index]):
                    new_row = prefix.copy()
                    print("PREFIX: " + str(prefix))
                    new_row.append(row[first_book_cell_index])
                    new_row.append(row[first_book_cell_index+1])
                    new_row.append(row[first_book_cell_index+2])
                    new_row.append(row[first_book_cell_index+3])
                    new_row += suffix
                    print("NEW_ROW: " + str(new_row))
                    transformed_results.append(new_row)
        else:
            new_row = prefix + ["", "", ""] + suffix
            transformed_results.append(new_row)

    with open('transformed-results-survey876599.csv', 'w', newline="\n") as csvoutfile:
        result_writer = csv.writer(csvoutfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for row in transformed_results:
            result_writer.writerow(row)



