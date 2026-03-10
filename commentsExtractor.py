import requests
import re
from bs4 import BeautifulSoup, Comment
from urllib.parse import urljoin
import argparse
from collections import defaultdict


def extract_html_comments(html):
    soup = BeautifulSoup(html, 'lxml')
    return [c.strip() for c in soup.find_all(string=lambda t: isinstance(t, Comment)) if c.strip()]

def extract_css_comments(css_content):
    comments = re.findall(r'/\*.*?\*/', css_content, re.DOTALL)
    return [c.strip() for c in comments if c.strip()]

def extract_js_comments(js_content):
    return re.findall(r'(?://[^\n]*|/\*[\s\S]*?\*/)', js_content, re.MULTILINE)


parser = argparse.ArgumentParser(
    prog='commentsExtractor',
    description='Extract hidden comments from HTML, CSS, and JS files of a target URL'
)
parser.add_argument('url', help='Target URL to scan')
parser.add_argument('-o', '--output', help='Save output to a file', metavar='FILE')
args = parser.parse_args()

base_url = args.url

session = requests.Session()
session.headers.update({"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"})

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
print("HTML pages: 1")

all_comments = defaultdict(list)

all_comments['HTML'].extend(extract_html_comments(html))

for css_url in css_files:
    try:
        css_content = session.get(css_url).text
        all_comments['CSS'].extend(extract_css_comments(css_content))
    except:
        pass

for js_url in js_files:
    try:
        js_content = session.get(js_url).text
        all_comments['JS'].extend(extract_js_comments(js_content))
    except:
        pass

lines = []
for file_type, comments in all_comments.items():
    lines.append(f"\n{file_type} Comments ({len(comments)}):")
    for comment in comments:
        lines.append(f"- {comment}")

output_text = "\n".join(lines)
print(output_text)

if args.output:
    with open(args.output, 'w') as f:
        f.write(output_text)
    print(f"\n[+] Output saved to {args.output}")
