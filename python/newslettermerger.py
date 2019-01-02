#!/usr/bin/python

"""
TODO
"""

import os
from bs4 import BeautifulSoup
from tkinter import *
import webbrowser
import tempfile

months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

class NewsletterTransformer:
    def __init__(self, master):
        self.master = master
        master.title("Newsletter transformer")

        # Prefix
        self.prefixlabel = Label(master, text="Prefix")
        self.prefixlabel.pack()
        self.prefixentry = Entry(master)
        self.prefixentry.pack()

        # Label
        self.label = Label(master, text="Enter the newsletter html below")
        self.label.pack()

        # Input frame
        self.inputframe = Frame(master)
        self.html_box_scrollbar = Scrollbar(self.inputframe)
        self.html_box_scrollbar.pack(side=RIGHT, fill=Y)

        self.html_box = Text(self.inputframe, borderwidth=3, relief="sunken")
        self.html_box.pack(side=LEFT, fill=BOTH, expand=1)

        self.html_box_scrollbar.config(command=self.html_box.yview)
        self.html_box.config(yscrollcommand=self.html_box_scrollbar.set)
        self.inputframe.pack(fill=BOTH, expand=1)

        # # Output frame
        # self.outputframe = Frame(master)
        # self.output_box_scrollbar = Scrollbar(self.outputframe)
        # self.output_box_scrollbar.pack(side=RIGHT, fill=Y)
        #
        # self.output_box = TkinterHtml(self.outputframe)
        # self.output_box.pack(side=LEFT, fill=BOTH, expand=1)
        #
        # self.output_box_scrollbar.config(command=self.output_box.yview)
        # self.output_box.config(yscrollcommand=self.output_box_scrollbar.set)
        # self.outputframe.pack(fill=BOTH, expand=1)

        # Button frame
        self.buttonframe = Frame(master)
        self.greet_button = Button(self.buttonframe, text="Transform", command=self.transform).grid(row=0, column=0)
        self.close_button = Button(self.buttonframe, text="Clear", command=self.clear).grid(row=0, column=1)
        self.close_button = Button(self.buttonframe, text="Close", command=master.quit).grid(row=0, column=2)
        self.buttonframe.pack()

    def transform(self):
        soup = BeautifulSoup(self.html_box.get("1.0", 'end-1c'), "html.parser")
        output = []
        for li in soup.find_all('li'):
            font = li.find('font')
            if font is not None:
                line = "".join([str(x).replace("\n", " ") for x in font.contents])
                # line = li.text.replace("\n", " ")
                regex_result = re.match(r'^(\d{1,2})(\-\d{1,2})?\.(\d{1,2})\s+(.*)',line)
                if regex_result:
                    try:
                        month = months[int(regex_result.group(3)) - 1]
                        day = int(regex_result.group(1))
                        text = regex_result.group(4)
                        nbsp = "&nbsp;" * 2
                        if day > 9:
                            nbsp = "&nbsp;" * 4
                        new_line = "%s: %s %d%s %s" % (self.prefixentry.get(), month, day, nbsp, text)
                        output.append(new_line)
                    except:
                        pass

        # self.output_box.delete("1.0", END)
        # self.output_box.parse("<br/>".join(output))

        output_file_name = os.path.join(tempfile.gettempdir(),"newlettermerger_output.html")
        with open(output_file_name, "w") as output_file:
            output_file.write("<html><head></head><body><p>"+"<br/>".join(output)+"</p></body></html>")
            webbrowser.open_new("file://"+output_file_name)

    def clear(self):
        self.html_box.delete("1.0", END)
        # self.output_box.delete("1.0", END)

root = Tk()
my_gui = NewsletterTransformer(root)
root.mainloop()
