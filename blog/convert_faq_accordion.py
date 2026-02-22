#!/usr/bin/env python3
"""Convert FAQ sections in blog articles from h2/h3/p to accordion (same design as realisations.html)."""
import re
import os

BLOG_DIR = os.path.dirname(os.path.abspath(__file__))
CSS_INSERT = '<link href="../assets/css/encadrement-vert.css" rel="stylesheet"/>'

def add_css_if_missing(content):
    if "encadrement-vert.css" in content:
        return content
    content = content.replace(
        '<link href="../assets/css/article-single.css" rel="stylesheet"/><link href="../assets/css/services-sidebar-mobile.css" rel="stylesheet"/>',
        '<link href="../assets/css/article-single.css" rel="stylesheet"/><link href="../assets/css/encadrement-vert.css" rel="stylesheet"/><link href="../assets/css/services-sidebar-mobile.css" rel="stylesheet"/>'
    )
    return content

def extract_faq_block(content):
    """Find FAQ section: from <h2...>FAQ : TITLE</h2> to last </p> before <div class="mt-50 p-4 rounded"."""
    match = re.search(
        r'<h2 class="text-2 text-semibold font-family-3 mt-40 mb-20">FAQ\s*:\s*([^<]+)</h2>\s*(.*?)<div class="mt-50 p-4 rounded"',
        content,
        re.DOTALL
    )
    if not match:
        return None, None, None
    title = match.group(1).strip()
    rest = match.group(2)
    # Parse Q&A pairs: <h3...>Q</h3> then <p class="text-para-3">A</p>
    pairs = []
    pattern = re.compile(
        r'<h3 class="text-3 text-semibold mt-30 mb-15">([^<]+)</h3>\s*<p class="text-para-3">(.*?)</p>',
        re.DOTALL
    )
    for m in pattern.finditer(rest):
        pairs.append((m.group(1).strip(), m.group(2).strip()))
    if not pairs:
        return None, None, None
    return title, pairs, match

def build_accordion(title, pairs):
    lines = [
        '<div class="article-faq-section mt-50 mb-50 encadrement-vert">',
        '<div class="section-title-center v1">',
        '<h6 class="text-para-3 text-upper text-semibold color-deepTealGreen">FAQ</h6>',
        f'<h2 class="text-2 mt-10 font-family-3 text-bold">{title}</h2>',
        '</div>',
        '<ul class="accordion-main mt-50 mt-xl-60" id="blogFaqAccordion">'
    ]
    for i, (q, a) in enumerate(pairs, 1):
        cls = "active" if i == 1 else ""
        btn_cls = "accordion-btn" if i == 1 else "accordion-btn collapsed"
        collapse_cls = "collapse show" if i == 1 else "collapse"
        lines.append(f'<li class="{cls}">')
        lines.append(f'<button class="{btn_cls}" type="button" data-bs-toggle="collapse" data-bs-target="#blogFaq-item-{i}" data-bs-parent="#blogFaqAccordion">{q}</button>')
        lines.append(f'<div class="{collapse_cls}" id="blogFaq-item-{i}" data-bs-parent="#blogFaqAccordion"><div class="box-content"><p class="text-para-3">{a}</p></div></div>')
        lines.append('</li>')
    lines.append('</ul>')
    lines.append('</div>')
    return '\n'.join(lines)

def process_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    if 'blogFaqAccordion' in content:
        return False, "already converted"
    content = add_css_if_missing(content)
    title, pairs, match = extract_faq_block(content)
    if not title or not pairs:
        return False, "no FAQ block found"
    accordion_html = build_accordion(title, pairs)
    # Replace FAQ block with accordion; keep the following <div class="mt-50 p-4 rounded" and rest
    new_content = content[:match.start()] + accordion_html + '\n\n<div class="mt-50 p-4 rounded"' + content[match.end():]
    with open(path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    return True, f"{len(pairs)} items"

def main():
    converted = 0
    for name in sorted(os.listdir(BLOG_DIR)):
        if name == 'index.html' or not name.endswith('.html'):
            continue
        path = os.path.join(BLOG_DIR, name)
        if not os.path.isfile(path):
            continue
        ok, msg = process_file(path)
        if ok:
            converted += 1
            print(f"OK {name}: {msg}")
        elif "no FAQ" in msg:
            pass  # skip silently
        else:
            print(f"SKIP {name}: {msg}")
    print(f"\nConverted {converted} files.")

if __name__ == '__main__':
    main()
