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

            match = re.search(r'\[([^\]]+)\]\(([^)]+)\)', parts[0])
            if match:
                filename = match.group(2).strip()[1:]
                markdown_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), filename)
                with open(markdown_file_path, 'r', encoding='utf-8') as file_to_read:
                            content = file_to_read.read()
                            last_url = extract_last_url(content)
                            if last_url:
                                bookmark_name = parts[0].strip('[]').split(']')[0]
                                html_bookmarks += f'        <DT><A HREF="{last_url}" ADD_DATE="{date_stamp}">{bookmark_name}</A>\n'



html_bookmarks += '    </DL><p>\n</DL><p>'

with open('bookmarks.html', 'w', encoding='utf-8') as html_file:
    html_file.write(html_bookmarks)
