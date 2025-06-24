import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, "../docs"))

MAX_DEPTH = 4
DO_NOT_EDIT = "<!-- AUTO-GENERATED FILE — DO NOT EDIT. Regenerated on merge -->"

def extract_title(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            lines = f.readlines()
            for line in lines:
                if line.strip().startswith("# "):
                    return line.strip().lstrip("# ").strip()
        return os.path.basename(path).replace(".md", "")
    except:
        return "Untitled"

def make_breadcrumb(path_parts):
    path_links = []
    for i, part in enumerate(path_parts):
        href = "./" if (len(path_parts) - i - 1 == 0) else "../" * (len(path_parts) - i - 1)
        label = part.replace("-", " ").title()
        path_links.append(f"[{label}]({href})")
    return " > ".join(path_links)

def generate_flatmap(folder_path, rel_path, depth):
    lines = []
    entries = sorted(os.listdir(folder_path))

    for entry in entries:
        full_path = os.path.join(folder_path, entry)
        entry_rel_path = os.path.join(rel_path, entry)

        if os.path.isdir(full_path):
            label = entry.replace("-", " ").title()
            if depth < MAX_DEPTH:
                lines.append(f"- **📂 {label}**")
                submap = generate_flatmap(full_path, entry_rel_path, depth + 1)
                for subline in submap:
                    lines.append(f"  {subline}")
        elif entry.endswith(".md") and entry != "index.md":
            title = extract_title(full_path)
            lines.append(f"- 📝 **[{title}]({entry})**")

    return lines

def generate_index_md(folder_path, rel_path):
    folder_name = os.path.basename(folder_path)
    human_title = folder_name.replace("-", " ").title()
    breadcrumb = make_breadcrumb(rel_path.split(os.sep)) if rel_path else "Home"
    flatmap = generate_flatmap(folder_path, rel_path, depth=0)

    frontmatter = f"---\ntitle: {human_title}\n---"
    output = [
        frontmatter,
        DO_NOT_EDIT,
        "",
        f"**📁 Path:** {breadcrumb}",
        "\n---\n",
        "### Contents\n",
    ]
    output += flatmap

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

if __name__ == "__main__":
    print(f"📁 Generating flatmaps up to depth={MAX_DEPTH} under `{ROOT_DIR}`...")
    walk_folders()
    print("✅ Done.")

