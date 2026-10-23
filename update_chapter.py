#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CIE 9702 Chapter Automation Tool
Usage:
  python3 update_chapter.py prepare <chapter_num>
  python3 update_chapter.py validate <chapter_html_file>
  python3 update_chapter.py apply <chapter_num> <chapter_html_file>
"""

import sys, os, re, shutil
from html.parser import HTMLParser

BASE_DIR = '/home/bill/nas/ruiqi_website/9702'
HTML_FILE = os.path.join(BASE_DIR, 'index.html')
CACHE_DIR = os.path.join(BASE_DIR, 'pdf_cache')

class TagValidator(HTMLParser):
    def __init__(self):
        super().__init__()
        self.stack = []
        self.void_tags = {'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link', 'meta', 'param', 'source', 'track', 'wbr'}
        self.errors = []

    def handle_starttag(self, tag, attrs):
        if tag.lower() not in self.void_tags:
            self.stack.append((tag.lower(), self.getpos()))

    def handle_endtag(self, tag):
        tag = tag.lower()
        if tag in self.void_tags:
            return
        if not self.stack:
            self.errors.append(f'Unexpected closing tag </{tag}> at line {self.getpos()[0]} col {self.getpos()[1]}')
            return
        last_tag, pos = self.stack.pop()
        if last_tag != tag:
            self.errors.append(f'Mismatched tag: expected </{last_tag}> (opened at {pos}), but got </{tag}> at line {self.getpos()[0]} col {self.getpos()[1]}')

def validate_chapter_html(content):
    errors = []
    # 1. Tag balance
    validator = TagValidator()
    validator.feed(content)
    if validator.stack:
        for tag, pos in validator.stack:
            errors.append(f'Unclosed tag <{tag}> opened at line {pos[0]} col {pos[1]}')
    errors.extend(validator.errors)

    # 2. SVG policy check
    if '<svg' in content.lower():
        errors.append('POLICY VIOLATION: Found inline <svg> tag. All figures must use <img> pointing to images/!')

    # 3. MathJax $ balance check
    # Exclude code or comments
    clean_for_math = re.sub(r'<!--.*?-->', '', content, flags=re.DOTALL)
    dollar_count = clean_for_math.count('$')
    if dollar_count % 2 != 0:
        errors.append(f'Unmatched LaTeX dollar signs: found {dollar_count} $ signs (must be even).')

    return errors

def cmd_prepare(ch_num):
    ch_str = f'{ch_num:02d}' if isinstance(ch_num, int) else ch_num.zfill(2)
    view_id = f'ch{int(ch_num)}-view'
    next_view_id = f'ch{int(ch_num)+1}-view'

    txt_file = os.path.join(CACHE_DIR, f'ch{ch_str}.txt')
    if not os.path.exists(txt_file):
        print(f'Error: Cache file {txt_file} does not exist!')
        sys.exit(1)

    with open(HTML_FILE, 'r', encoding='utf-8') as f:
        html = f.read()

    # Locate ch-view boundaries
    start_m = re.search(r'<div[^>]*id=[\"\']' + view_id + r'[\"\'][^>]*>', html)
    if not start_m:
        print(f'Error: Could not locate <div id=\"{view_id}\"> in index.html!')
        sys.exit(1)

    start_idx = start_m.start()

    # Find next chapter marker or footer
    end_m = re.search(r'<!-- CHAPTER ' + str(int(ch_num)+1) + r' VIEW -->|<div[^>]*id=[\"\']' + next_view_id + r'[\"\'][^>]*>', html)
    if end_m:
        end_idx = end_m.start()
    else:
        # Fallback to main end
        end_idx = html.find('</main>', start_idx)

    slice_html = html[start_idx:end_idx].rstrip()
    if slice_html.endswith('</div>'):
        # Keep intact
        pass

    out_curr = f'/tmp/ch{int(ch_num)}_current.html'
    with open(out_curr, 'w', encoding='utf-8') as f:
        f.write(slice_html)

    print(f'=== CHAPTER {ch_num} PREPARATION READY ===')
    print(f'1. Reference textbook text: {txt_file} ({os.path.getsize(txt_file)/1024:.1f} KB)')
    print(f'2. Existing chapter HTML: {out_curr} ({os.path.getsize(out_curr)/1024:.1f} KB)')
    print(f'3. Location in index.html: index [{start_idx}:{end_idx}]')

    # Analyze existing sections
    sec_ids = re.findall(r'<section[^>]*id=[\"\']([^\"\']+)[\"\']', slice_html)
    print(f'4. Existing sections ({len(sec_ids)}): {sec_ids}')
    ex_count = len(re.findall(r'例题\s*' + str(int(ch_num)) + r'\.\d', slice_html))
    pr_count = len(re.findall(r'练习\s*' + str(int(ch_num)) + r'\.\d', slice_html))
    print(f'5. Existing examples: {ex_count} 例题, {pr_count} 练习')

def cmd_validate(html_file):
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    errors = validate_chapter_html(content)
    if errors:
        print(f'VALIDATION FAILED ({len(errors)} errors):')
        for e in errors:
            print(f'  - {e}')
        return False
    else:
        print('VALIDATION PASSED: Tags balanced, LaTeX $ paired, SVG-free, clean markup.')
        return True

def cmd_apply(ch_num, new_html_file):
    if not cmd_validate(new_html_file):
        print('Aborting apply due to validation failure.')
        sys.exit(1)

    with open(new_html_file, 'r', encoding='utf-8') as f:
        new_content = f.read().strip()

    view_id = f'ch{int(ch_num)}-view'
    next_view_id = f'ch{int(ch_num)+1}-view'

    with open(HTML_FILE, 'r', encoding='utf-8') as f:
        html = f.read()

    start_m = re.search(r'<div[^>]*id=[\"\']' + view_id + r'[\"\'][^>]*>', html)
    if not start_m:
        print(f'Error: Could not locate <div id=\"{view_id}\"> in index.html!')
        sys.exit(1)
    start_idx = start_m.start()

    end_m = re.search(r'<!-- CHAPTER ' + str(int(ch_num)+1) + r' VIEW -->|<div[^>]*id=[\"\']' + next_view_id + r'[\"\'][^>]*>', html)
    if end_m:
        end_idx = end_m.start()
    else:
        end_idx = html.find('</main>', start_idx)

    # Create safety backup
    bak_path = f'{HTML_FILE}.bak_ch{int(ch_num)}'
    shutil.copyfile(HTML_FILE, bak_path)
    print(f'Safety backup created at {bak_path}')

    # Replace
    updated_html = html[:start_idx] + new_content + '\n\n    ' + html[end_idx:]
    with open(HTML_FILE, 'w', encoding='utf-8') as f:
        f.write(updated_html)

    print(f'=== CHAPTER {ch_num} SUCCESSFULLY APPLIED TO index.html ===')
    
    # List images referenced in new content
    imgs = re.findall(r'<img[^>]+src=[\"\']([^\"\']+)[\"\']', new_content)
    print('\n[IMAGES REQUIRED FOR THIS CHAPTER]:')
    for img in sorted(set(imgs)):
        full_p = os.path.join(BASE_DIR, img)
        exists = os.path.exists(full_p)
        status = 'EXISTS (OK)' if exists else 'MISSING (Needs screenshot)'
        print(f'  • {img:<45} [{status}]')

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)
    action = sys.argv[1].lower()
    if action == 'prepare':
        cmd_prepare(int(sys.argv[2]))
    elif action == 'validate':
        cmd_validate(sys.argv[2])
    elif action == 'apply':
        cmd_apply(int(sys.argv[2]), sys.argv[3])
    else:
        print(f'Unknown action: {action}')
        sys.exit(1)
