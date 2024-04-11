import os
import re

def extract_last_url(md_content):
    urls = re.findall(r'\(https?://[^\s)]+\)', md_content)
    if urls:
        return urls[-1].strip('()')
    return None

with open('results_file.txt', 'w') as results_file:
    with open('README.md', 'r',encoding='utf-8') as md_file:
        lines = md_file.readlines()

    for line in lines:
        parts = line.split('|')
        if len(parts) > 2 and any(keyword in parts[2].lower() for keyword in [' br', 'latam', 'americas', 'worldwide']):
            match = re.search(r'\[([^\]]+)\]\(([^)]+)\)', parts[0])
            if match:
                filename = match.group(2).strip()[1:]
                markdown_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), filename)
                with open(markdown_file_path, 'r',encoding='utf-8') as file_to_read:
                    content = file_to_read.read()
                    last_url = extract_last_url(content)
                    if last_url:
                        results_file.write(last_url + '\n')
