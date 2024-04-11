import os
import re
import time
from datetime import datetime

def extract_last_url(md_content):
    urls = re.findall(r'\(https?://[^\s)]+\)', md_content)
    if urls:
        return urls[-1].strip('()')
    return None

def create_subfolder(folder_name, date_stamp):
    return f'    <DT><H3 ADD_DATE="{date_stamp}" LAST_MODIFIED="{date_stamp}">{folder_name}</H3>\n    <DL><p>\n'

html_bookmarks = '''
<!DOCTYPE NETSCAPE-Bookmark-file-1>
<META HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=UTF-8">
<TITLE>Bookmarks</TITLE>
<H1>Bookmarks</H1>
<DL><p>
'''
date_stamp = int(time.mktime(datetime.now().timetuple()))
html_bookmarks += create_subfolder("Extracted Jobs", date_stamp)



with open('README.md', 'r', encoding='utf-8', errors='ignore') as md_file:
    for line in md_file:
        parts = line.split(' | ')
        if len(parts) >= 3 and any(term in parts[2].lower() for term in ['br', 'latam', 'americas', 'worldwide']):
            bookmark_name = parts[0].strip('[]').split(']')[0]
            bookmark_link = parts[0].split('](')[-1].strip(')')
            html_bookmarks += f'    <DT><A HREF="{bookmark_link}" ADD_DATE="">{bookmark_name}</A>\n'



html_bookmarks += '    </DL><p>\n</DL><p>'

with open('bookmarks.html', 'w', encoding='utf-8') as html_file:
    html_file.write(html_bookmarks)
