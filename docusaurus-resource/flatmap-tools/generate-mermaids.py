import os
import re
import json

ROOT_DIR = os.path.abspath(os.path.join(os.getcwd(), "docs"))
MAX_DEPTH = 4
DO_NOT_EDIT = "<!-- AUTO-GENERATED FILE — DO NOT EDIT. Regenerated on merge -->"
STYLE_CONFIG_PATH = os.path.abspath(os.path.join(os.getcwd(), "flatmap-tools", "flatmap-style.config.json"))

def load_style_config():
    """Load the flatmap styling configuration."""
    try:
        with open(STYLE_CONFIG_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"⚠️  Warning: Could not load style config: {e}")
        return {"tags": {}}

def parse_frontmatter(file_path):
    """Parse frontmatter from a markdown file and extract tags."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
            
        # Check if file has frontmatter (starts with ---)
        if not content.startswith("---"):
            return {}
            
        # Extract frontmatter
        frontmatter_match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
        if not frontmatter_match:
            return {}
            
        frontmatter_text = frontmatter_match.group(1)
        
        # Parse frontmatter manually
        tags = {}
        for line in frontmatter_text.split('\n'):
            line = line.strip()
            if ':' in line and not line.startswith('#'):
                key, value = line.split(':', 1)
                key = key.strip()
                value = value.strip()
                
                # Handle array values like topics: [agents, lifecycle]
                if value.startswith('[') and value.endswith(']'):
                    try:
                        # Remove brackets and split by comma
                        array_content = value[1:-1]
                        if array_content.strip():
                            value = [item.strip() for item in array_content.split(',')]
                        else:
                            value = []
                    except:
                        value = []
                # Handle quoted strings
                elif value.startswith('"') and value.endswith('"'):
                    value = value[1:-1]
                elif value.startswith("'") and value.endswith("'"):
                    value = value[1:-1]
                
                tags[key] = value
            
    except Exception as e:
        print(f"⚠️  Warning: Could not parse frontmatter from {file_path}: {e}")
        return {}
    
    return tags

def extract_tags_from_frontmatter(frontmatter):
    """Extract all possible tags from frontmatter for styling."""
    tags = []
    
    # Direct tag fields
    tag_fields = ['type', 'status', 'level', 'visibility']
    for field in tag_fields:
        if field in frontmatter:
            value = frontmatter[field]
            if isinstance(value, str):
                tags.append(f"{field}:{value}")
    
    # Handle topics array
    if 'topics' in frontmatter:
        topics = frontmatter['topics']
        if isinstance(topics, list):
            for topic in topics:
                if isinstance(topic, str) and ':' in topic:
                    tags.append(topic)
    
    return tags

def apply_styling_to_node(tags, style_config):
    """Apply styling to a node based on tags and style config."""
    styles = {
        'icon': None,
        'border_color': None,
        'background_color': None,
        'text_color': None,
        'border_style': None,
        'border_width': None,
        'clickable': True,
        'exclude': False
    }
    
    # Apply styles from matching tags
    for tag in tags:
        if tag in style_config.get('tags', {}):
            tag_style = style_config['tags'][tag]
            for style_key, style_value in tag_style.items():
                if style_key in styles:
                    # For conflicts, use the first matching tag's style
                    if styles[style_key] is None:
                        styles[style_key] = style_value
    
    return styles

def create_mermaid_node_style(styles):
    """Create Mermaid-compatible styling for a node."""
    style_parts = []
    
    if styles.get('background_color'):
        style_parts.append(f"fill:{styles['background_color']}")
    
    if styles.get('border_color'):
        border_style = styles.get('border_style') or 'solid'
        border_width = styles.get('border_width') or '2px'
        style_parts.append(f"stroke:{styles['border_color']}")
        style_parts.append(f"stroke-width:{border_width}")
        style_parts.append(f"stroke-dasharray:{'5,5' if border_style == 'dashed' else '1,1' if border_style == 'dotted' else '0'}")
    
    if styles.get('text_color'):
        style_parts.append(f"color:{styles['text_color']}")
    
    return ",".join(style_parts) if style_parts else None

def create_node_label(title, styles, is_external=False, external_url=None):
    """Create the label for a node with optional icon and external link."""
    label_parts = []
    
    # Add icon if specified
    if styles['icon']:
        label_parts.append(styles['icon'])
    
    # Add title
    safe_title = title.replace('"', "'")  # avoid breaking Mermaid syntax
    label_parts.append(safe_title)
    
    # Add external link indicator
    if is_external:
        label_parts.append("🔗")
    
    label = " ".join(label_parts)
    
    # Wrap in HTML link if external
    if is_external and external_url:
        return f"<a href='{external_url}' target='_blank' rel='noopener noreferrer'>{label}</a>"
    
    return label

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
    # Load style configuration once
    style_config = load_style_config()
    
    lines = []
    clicks = []
    classes = {}
    style_classes = {}  # For custom styling

    current_id = normalize_id(rel_path or "root")
    label = strip_order_prefix(os.path.basename(folder_path)).replace("-", " ").title() or "Home"
    lines.append(f'{current_id}["{label}"]')

    if rel_path:
        clean_rel_path = "/".join(strip_order_prefix(p) for p in rel_path.split(os.sep))
        clicks.append(f'click {current_id} "/docs/{clean_rel_path}"')

    if parent_id:
        lines.append(f"{parent_id} --> {current_id}")

    if depth >= MAX_DEPTH:
        return lines, clicks, {current_id: depth}, style_classes

    entries = sorted(os.listdir(folder_path))
    for entry in entries:
        full_path = os.path.join(folder_path, entry)
        entry_rel_path = os.path.join(rel_path, entry) if rel_path else entry

        if os.path.isdir(full_path):
            sub_lines, sub_clicks, sub_classes, sub_style_classes = build_mermaid(full_path, entry_rel_path, depth + 1, current_id)
            lines.extend(sub_lines)
            clicks.extend(sub_clicks)
            classes.update(sub_classes)
            style_classes.update(sub_style_classes)

        elif entry.endswith(".md") and entry != "index.md":
            title = extract_title(full_path)
            node_id = normalize_id(entry_rel_path)
            is_external, external_url = is_external_doc(full_path)
            
            # Parse frontmatter and apply styling
            frontmatter = parse_frontmatter(full_path)
            tags = extract_tags_from_frontmatter(frontmatter)
            styles = apply_styling_to_node(tags, style_config)
            
            # Skip excluded nodes
            if styles['exclude']:
                continue
            
            # Create node label with styling
            node_label = create_node_label(title, styles, is_external, external_url)
            lines.append(f'{node_id}["{node_label}"]')
            
            # Add click handler if clickable and not external
            if styles['clickable'] and not is_external:
                clean_entry_path = "/docs/" + "/".join(strip_order_prefix(p) for p in entry_rel_path.replace(".md", "").split(os.sep))
                clicks.append(f'click {node_id} "{clean_entry_path}"')
            
            # Add connection to parent
            lines.append(f"{current_id} --> {node_id}")

            # Apply custom styling if any
            mermaid_style = create_mermaid_node_style(styles)
            if mermaid_style:
                style_classes[node_id] = mermaid_style

            classes[node_id] = depth + 1

    classes[current_id] = depth
    return lines, clicks, classes, style_classes

def generate_index_md(folder_path, rel_path):
    folder_name = os.path.basename(folder_path)
    human_title = strip_order_prefix(folder_name).replace("-", " ").title() or "Home"

    frontmatter = f"---\ntitle: {human_title}\nhide_title: true\n---"

    # Insert intro.md content if present
    intro_md_path = os.path.join(folder_path, "intro.md")
    intro_content = ""
    if os.path.isfile(intro_md_path):
        with open(intro_md_path, "r", encoding="utf-8") as f:
            intro_content = f.read().strip()

    # Use a class-based version of the helper text for better compatibility
    custom_intro = [
        f"### {human_title}",
        '<p class=\"margin-top-negative\"><em>Click any block below to navigate directly to that section.</em></p>',
        ""
    ]

    lines, clicks, classes, style_classes = build_mermaid(folder_path, rel_path, depth=0)

    class_lines = []
    
    # Create depth-based color classes (fallback styling)
    for d in range(MAX_DEPTH + 1):
        color = ["#b3d9ff", "#d5b3ff", "#ffcccc", "#ffd699", "#d0f0c0"][d % 5]
        class_lines.append(f"classDef col{d} fill:{color},stroke:none;")
    
    # Apply depth-based classes to nodes without custom styling
    for node_id, col in classes.items():
        if node_id not in style_classes:
            class_lines.append(f"class {node_id} col{col};")
    
    # Create and apply custom style classes
    style_counter = 0
    for node_id, style in style_classes.items():
        style_class_name = f"custom{style_counter}"
        class_lines.append(f"classDef {style_class_name} {style};")
        class_lines.append(f"class {node_id} {style_class_name};")
        style_counter += 1

    output = [
        frontmatter,
        DO_NOT_EDIT,
        ""
    ]
    if intro_content:
        output.append(intro_content)
        output.append("")
    output += custom_intro + [
        "```mermaid",
        "graph LR",
    ] + lines + clicks + class_lines + [
        "linkStyle default interpolate basis",
        "```"
    ]

    # Load style config for legend
    style_config = load_style_config()
    
    # Create compact legend
    legend_items = create_compact_legend(style_classes, style_config)
    if legend_items:
        output.extend(legend_items)

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

def color_to_dot(color):
    """Map a color name to a colored dot emoji."""
    color = color.lower()
    color_map = {
        'red': '🔴',
        'orange': '🟠',
        'yellow': '🟡',
        'green': '🟢',
        'blue': '🔵',
        'purple': '🟣',
        'pink': '🩷',  # closest available
        'black': '⚫',
        'white': '⚪',
        'grey': '⚪',  # no grey dot, use white
        'gray': '⚪',
        # fallback for custom colors
    }
    # Try to match CSS hex colors to a dot (very basic)
    if color.startswith('#'):
        # Could do more advanced mapping here
        return '⬤'
    return color_map.get(color, '⬤')

def create_compact_legend(style_classes, style_config):
    """Create a compact legend showing all styles from the config, with color dots for border/background."""
    legend_items = []
    for tag, tag_config in style_config.get('tags', {}).items():
        icon = tag_config.get('icon', '')
        border_color = tag_config.get('border_color', '')
        background_color = tag_config.get('background_color', '')
        border_dot = color_to_dot(border_color) if border_color else ''
        background_dot = color_to_dot(background_color) if background_color else ''
        visual_parts = []
        if icon:
            visual_parts.append(icon)
        if border_dot:
            visual_parts.append(f"border:{border_dot}")
        if background_dot:
            visual_parts.append(f"bg:{background_dot}")
        visual = " ".join(visual_parts) if visual_parts else "•"
        legend_items.append(f"**{visual}** {tag}")
    if not legend_items:
        return []
    legend_text = " | ".join(legend_items)
    return [
        "",
        f"<small><strong>Legend:</strong> {legend_text}</small>"
    ]

walk_folders()
