from typing import List
import os
from jinja2 import Environment, FileSystemLoader
from moffee.compositor import Page, PageOption, composite, parse_frontmatter
from moffee.markdown import md
from moffee.utils.md_helper import extract_title
from moffee.utils.file_helper import redirect_paths, copy_assets, merge_directories


def read_options(document_path) -> PageOption:
    """Read frontmatter options from the document path"""
    with open(document_path, "r", encoding="utf8") as f:
        document = f.read()
    _, options = parse_frontmatter(document)
    return options


def retrieve_structure(pages: List[Page]) -> dict:
    current_h1 = None
    current_h2 = None
    current_h3 = None
    last_h1_idx = -1
    last_h2_idx = -1
    last_h3_idx = -1
    page_meta = []
    headings = []
    for i, page in enumerate(pages):
        if page.h1 and page.h1 != current_h1:
            current_h1 = page.h1
            current_h2 = None
            current_h3 = None
            last_h1_idx = len(headings)
            headings.append({"level": 1, "content": page.h1, "page_ids": []})

        if page.h2 and page.h2 != current_h2:
            current_h2 = page.h2
            current_h3 = None
            last_h2_idx = len(headings)
            headings.append({"level": 2, "content": page.h2, "page_ids": []})

        if page.h3 and page.h3 != current_h3:
            current_h3 = page.h3
            last_h3_idx = len(headings)
            headings.append({"level": 3, "content": page.h3, "page_ids": []})

        if page.h1 or page.h2 or page.h3:
            headings[last_h1_idx]["page_ids"].append(i)
        if page.h2 or page.h3:
            headings[last_h2_idx]["page_ids"].append(i)
        if page.h3:
            headings[last_h3_idx]["page_ids"].append(i)

        page_meta.append({"h1": current_h1, "h2": current_h2, "h3": current_h3})

    return {"page_meta": page_meta, "headings": headings}


def render_jinja2(document: str, template_dir) -> str:
    """Run jinja2 templating to create html"""
    # Setup Jinja 2
    env = Environment(loader=FileSystemLoader(template_dir))

    env.filters["markdown"] = md

    template = env.get_template("index.html")

    # Fill template
    pages = composite(document)
    title = extract_title(document) or "Untitled"
    slide_struct = retrieve_structure(pages)
    _, options = parse_frontmatter(document)
    width, height = options.computed_slide_size

    data = {
        "title": title,
        "struct": slide_struct,
        "slide_width": width,
        "slide_height": height,
        "slides": [
            {
                "h1": page.h1,
                "h2": page.h2,
                "h3": page.h3,
                "chunk": page.chunk,
                "layout": page.option.layout,
                "styles": page.option.styles,
            }
            for page in pages
        ],
    }

    return template.render(data)


def build(
    document_path: str, output_dir: str, template_dir: str, theme_dir: str = None
):
    """Render document, create output directories and write result html."""
    with open(document_path, encoding="utf8") as f:
        document = f.read()
    asset_dir = os.path.join(output_dir, "assets")

    merge_directories(template_dir, output_dir, theme_dir)
    options = read_options(document_path)
    output_html = render_jinja2(document, output_dir)
    output_html = redirect_paths(
        output_html, document_path=document_path, resource_dir=options.resource_dir
    )
    output_html = copy_assets(output_html, asset_dir, url_prefix="assets")

    output_file = os.path.join(output_dir, f"index.html")
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(output_html)
