import requests
import re
from bs4 import BeautifulSoup, Comment
from urllib.parse import urljoin
import sys
from collections import defaultdict
from contextlib import redirect_stdout

def extract_html_comments(html):
    soup = BeautifulSoup(html, 'lxml')
    return [c.strip() for c in soup.find_all(string=lambda t: isinstance(t, Comment)) if c.strip()]

def extract_css_comments(css_content):
    comments = re.findall(r'/\*.*?\*/', css_content, re.DOTALL)
    return [c.strip() for c in comments if c.strip()]

def extract_js_comments(js_content):
    return re.findall(r'(?://[^\n]*|/\*[\s\S]*?\*/)', js_content, re.MULTILINE)

session = requests.Session()
session.headers.update({"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"})

if len(sys.argv) < 2:
    print("Usage: python3 script.py <url> [-o]")
    sys.exit(1)

base_url = sys.argv[1]
html = session.get(base_url).text
soup = BeautifulSoup(html, 'html.parser')

css_files = []
js_files = []

for link in soup.find_all('link', rel='stylesheet'):
    if 'href' in link.attrs:
        css_files.append(urljoin(base_url, link['href']))

for script in soup.find_all('script', src=True):
    js_files.append(urljoin(base_url, script['src']))

print("Found CSS files:", len(css_files))
print("Found JS files:", len(js_files))

all_comments = defaultdict(list)

# Extract from HTML
all_comments['HTML'].extend(extract_html_comments(html))

# Fetch and extract CSS
for css_url in css_files:
    try:
        css_content = session.get(css_url).text
        all_comments['CSS'].extend(extract_css_comments(css_content))
    except Exception as e:
        print(f"[!] Failed to fetch CSS: {css_url} -> {e}")

# Fetch and extract JS
for js_url in js_files:
    try:
        js_content = session.get(js_url).text
        all_comments['JS'].extend(extract_js_comments(js_content))
    except Exception as e:
        print(f"[!] Failed to fetch JS: {js_url} -> {e}")

def comment_extraction():
    for file_type, comments in all_comments.items():
        print(f"\n{file_type} Comments ({len(comments)}):")
        for comment in comments:
            print(f"  - {comment}")

# Output
if '-o' in sys.argv:
    output_file = 'comments.txt'
    with open(output_file, 'w') as f:
        with redirect_stdout(f):
            comment_extraction()
    print(f"[+] Output stored in {output_file}")
else:
    comment_extraction()
