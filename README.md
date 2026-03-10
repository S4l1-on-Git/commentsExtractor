# commentsExtractor

A Python-based web recon tool that extracts hidden comments from HTML, CSS, and JavaScript files of a target web page — useful for bug bounty hunting, CTF challenges, and web application reconnaissance.

## Features

- Extracts **HTML comments** (`<!-- ... -->`) from the main page
- Extracts **CSS comments** (`/* ... */`) from all linked stylesheets
- Extracts **JS comments** (`// ...` and `/* ... */`) from all linked scripts
- Automatically discovers and fetches external CSS/JS files
- Uses a realistic Linux User-Agent to avoid basic bot detection
- `-o` flag to save output to a file

## Requirements

Install dependencies with:

```bash
pip install -r requirements.txt
```

## Usage

```bash
python3 commentsExtractor.py <target_url>
python3 commentsExtractor.py -o <output_file> <target_url>
```

**Examples:**

```bash
# Basic scan
python3 commentsExtractor.py https://example.com

# Save output to file
python3 commentsExtractor.py -o results.txt https://example.com
```

## Options

| Flag | Description |
|------|-------------|
| `url` | Target URL to scan (required) |
| `-o, --output FILE` | Save output to a specified file |
| `-h, --help` | Show help message and exit |

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
