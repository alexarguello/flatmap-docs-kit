import os
import re
import shutil
from pathlib import Path
from typing import List

PLAN_FILE = "plan.md"
TEMPLATE_FILE = "docs/.template.md"
SIDEBAR_FILE = "sidebars.js"
AUTHOR = "Alexandra Arguello [https://github.com/alexarguello}]"

DEFAULT_FRONTMATTER = {
    "type": "guide",
    "level": "beginner",
    "status": "draft",
    "visibility": "public",
    "author": AUTHOR
}

sidebar_structure = {}

def slugify(text):
    return text.lower().replace(" ", "-").replace("&", "and").replace("/", "-")

def extract_sections(lines: List[str]):
    sections = {}
    current_path = None
    buffer = []

    for line in lines:
        match = re.search(r"\(\s*->\s*`([^`]+)`\s*\)", line)
        if match:
            if current_path and buffer:
                sections[current_path] = buffer
            current_path = match.group(1).strip()
            buffer = []
        elif current_path:
            buffer.append(line)

    if current_path and buffer:
        sections[current_path] = buffer

    return sections

def read_template():
    if not os.path.exists(TEMPLATE_FILE):
        return ""
    with open(TEMPLATE_FILE, encoding="utf-8") as f:
        return f.read()

def write_markdown(path, frontmatter, content, template):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write("---\n")
        for key, value in frontmatter.items():
            if isinstance(value, list):
                f.write(f"{key}: [{', '.join(value)}]\n")
            else:
                f.write(f"{key}: {value}\n")
        f.write("---\n\n")
        if template:
            f.write(template + "\n\n")
        f.writelines(content)

def generate_intro(folder_path, title):
    intro_path = os.path.join(folder_path, "_intro.md")
    if not os.path.exists(intro_path):
        frontmatter = {
            "title": title,
            "type": "overview",
            "level": "beginner",
            "status": "draft",
            "visibility": "public",
            "topics": [slugify(Path(folder_path).name)],
            "author": AUTHOR
        }
        write_markdown(intro_path, frontmatter, [f"# {title}\n\n*(Overview coming soon)*\n"], read_template())

def add_to_sidebar(path):
    parts = Path(path).parts
    if "accessibility" not in parts:
        return
    idx = parts.index("accessibility")
    rel_parts = parts[idx + 1:]
    current = sidebar_structure.setdefault("accessibility", {})
    for part in rel_parts[:-1]:
        current = current.setdefault(part, {})
    current.setdefault("_files", []).append("/".join(["accessibility"] + list(rel_parts)))

def build_sidebar_items(structure):
    items = []
    for key, value in structure.items():
        if key == "_files":
            items.extend(sorted(value))
        else:
            items.append({
                "type": "category",
                "label": key.replace("-", " ").title(),
                "items": build_sidebar_items(value)
            })
    return items

def write_sidebar():
    sidebar_items = build_sidebar_items(sidebar_structure)
    with open(SIDEBAR_FILE, "w", encoding="utf-8") as f:
        f.write("module.exports = {\n  docs: [\n")
        f.write("    {\n      type: 'category',\n      label: 'Accessibility Hub',\n      items: [\n")
        for item in sidebar_items:
            f.write(f"        {repr(item)},\n")
        f.write("      ]\n    }\n  ]\n};\n")

def main():
    with open(PLAN_FILE, encoding="utf-8") as f:
        lines = f.readlines()

    template = read_template()
    sections = extract_sections(lines)

    for rel_path, content in sections.items():
        full_path = os.path.join("docs", "accessibility", rel_path)
        folder = os.path.dirname(full_path)
        filename = os.path.basename(full_path)
        title = Path(filename).stem.replace("-", " ").title()

        # --- FIX: Skip if rel_path is a directory (no filename) ---
        if not filename or filename.endswith("/"):
            continue

        ftype = "external" if "external-resources" in filename else "guide"
        topics = [slugify(p) for p in Path(folder).parts if p not in ("docs", "accessibility")]

        frontmatter = {
            "title": title,
            "type": ftype,
            "level": "beginner",
            "status": "draft",
            "visibility": "public",
            "topics": topics,
            "author": AUTHOR
        }

        write_markdown(full_path, frontmatter, content, template)
        generate_intro(folder, Path(folder).name.replace("-", " ").title())
        add_to_sidebar(full_path)

        if os.path.exists(TEMPLATE_FILE):
            shutil.copy(TEMPLATE_FILE, os.path.join(folder, ".template.md"))

    write_sidebar()
    print("✅ All files generated under docs/accessibility/")
    print("✅ sidebars.js updated")

if __name__ == "__main__":
    main()