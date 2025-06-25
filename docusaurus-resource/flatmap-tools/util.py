# flatmap-tools/util.py
import os
import re
import json

STYLE_CONFIG_PATH = os.path.abspath(os.path.join(os.getcwd(), "flatmap-tools", "flatmap-style.config.json"))


def load_style_config():
    try:
        with open(STYLE_CONFIG_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"⚠️  Warning: Could not load style config: {e}")
        return {"tags": {}}


def parse_frontmatter(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        if not content.startswith("---"):
            return {}
        match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
        if not match:
            return {}
        frontmatter_text = match.group(1)
        tags = {}
        for line in frontmatter_text.split('\n'):
            line = line.strip()
            if ':' in line and not line.startswith('#'):
                key, value = line.split(':', 1)
                key, value = key.strip(), value.strip()
                if value.startswith('[') and value.endswith(']'):
                    array_content = value[1:-1]
                    value = [item.strip() for item in array_content.split(',')] if array_content.strip() else []
                elif value.startswith(('"', "'")) and value.endswith(('"', "'")):
                    value = value[1:-1]
                tags[key] = value
        return tags
    except Exception as e:
        print(f"⚠️  Could not parse frontmatter from {file_path}: {e}")
        return {}


def extract_title(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip().startswith("# "):
                    return line.strip().lstrip("# ").strip()
        return os.path.basename(path).replace(".md", "")
    except:
        return "Untitled"


def extract_tags_from_frontmatter(frontmatter):
    tags = []
    tag_fields = ['type', 'status', 'level', 'visibility', 'collaboration', 'feature-priority']
    for field in tag_fields:
        if field in frontmatter:
            value = frontmatter[field]
            if isinstance(value, str):
                tags.append(f"{field}:{value}")
    if 'topics' in frontmatter and isinstance(frontmatter['topics'], list):
        for topic in frontmatter['topics']:
            if isinstance(topic, str):
                tags.append(topic)
    return tags


def normalize_id(path):
    id_raw = path.replace("/", "_").replace("-", "_").replace(".", "_")
    return f"n_{id_raw}" if re.match(r"^\d", id_raw) else id_raw


def strip_order_prefix(name):
    return re.sub(r"^\d{2,}-", "", name)


def get_rel_path_from_root(path, root_dir="docs"):
    abs_path = os.path.abspath(path)
    root_path = os.path.abspath(os.path.join(os.getcwd(), root_dir))
    return os.path.relpath(abs_path, root_path)


def get_file_modification_date(path):
    try:
        return os.path.getmtime(path)
    except:
        return 0
