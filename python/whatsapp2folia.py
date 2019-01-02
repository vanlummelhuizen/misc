import sys
import os
from lxml import etree
import re
from datetime import datetime



file_name = sys.argv[1]

file_basename = os.path.basename(file_name)
file_basename = file_basename.replace(".txt", "")

root = etree.Element("FoLiA", {"{http://www.w3.org/XML/1998/namespace}id": file_basename})
text_element = etree.Element("text", {"{http://www.w3.org/XML/1998/namespace}id": file_basename + ".text.1"})
root.append(text_element)

def try_match(regex, date_format, line):
    match = re.match(regex, line)
    if match:
        date_and_time = datetime.strptime(match.groups()[0], '%d/%m/%Y %H:%M')
        begin_datetime = date_and_time.strftime('%Y-%m-%dT%H:%M')
        actor = match.groups()[1]
        text = match.groups()[2]
        return begin_datetime, actor, text
    return None, None, None

def make_event(begin_datetime, actor, text):
    event_id = file_basename + ".text.1.event." + str(index + 1)
    event_element = etree.Element("event", {"class": "message",
                                            "begindatetime": begin_datetime,
                                            "actor": actor,
                                            "{http://www.w3.org/XML/1998/namespace}id": event_id})
    t_element = etree.Element("t")
    t_element.text = text
    event_element.append(t_element)
    text_element.append(event_element)

with open(file_name, encoding="utf8") as input_file:
    lines = ["".join(filter(lambda x: ord(x) < 57430, l)).strip() for l in input_file.readlines()]

    previous = None

    for index, line in enumerate(lines):

        if previous is not None:
            make_event(previous)

        begin_datetime = None
        actor = None
        text = None

        regexes = [
            (r'^(\d{1,2}\/\d{1,2}\/\d{4} \d{2}:\d{2}): ([^:]+): (.*)', '%d/%m/%Y %H:%M'),
            (r'^(\d{1,2}-\d{1,2}-\d{4} \d{2}:\d{2}:\d{2}): ([^:]+): (.*)', '%d-%m-%y %H:%M'),
            (r'^(\d{1,2}\s+[A-Za-z]{3}\.?\s+(\d{2}|\d{4})?)\s+\-\s+([^:]+): (.*)', '%d %b. %H:%M')
        ]

        for regex in regexes:
            (begin_datetime, actor, text) = try_match(regex, line)
            if begin_datetime is not None:
                break

        if begin_datetime is None:
            previous[2] = previous[2] + text
        else:
            previous = (begin_datetime, actor, text)

    if previous is not None:
        make_event(previous)




print(etree.tostring(root, pretty_print=True).decode("utf8"))
