---
description: Update a chapter in the CIE 9702 website using the pre-extracted PDF text and automated pipeline
---

# /update-chapter <chapter_num>

This skill updates chapter `<chapter_num>` in `/home/bill/nas/bic_website/9702/index.html` according to the teacher's reference textbook `Physics9702_Teacher.pdf`.

## Step 1: Run Prepare
Run:
```bash
python3 /home/bill/nas/bic_website/9702/update_chapter.py prepare $ARGUMENTS
```
This extracts `/tmp/ch<N>_current.html` and checks the pre-extracted textbook text `/home/bill/nas/bic_website/9702/pdf_cache/ch<0N>.txt`.

## Step 2: Compare & Synthesize
1. Read the pre-extracted chapter text `/home/bill/nas/bic_website/9702/pdf_cache/ch<0N>.txt`.
2. Compare against `/tmp/ch<N>_current.html`.
3. Identify all missing worked examples (例题), practice questions (练习), summary tables (本章小结), theoretical deductions, definitions, and teacher notes.
4. Ensure text is verbatim identical to the reference text.
5. **IMAGE POLICY (CRITICAL)**:
   - Do NOT generate inline `<svg>`.
   - Use `<div class="diagram-container"><img src="images/ch<0N>_<desc>.png" class="diagram-img" alt="..."><div class="diagram-caption">...</div></div>`.
6. Write the complete, perfectly balanced chapter view HTML to `/tmp/ch<N>_new.html`.

## Step 3: Validate & Apply
Run:
```bash
python3 /home/bill/nas/bic_website/9702/update_chapter.py apply $ARGUMENTS /tmp/ch<N>_new.html
```
This automatically:
- Validates HTML tag balance (TagValidator).
- Verifies LaTeX MathJax `$` delimiter pairs.
- Ensures no SVG tags exist.
- Creates safety backup `index.html.bak_ch<N>`.
- Replaces the chapter block in `index.html`.
- Prints the exact list of screenshots the user needs to provide.

## Step 4: Output Screenshot Summary
Display the table of required images (filename, chapter section, PDF page number, description) for the user.
