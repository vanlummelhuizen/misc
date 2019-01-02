#!/usr/bin/python

"""
TODO
"""

import sys
from bs4 import BeautifulSoup
from tkinter import *

class NewsletterTransformer:
    def __init__(self, master):
        self.master = master
        master.title("Newsletter transformer")

        self.label = Label(master, text="Enter the newsletter html below")
        self.label.pack()

        self.buttonframe = Frame(master)
        self.greet_button = Button(self.buttonframe, text="Transform", command=self.transform).grid(row=0, column=0)
        self.close_button = Button(self.buttonframe, text="Clear", command=self.clear).grid(row=0, column=1)
        self.close_button = Button(self.buttonframe, text="Close", command=master.quit).grid(row=0, column=2)
        self.buttonframe.pack(side=BOTTOM)

        self.html_box_scrollbar = Scrollbar(master)
        self.html_box_scrollbar.pack(side=RIGHT, fill=Y)

        self.html_box = Text(master, borderwidth=3, relief="sunken")
        self.html_box.pack(side=LEFT, fill=BOTH, expand=1)

        self.html_box_scrollbar.config(command=self.html_box.yview)
        self.html_box.config(yscrollcommand=self.html_box_scrollbar.set)

    def transform(self):
        #print(self.html_box.get("1.0", 'end-1c'))
        soup = BeautifulSoup(self.html_box.get("1.0", 'end-1c'), "html.parser")
        for li in soup.find_all('li'):
            print(li.text.replace("\n", " "))

    def clear(self):
        self.html_box.delete("1.0", END)

root = Tk()
my_gui = NewsletterTransformer(root)
root.mainloop()
