import requests
import re
from bs4 import BeautifulSoup, Comment
from urllib.parse import urljoin, urlparse
import sys
from collections import defaultdict

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
    print("Usage: python3 script.py <url>")
    sys.exit(1)

base_url = sys.argv[1]
html = session.get(base_url).text
soup = BeautifulSoup(html, 'html.parser')

# Find HTML, CSS, JS links (external files)
html_files = []
css_files = []
js_files = []

for link in soup.find_all('link', rel='stylesheet'):
    if 'href' in link.attrs:
        css_files.append(urljoin(base_url, link['href']))

for script in soup.find_all('script', src=True):
    js_files.append(urljoin(base_url, script['src']))

# Inline HTML is the main page; add external HTML if any (e.g., iframes rare)
html_files.append(base_url)  # Main HTML

print("Found CSS files:", len(css_files))
print("Found JS files:", len(js_files))
print("HTML pages:", len(html_files))

all_comments = defaultdict(list)

# Extract from main HTML
html_comments = extract_html_comments(html)
all_comments['HTML'].extend(html_comments)

# Fetch and extract CSS
for css_url in css_files:
    try:
        css_content = session.get(css_url).text
        css_comments = extract_css_comments(css_content)
        all_comments['CSS'].extend(css_comments)
    except:
        pass

# Fetch and extract JS
for js_url in js_files:
    try:
        js_content = session.get(js_url).text
        js_comments = extract_js_comments(js_content)
        all_comments['JS'].extend(js_comments)
    except:
        pass

# Output
for file_type, comments in all_comments.items():
    print(f"\n{file_type} Comments ({len(comments)}):")
    for comment in comments:  # First 10
        print(f"- {comment}")
