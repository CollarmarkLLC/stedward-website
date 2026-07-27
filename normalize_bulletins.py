#!/usr/bin/env python3
"""
Normalize frontmatter for all St. Edward bulletins.
Adds consistent, minimal frontmatter so the user can later update images by season.
"""

import os
import re
from datetime import datetime
from pathlib import Path

POSTS_DIR = Path("src/posts")

def extract_existing_frontmatter(content):
    """Extract existing title and date if present."""
    title = None
    date = None
    
    # Look for title
    title_match = re.search(r'^title:\s*["\']?(.*?)["\']?\s*$', content, re.MULTILINE)
    if title_match:
        title = title_match.group(1).strip()
    
    # Look for date
    date_match = re.search(r'^date:\s*["\']?(\d{4}-\d{2}-\d{2})', content, re.MULTILINE)
    if date_match:
        date = date_match.group(1)
    
    return title, date

def generate_title_from_filename(filename, existing_title):
    """Generate a reasonable title if none exists."""
    if existing_title and existing_title != "placeholderText":
        return existing_title
    
    # Try to extract date from filename
    match = re.search(r'(\d{4}-\d{2}-\d{2})', filename)
    if match:
        date_str = match.group(1)
        try:
            dt = datetime.strptime(date_str, "%Y-%m-%d")
            return dt.strftime("%B %-d, %Y")
        except:
            pass
    return filename.replace(".md", "").replace("-", " ").title()

def normalize_file(filepath):
    content = filepath.read_text(encoding="utf-8")
    
    # Skip if it already has clean frontmatter we like
    if content.startswith("---\n") and "image:" in content.split("---")[1]:
        return False  # already normalized
    
    title, date = extract_existing_frontmatter(content)
    
    # Derive date from filename if not found
    if not date:
        match = re.search(r'(\d{4}-\d{2}-\d{2})', filepath.name)
        if match:
            date = match.group(1)
        else:
            date = "2020-01-01"  # fallback
    
    title = generate_title_from_filename(filepath.name, title)
    
    # Remove old frontmatter
    body = re.sub(r'^---.*?---\s*', '', content, flags=re.DOTALL).strip()
    
    # Build new clean frontmatter
    new_frontmatter = f"""---
title: "{title}"
date: {date}
image: /images/bulletins/placeholder.jpg
summary: ""
---
"""
    
    new_content = new_frontmatter + "\n" + body + "\n"
    filepath.write_text(new_content, encoding="utf-8")
    return True

def main():
    updated = 0
    for md_file in sorted(POSTS_DIR.glob("*.md")):
        if normalize_file(md_file):
            updated += 1
            print(f"Normalized: {md_file.name}")
    
    print(f"\nDone. Normalized {updated} bulletin files.")

if __name__ == "__main__":
    main()