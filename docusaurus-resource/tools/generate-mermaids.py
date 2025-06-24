import os
import re

ROOT_DIR = os.path.abspath(os.path.join(os.getcwd(), "docs"))
MAX_DEPTH = 4
DO_NOT_EDIT = "<!-- AUTO-GENERATED FILE — DO NOT EDIT. Regenerated on merge -->"

def strip_order_prefix(name):
    return re.sub(r"^\d{2,}-", "", name)

def normalize_id(path):
    id_raw = path.replace("/", "_").replace("-", "_").replace(".", "_")
    return f"n_{id_raw}" if re.match(r"^\d", id_raw) else id_raw

def extract_title(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip().startswith("# "):
                    return line.strip().lstrip("# ").strip()
        return os.path.basename(path).replace(".md", "")
    except:
        return "Untitled"

def build_mermaid(folder_path, rel_path, depth, parent_id=None):
    lines = []
    clicks = []
    classes = {}

    current_id = normalize_id(rel_path or "root")
    label = strip_order_prefix(os.path.basename(folder_path)).replace("-", " ").title() or "Home"
    lines.append(f'{current_id}["{label}"]')

    if rel_path:
        clean_rel_path = "/".join(strip_order_prefix(p) for p in rel_path.split(os.sep))
        clicks.append(f'click {current_id} "/docs/{clean_rel_path}"')

    if parent_id:
        lines.append(f"{parent_id} --> {current_id}")

    if depth >= MAX_DEPTH:
        return lines, clicks, {current_id: depth}

    entries = sorted(os.listdir(folder_path))
    for entry in entries:
        full_path = os.path.join(folder_path, entry)
        entry_rel_path = os.path.join(rel_path, entry) if rel_path else entry

        if os.path.isdir(full_path):
            sub_lines, sub_clicks, sub_classes = build_mermaid(full_path, entry_rel_path, depth + 1, current_id)
            lines.extend(sub_lines)
            clicks.extend(sub_clicks)
            classes.update(sub_classes)

        elif entry.endswith(".md") and entry != "index.md":
            title = extract_title(full_path)
            node_id = normalize_id(entry_rel_path)
            is_external, external_url = is_external_doc(full_path)

            label = f'{title} 🔗' if is_external else title
            lines.append(f'{node_id}["{label}"]')
            lines.append(f"{current_id} --> {node_id}")

            if is_external and external_url:
                clicks.append(f'click {node_id} "{external_url}" _blank')
            else:
                clean_entry_path = "/docs/" + "/".join(strip_order_prefix(p) for p in entry_rel_path.replace(".md", "").split(os.sep))
                clicks.append(f'click {node_id} "{clean_entry_path}"')

            classes[node_id] = depth + 1


    classes[current_id] = depth
    return lines, clicks, classes

def generate_index_md(folder_path, rel_path):
    folder_name = os.path.basename(folder_path)
    human_title = strip_order_prefix(folder_name).replace("-", " ").title() or "Home"

    frontmatter = f"---\ntitle: {human_title}\nhide_title: true\n---"

    # Use a class-based version of the helper text for better compatibility
    custom_intro = [
        f"### {human_title}",
        '<p class="margin-top-negative"><em>Click any block below to navigate directly to that section.</em></p>',
        ""
    ]

    lines, clicks, classes = build_mermaid(folder_path, rel_path, depth=0)

    class_lines = []
    for d in range(MAX_DEPTH + 1):
        color = ["#b3d9ff", "#d5b3ff", "#ffcccc", "#ffd699", "#d0f0c0"][d % 5]
        class_lines.append(f"classDef col{d} fill:{color},stroke:none;")
    for node_id, col in classes.items():
        class_lines.append(f"class {node_id} col{col};")

    output = [
                 frontmatter,
                 DO_NOT_EDIT,
                 ""
             ] + custom_intro + [
                 "```mermaid",
                 "graph LR",
             ] + lines + clicks + class_lines + [
                 "linkStyle default interpolate basis",
                 "```"
             ]

    index_md_path = os.path.join(folder_path, "index.md")
    with open(index_md_path, "w", encoding="utf-8") as f:
        f.write("\n".join(output))

    print(f"✔️  Wrote: {index_md_path}")


def walk_folders():
    for root, dirs, files in os.walk(ROOT_DIR):
        md_files = [f for f in files if f.endswith(".md")]
        if md_files or dirs:
            rel_path = os.path.relpath(root, ROOT_DIR)
            if rel_path == ".":
                rel_path = ""
            generate_index_md(root, rel_path)

def is_external_doc(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
            match = re.search(r'^type:\s*external\s*$', content, re.MULTILINE)
            if not match:
                return False, None
            link_match = re.search(r'^link:\s*(\S+)', content, re.MULTILINE)
            return True, link_match.group(1) if link_match else None
    except:
        return False, None

walk_folders()
