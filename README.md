# commentsExtractor

A Python-based web recon tool that extracts hidden comments from HTML, CSS, and JavaScript files of a target web page — useful for bug bounty hunting, CTF challenges, and web application reconnaissance.

## Features

- Extracts **HTML comments** (`<!-- ... -->`) from the main page
- Extracts **CSS comments** (`/* ... */`) from all linked stylesheets
- Extracts **JS comments** (`// ...` and `/* ... */`) from all linked scripts
- Automatically discovers and fetches external CSS/JS files
- Uses a realistic Linux User-Agent to avoid basic bot detection

## Requirements

Install dependencies with:

```bash
pip install requests beautifulsoup4 lxml
```

## Usage

```bash
python3 commentsExtractor.py <target_url>
```

**Example:**

```bash
python3 commentsExtractor.py https://example.com
```

## Sample Output

```
Found CSS files: 2
Found JS files: 5
HTML pages: 1

HTML Comments (3):
- <!-- TODO: remove debug endpoint /admin -->
- <!-- staging build v2.1 -->

CSS Comments (1):
- /* legacy style - deprecated */

JS Comments (8):
- // API key: xxxxxxxxxxxxxxxx
- /* internal use only */
```

## Use Cases

- Web application penetration testing
- Bug bounty recon phase
- CTF web challenges
- OSINT and passive information gathering
