import os
import re
from util import parse_frontmatter, normalize_id, strip_order_prefix

ROOT_DIR = os.path.abspath(os.path.join(os.getcwd(), "docs"))
OUTPUT_DIR = os.path.abspath(os.path.join(os.getcwd(), "docs", "_contribute"))

TEMPLATE = """---
title: Help us write: {title}
id: {id}
sidebar_label: {title}
hide_title: true
---

> 📄 This page was generated to help you contribute this resource. If you're interested, follow the instructions below and submit your PR!

### 🧩 Context

This article belongs in:

**`{section_path}`**

#### Sibling Articles:
{siblings}

---

### ✍️ How to contribute this article

To claim and write this article:

1. **Fork** this repo on GitHub
2. In your fork, navigate to:

```bash
cd docs/{rel_path_folder}
```

3. Open `{filename}` and:
    - Add your name and GitHub handle to the `author` field
    - Set a realistic `eta` field (e.g. `2025-08-01`)
    - Change `status` to `draft`

4. Start writing! You can either:
    - Write inline markdown in this file (example structure will be prefilled)
    - Or link to an external resource you created (example below)

#### 🔁 Example: external resource
```yaml
---
title: Building Your First ADK Agent (Dev.to)
type: external
level: beginner
topics: [tutorial, agents]
status: published
visibility: public
author: Your Name (@githubhandle)
link: https://your-article-link.com
---

👉 <strong><a href="https://your-article-link.com" target="_blank" rel="noopener noreferrer">Read the full tutorial</a></strong>
```

#### 🧠 Example: inline resource
```yaml
---
title: Initializing an ADK Agent
type: tutorial
level: beginner
topics: [agents, initialization, setup]
status: published
visibility: public
author:
  - Your Name (@githubhandle)
---

Intro text here...

```java
// Java example
```
```

---

### ✅ Once you're done
- Mark the article as `review-needed`
- Submit a pull request

Thank you for helping make this resource better! 💚
"""

def get_sibling_summaries(folder_path, current_filename):
    siblings = []
    for fname in sorted(os.listdir(folder_path)):
        if not fname.endswith(".md") or fname == current_filename:
            continue
        fpath = os.path.join(folder_path, fname)
        title = extract_title(fpath)
        fm = parse_frontmatter(fpath)
        status = fm.get("status", "?")
        status_icon = {
            "missing": "❌",
            "draft": "📝",
            "review-needed": "🕵️",
            "published": "✅"
        }.get(status, "•")
        siblings.append(f"- {status_icon} **{title}** ({fname})")
    return "\n".join(siblings) or "_No other articles in this folder yet._"

def extract_title(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip().startswith("# "):
                    return line.strip().lstrip("# ").strip()
        return os.path.basename(path).replace(".md", "")
    except:
        return "Untitled"

def create_contribution_page(md_path, rel_path, frontmatter):
    title = frontmatter.get("title", os.path.basename(md_path).replace(".md", ""))
    id = normalize_id(rel_path)
    filename = os.path.basename(md_path)
    rel_path_folder = os.path.dirname(rel_path)
    abs_folder_path = os.path.join(ROOT_DIR, rel_path_folder)

    siblings = get_sibling_summaries(abs_folder_path, filename)
    section_path = rel_path_folder.replace(os.sep, " > ")

    content = TEMPLATE.format(
        title=title,
        id=id,
        section_path=section_path,
        rel_path_folder=rel_path_folder,
        filename=filename,
        siblings=siblings
    )

    output_path = os.path.join(OUTPUT_DIR, id + ".md")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"✅ Created: {output_path}")

def walk_docs():
    for root, _, files in os.walk(ROOT_DIR):
        for f in files:
            if f.endswith(".md") and f != "index.md":
                abs_path = os.path.join(root, f)
                rel_path = os.path.relpath(abs_path, ROOT_DIR)
                frontmatter = parse_frontmatter(abs_path)
                status = frontmatter.get("status", None)

                if status == "missing":
                    create_contribution_page(abs_path, rel_path, frontmatter)
                elif status == "draft" and frontmatter.get("collaboration", "") == "open":
                    pass  # TODO: handle open collaboration articles
                elif status == "review-needed":
                    pass  # TODO: handle review-needed ones

if __name__ == "__main__":
    walk_docs()