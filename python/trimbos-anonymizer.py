#!/usr/bin/python

"""
TODO
"""

import sys
import getopt
import re
from filecollectionprocessing.fileprocessor import FileProcessor
from filecollectionprocessing.filecollectionprocessor import FileCollectionProcessor
from openpyxl import load_workbook

class TrimbosAnonymizer(FileProcessor):
    _extensions = ["xml", "xls", "xlsx"]

    def __init__(self, first_row, last_row, agent_column, prechat_column, body_column,
                 names_file=None, organisations_file=None, places_file=None, words_and_names_file=None):
        self.first_row = first_row
        self.last_row = last_row
        self.agent_column = agent_column
        self.prechat_column = prechat_column
        self.body_column = body_column

        self.replace_lists = {}
        for type, file_name in {"name": names_file,
                                "organisation": organisations_file,
                                "place": places_file}.items():
            if file_name is not None:
                with open(file_name) as file:
                    lines = file.readlines()
                    lines = [line.strip() for line in lines]
                    self.replace_lists[type] = lines

        self.words_and_names = []
        if words_and_names_file is not None:
            with open(words_and_names_file) as words_and_names:
                self.words_and_names = [line.strip().lower() for line in words_and_names.readlines()]
        print(len(self.words_and_names))

        self.agent_set = set([])

    def process_file(self, file_name):
        """
        Processes one file.

        :param file_name:
        :return:
        """
        # try:
        # Load the workbook
        workbook = load_workbook(filename=file_name)
        # Take the first worksheet
        worksheet = workbook[workbook.get_sheet_names()[0]]

        for row_index in range(self.first_row, self.last_row+1):
            # Agents
            agent = worksheet[self.agent_column+str(row_index)].value
            self.agent_set.add(agent)
            worksheet[self.agent_column + str(row_index)] = "[name]"

            # Prechat
            prechat = worksheet[self.prechat_column+str(row_index)].value
            prechat_lines = prechat.strip().split("\n")

            # print([item.split(" = ") for item in prechat_lines])
            # prechat_dict = dict(re.split(" = ?", item) for item in prechat_lines)
            # print(prechat_dict["Naam"])
            # print(prechat)

            prechat = re.sub(r'(Naam:? = ?)[^\n]*(\n)', r'\1[name]\2', prechat)
            prechat = re.sub(r'(Woonplaats:? = ?)[^\n]*(\n)', r'\1[place]\2', prechat)
            prechat = re.sub(r'\d{4}[ \t]*[A-Za-z]{2}\b', '[zipcode]', prechat)
            prechat = self.replace_using_list_items(prechat)
            prechat = self.replace_email_address(prechat)
            prechat = self.replace_url(prechat)
            prechat = self.replace_acronyms(prechat)
            worksheet[self.prechat_column + str(row_index)] = prechat

            # Body
            body = worksheet[self.body_column+str(row_index)].value
            body = re.sub(r'(\] )\w+(:)', r'\1[name]\2', body)
            body = re.sub(r'\d{4}[ \t]*[A-Za-z]{2}\b', '[zipcode]', body)

            body = self.replace_using_list_items(body)
            body = self.replace_email_address(body)
            body = self.replace_url(body)
            body = self.replace_acronyms(body)

            worksheet[self.body_column + str(row_index)] = body

        workbook.save(file_name + "_NEW.xlsx")

        # except Exception as exception:
        #     print(exception)

    def replace_using_list_items(self, text):
        for type, list in self.replace_lists.items():
            for item in list:
                print("Item: " + item)
                print("item.lower(): " + item.lower())
                print("In words_and_names: " + str(item.lower() in self.words_and_names))
                if len(item) < 5 or item.lower() in self.words_and_names:
                    # Strict: NOT ignoring case
                    print("Strict: " + item)
                    text = re.sub(r'\b' + re.sub(r'\\ ', '\s+', re.escape(item)) + r'\b', "[%s]" % type, text)
                else:
                    # Not strict: ignoring case
                    print("Not strict: " + item)
                    text = re.sub(r'\b' + re.sub(r'\\ ', '\s+', re.escape(item)) + r'\b', "[%s]" % type, text,
                                  flags=re.I)
        return text

    def replace_email_address(self, text):
        return re.sub(r"[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})", "[email]", text)

    def replace_url(self, text):
        return re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', "[url]", text)

    def replace_acronyms(self, text):
        return re.sub(r'\b[A-Z]{2,}\b', "[acronym]", text)


    def get_extensions(self):
        return self._extensions

if __name__ == "__main__":
    # -o Output directory; optional
    usage = "Usage: \n" + sys.argv[0] + \
            " -o <output directory>" + \
            " -n <names list>" + \
            " -r <organisation list>" + \
            " -p <places list>"

    # Set default values
    output_dir = None

    # Register command line arguments
    opt_list, file_list = getopt.getopt(sys.argv[1:], 'o:n:r:p:w:')
    for opt in opt_list:
        if opt[0] == '-o':
            output_dir = opt[1]
        if opt[0] == '-n':
            names_file = opt[1]
        if opt[0] == '-r':
            organisations_file = opt[1]
        if opt[0] == '-p':
            places_file = opt[1]
        if opt[0] == '-w':
            print("W")
            words_and_names_file = opt[1]

    # Check for errors and report
    errors = []
    if file_list is None or len(file_list) == 0:
        errors.append("No files or directories given.")

    if len(errors) != 0:
        print("Errors:")
        print("\n".join(errors))
        print(usage)
        exit(1)

    # Report registered options
    print("OPTIONS", file=sys.stderr)
    print("Files: " + ", ".join(file_list), file=sys.stderr)
    print("Names file: " + names_file, file=sys.stderr)
    print("Organisations file: " + organisations_file, file=sys.stderr)
    print("Places file: " + places_file, file=sys.stderr)
    print("Words and names file: " + words_and_names_file, file=sys.stderr)
    if output_dir is not None:
        print("Output directory: " + output_dir, file=sys.stderr)

    # Build and run
    file_collection_processor = FileCollectionProcessor(file_list, output_dir=output_dir, extensions_to_process=["xlsx"])
    trimbosAnonymizer = TrimbosAnonymizer(13, 25, "D", "W", "Y", names_file=names_file,
                                          organisations_file=organisations_file, places_file=places_file,
                                          words_and_names_file=words_and_names_file)
    file_collection_processor.add_file_processor(trimbosAnonymizer)
    file_collection_processor.run()