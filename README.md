# Comment Extractor

A reconnaissance tool that scrapes and extracts comments from HTML, CSS, and JavaScript files of a target web page. Useful for bug bounty hunting, CTF challenges, and web application penetration testing.

---

## Features

- Extracts **HTML** comments (`<!-- ... -->`)
- Extracts **CSS** block comments (`/* ... */`)
- Extracts **JavaScript** single-line (`// ...`) and block (`/* ... */`) comments
- Optional **file output** with `-o` flag
- Custom **User-Agent** header to blend with browser traffic

---

## Requirements

Install dependencies via pip:

```bash
pip install -r requirements.txt
```

---

## Usage

```bash
python3 commentsExtractor.py <url> [-o]
```

### Arguments

| Argument | Description |
|----------|-------------|
| `<url>`  | Target URL to scan (required) |
| `-o`     | Save output to `comments.txt` (optional) |

### Examples

```bash
# Print comments to terminal
python3 commentsExtractor.py https://example.com

# Save comments to comments.txt
python3 commentsExtractor.py https://example.com -o
```

---

## Output Format

```
Found CSS files: 2
Found JS files: 3

HTML Comments (1):
  - <!-- TODO: remove debug info -->

CSS Comments (2):
  - /* Main stylesheet v1.2 */
  - /* Author: dev@example.com */

JS Comments (4):
  - // API endpoint: /api/v2/internal
  - /* Legacy auth handler - disabled */
```

---

## Recon Tips

Filter output for sensitive keywords:

```bash
python3 script.py https://example.com -o
grep -iE 'password|token|secret|api|key|todo|fix|hack|debug|internal|staging' comments.txt
```

---

## Disclaimer

This tool is intended for **authorized security testing only**. Only use it on targets you have explicit permission to test.
