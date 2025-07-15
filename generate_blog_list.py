#!/usr/bin/env python3
import os
import json

BLOGS_DIR  = 'blogs'
OUTPUT_FILE = 'blogs.json'

def make_title(path):
    # Derive a human-readable title from the filename
    name = os.path.splitext(os.path.basename(path))[0]
    return name.replace('-', ' ').replace('_', ' ').strip()

def main():
    if not os.path.isdir(BLOGS_DIR):
        print(f"Error: directory '{BLOGS_DIR}' not found.")
        return 1

    entries = []
    for fname in sorted(os.listdir(BLOGS_DIR), key=str.lower):
        if not fname.lower().endswith('.html'):
            continue
        url   = os.path.join(BLOGS_DIR, fname).replace(os.sep, '/')
        title = make_title(url)
        entries.append({
            "title": title,
            "url":   url
        })

    # Wrap under the "blogs" key so old JS (data.blogs) continues working
    output = { "blogs": entries }

    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"Generated {OUTPUT_FILE} with {len(entries)} entries.")
    return 0

if __name__ == "__main__":
    exit(main())
