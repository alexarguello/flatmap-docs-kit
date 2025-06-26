import os
import re
import datetime
import json
from util import parse_frontmatter, normalize_id, strip_order_prefix, get_section_title, build_url_path, extract_title, parse_ymd_date, get_file_modification_date_as_date, make_breadcrumb_to_article, make_breadcrumb_to_contribute_page, make_dashboard_breadcrumb_link, make_full_breadcrumb, load_style_config, get_docs_root_dir, extract_tags_from_frontmatter

ROOT_DIR = get_docs_root_dir()
OUTPUT_DIR = os.path.join(ROOT_DIR, "99-contribute")
TEMPLATE_PATH = os.path.join(os.path.dirname(__file__), "contribute-page-template.md")
DASHBOARD_TEMPLATE_PATH = os.path.join(os.path.dirname(__file__), "contribute-dashboard-template.md")
DASHBOARD_OUTPUT_PATH = os.path.join(OUTPUT_DIR, "index.md")
CONTRIBUTING_MD_PATH = os.path.abspath(os.path.join(os.getcwd(), "../CONTRIBUTING.md"))
CONTRIB_GUIDE_OUTPUT_PATH = os.path.join(OUTPUT_DIR, "contributing-new-resource.md")

def load_template():
    with open(TEMPLATE_PATH, "r", encoding="utf-8") as f:
        return f.read()

def load_dashboard_template():
    with open(DASHBOARD_TEMPLATE_PATH, "r", encoding="utf-8") as f:
        return f.read()

def get_repository_link():
    """Get the repository link from style config."""
    style_config = load_style_config()
    return style_config.get("repository_link", "https://github.com/YOUR_ORG/YOUR_REPO")

def clean_contribute_folder():
    if not os.path.exists(OUTPUT_DIR):
        return
    for fname in os.listdir(OUTPUT_DIR):
        if fname.endswith(".md") and fname != "contributing-new-resource.md":
            os.remove(os.path.join(OUTPUT_DIR, fname))

def create_section_links(rel_path_folder):
    parts = rel_path_folder.split(os.sep)
    links = []
    url_parts = []
    for i, part in enumerate(parts):
        url_parts.append(strip_order_prefix(part))
        current_folder_path = os.path.join(ROOT_DIR, *parts[:i+1])
        title = get_section_title(current_folder_path)
        url_path = build_url_path(parts[:i+1])
        links.append(f'<a href="/docs/{url_path}" target="_blank" rel="noopener noreferrer">{title}</a>')
    return " > ".join(links)

def get_sibling_summaries(folder_path, current_filename):
    siblings = []
    for fname in sorted(os.listdir(folder_path)):
        if not fname.endswith(".md") or fname == current_filename:
            continue
        fpath = os.path.join(folder_path, fname)
        title = extract_title(fpath)
        fm = parse_frontmatter(fpath)
        status = fm.get("status", "?")
        url_path = os.path.relpath(fpath, ROOT_DIR).replace(os.sep, "/").replace(".md", "")
        link = f'<a href="/docs/{url_path}" target="_blank" rel="noopener noreferrer">{title}</a>'
        status_desc = {
            "missing": "missing",
            "draft": "in progress", 
            "review-needed": "review needed",
            "published": "published"
        }.get(status, "")
        status_icon = {
            "missing": "❌",
            "draft": "📝",
            "review-needed": "🕵️",
            "published": "✅"
        }.get(status, None)
        status_text = f" - {status_desc}" if status_desc else ""
        if status_icon:
            siblings.append(f"- {status_icon} {link} ({fname}){status_text}")
        else:
            siblings.append(f"- {link} ({fname})")
    return "\n".join(siblings) or "_No other articles in this folder yet._"

def make_breadcrumb_from_root(rel_path, article_title=None, link_to_article=True):
    # rel_path: e.g. 20-agent-frameworks/langgraph4j/get-started.md
    parts = rel_path.split(os.sep)
    # Remove .md from last part
    if parts[-1].endswith('.md'):
        parts[-1] = parts[-1][:-3]
    # Build clickable breadcrumbs from root
    crumbs = []
    for i, part in enumerate(parts[:-1]):
        folder_path = os.path.join(ROOT_DIR, *parts[:i+1])
        title = get_section_title(folder_path)
        url_path = build_url_path(parts[:i+1])
        crumbs.append(f'<a href="/docs/{url_path}" target="_blank" rel="noopener noreferrer">{title}</a>')
    # Article part
    art_title = article_title if article_title else extract_title(os.path.join(ROOT_DIR, rel_path))
    if link_to_article:
        url_path = build_url_path(parts)
        crumbs.append(f'<a href="/docs/{url_path}" target="_blank" rel="noopener noreferrer">{art_title}</a>')
    else:
        crumbs.append(art_title)
    return " > ".join(crumbs)

def create_contribution_page(md_path, rel_path, frontmatter):
    title = frontmatter.get("title", os.path.basename(md_path).replace(".md", ""))
    id = f"contribute-{normalize_id(rel_path)}"
    filename = os.path.basename(md_path)
    rel_path_folder = os.path.dirname(rel_path)
    abs_folder_path = os.path.join(ROOT_DIR, rel_path_folder)

    # Section links: upstream folders only (breadcrumb, all clickable, no article)
    parts = rel_path.split(os.sep)
    if parts[-1].endswith('.md'):
        parts[-1] = parts[-1][:-3]
    if len(parts) > 1:
        section_links = []
        for i in range(len(parts)-1):
            folder_path = os.path.join(ROOT_DIR, *parts[:i+1])
            folder_title = get_section_title(folder_path)
            url_path = build_url_path(parts[:i+1])
            section_links.append(f'<a href="/docs/{url_path}" target="_blank" rel="noopener noreferrer">{folder_title}</a>')
        section_links = " > ".join(section_links)
    else:
        section_links = ""

    # Article link: just the article title, clickable, links to the article
    url_path = build_url_path(parts)
    article_link = f'<a href="/docs/{url_path}" target="_blank" rel="noopener noreferrer">{title}</a>'

    # Sibling articles (skip intro.md and index.md)
    sibling_articles = []
    for fname in sorted(os.listdir(abs_folder_path)):
        if not fname.endswith(".md") or fname == filename or fname in ("intro.md", "index.md"):
            continue
        fpath = os.path.join(abs_folder_path, fname)
        sib_fm = parse_frontmatter(fpath)
        # Use frontmatter title first, then fall back to extracted title
        sib_title = sib_fm.get("title", extract_title(fpath))
        status = sib_fm.get("status", "?")
        sib_rel_path = os.path.relpath(fpath, ROOT_DIR)
        link = make_full_breadcrumb(sib_rel_path, article_title=sib_title, root_dir=ROOT_DIR)
        status_desc = {
            "missing": "missing",
            "draft": "in progress", 
            "review-needed": "review needed",
            "published": "published"
        }.get(status, "")
        status_icon = {
            "missing": "❌",
            "draft": "📝",
            "review-needed": "🕵️",
            "published": "✅"
        }.get(status, None)
        status_text = f" - {status_desc} {status_icon}" if status_desc and status_icon else ""
        sibling_articles.append(f"- {link}{status_text}")
    sibling_articles_md = "\n".join(sibling_articles) or "_No other articles in this folder yet._"

    file_edit_link = f"{get_repository_link()}/edit/main/docs/{rel_path_folder}/{filename}"

    template = load_template()
    content = template.format(
        title=title,
        id=id,
        section_links=section_links,
        article_link=article_link,
        rel_path_folder=rel_path_folder,
        filename=filename,
        sibling_articles=sibling_articles_md,
        file_edit_link=file_edit_link
    )

    output_path = os.path.join(OUTPUT_DIR, id + ".md")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"✅ Created: {output_path}")

def extract_contrib_guide():
    # Extract the section from CONTRIBUTING.md
    if not os.path.exists(CONTRIBUTING_MD_PATH):
        print(f"⚠️ CONTRIBUTING.md not found at {CONTRIBUTING_MD_PATH}")
        return
    with open(CONTRIBUTING_MD_PATH, "r", encoding="utf-8") as f:
        lines = f.readlines()
    start = None
    end = None
    for i, line in enumerate(lines):
        if line.strip().startswith("## 📝 How to Add a New Resource"):
            start = i
            break
    if start is None:
        print("⚠️ Could not find '## 📝 How to Add a New Resource' section in CONTRIBUTING.md")
        return
    for j in range(start+1, len(lines)):
        if lines[j].strip().startswith("## "):
            end = j
            break
    section = lines[start:end] if end else lines[start:]
    # Write to output file with Docusaurus frontmatter
    with open(CONTRIB_GUIDE_OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write("---\ntitle: Contributor Guide for New Articles\nsidebar_label: New Article Guide\nhide_title: false\n---\n\n")
        f.writelines(section)
    print(f"✅ Wrote: {CONTRIB_GUIDE_OUTPUT_PATH}")

def walk_docs():
    clean_contribute_folder()
    extract_contrib_guide()
    
    # Import collaboration page creation function
    try:
        import sys
        import os
        sys.path.append(os.path.dirname(__file__))
        from generate_collaborate_pages import create_collaboration_page, get_author_info, create_location_breadcrumb, create_discussion_link, get_suggested_contributions, load_style_config
    except ImportError as e:
        print(f"⚠️  Collaboration page generator not available: {e}")
        create_collaboration_page = None
    
    # Import review page creation function
    try:
        from generate_review_pages import create_review_page
    except ImportError as e:
        print(f"⚠️  Review page generator not available: {e}")
        create_review_page = None
    
    # Dashboard data collection
    today = datetime.date.today()
    priority_map = {"high": "🔥", "medium": "❤️", "": "🤲"}
    gaps_by_priority = {"high": [], "medium": [], "": []}
    collaboration_articles = []
    review_articles = []
    recent_articles = []
    
    for root, _, files in os.walk(ROOT_DIR):
        for f in files:
            if f.endswith(".md") and not f.startswith("."):
                abs_path = os.path.join(root, f)
                rel_path = os.path.relpath(abs_path, ROOT_DIR)
                
                # Skip index.md files if there's a corresponding _intro.md file
                if f == "index.md":
                    intro_path = os.path.join(root, "_intro.md")
                    if os.path.exists(intro_path):
                        print(f"⏭️  Skipping {rel_path} (has corresponding _intro.md)")
                        continue
                
                frontmatter = parse_frontmatter(abs_path)
                
                # Normalize all frontmatter keys to lowercase
                frontmatter = {k.lower(): v for k, v in frontmatter.items()}
                status = frontmatter.get("status", None)
                collaboration = frontmatter.get("collaboration", "")
                author = frontmatter.get("author", "")
                
                # Check if author exists (handle string format: "Name" (@github), "Name" (@github))
                has_author = False
                if isinstance(author, str) and author.strip():
                    has_author = True
                
                article = {
                    'abs_path': abs_path,
                    'rel_path': rel_path,
                    'title': frontmatter.get('title', extract_title(abs_path)),
                    'status': status,
                    'author': author,
                    'priority': frontmatter.get('priority', ''),
                    'article-priority': frontmatter.get('article-priority', ''),
                    'collaboration': collaboration,
                    'collaboration-topic': frontmatter.get('collaboration-topic', ''),
                    'review-reason': frontmatter.get('review-reason', ''),
                    'eta': frontmatter.get('eta', ''),
                    'modified': frontmatter.get('modified', None)
                }
                
                # Page generation and dashboard data collection in one loop
                if status == "missing":
                    if not author:
                        # Create contribute page for unclaimed articles
                        create_contribution_page(abs_path, rel_path, frontmatter)
                        # Collect for high impact gaps (same logic as before)
                        prio = frontmatter.get('article-priority', '')
                        prio = prio.strip().lower() if isinstance(prio, str) else ""
                        if prio not in gaps_by_priority:
                            prio = ""
                        gaps_by_priority[prio].append(article)
                    elif collaboration == "open" and has_author:
                        # Create collaboration page for claimed articles open for collaboration
                        if create_collaboration_page:
                            style_config = load_style_config()
                            create_collaboration_page(abs_path, rel_path, frontmatter, style_config)
                            collaboration_articles.append(article)
                        else:
                            print(f"⚠️  Cannot create collaboration page for {rel_path} - collaboration generator not available")
                elif status in ["draft", "wip", "review-needed"] and collaboration == "open" and has_author:
                    # Create collaboration page for in-progress articles open for collaboration
                    if create_collaboration_page:
                        style_config = load_style_config()
                        create_collaboration_page(abs_path, rel_path, frontmatter, style_config)
                        collaboration_articles.append(article)
                    else:
                        print(f"⚠️  Cannot create collaboration page for {rel_path} - collaboration generator not available")
                
                # Collect other dashboard data (same logic as before)
                if status == "review-needed":
                    review_articles.append(article)
                    # Create review page for articles needing review
                    if create_review_page:
                        style_config = load_style_config()
                        create_review_page(abs_path, rel_path, frontmatter, style_config)
                    else:
                        print(f"⚠️  Cannot create review page for {rel_path} - review generator not available")
                elif status == "published":
                    mod_date = None
                    if 'modified' in article and article['modified']:
                        mod_date = parse_ymd_date(article['modified'])
                    if not mod_date:
                        mod_date = get_file_modification_date_as_date(article['abs_path'])
                    if mod_date and (today - mod_date).days <= 14:
                        recent_articles.append(article)
    
    print(f"📊 Found {len(collaboration_articles)} articles open for collaboration")
    
    # Generate dashboard tables (exact same logic as before)
    gap_rows = []
    for prio in ["high", "medium", ""]:
        prio_icon = priority_map[prio]
        grouped = {}
        for art in gaps_by_priority[prio]:
            parts = art['rel_path'].split(os.sep)
            subfolder = "/".join(parts[:-1][-2:]) if len(parts) > 2 else "/".join(parts[:-1])
            grouped.setdefault(subfolder, []).append(art)
        for subfolder in sorted(grouped):
            for art in grouped[subfolder]:
                link = make_dashboard_breadcrumb_link(art['rel_path'], article_title=art['title'], to_contribute_page=True, root_dir=ROOT_DIR)
                gap_rows.append(f'| {prio_icon} | {link} |')
    high_impact_gaps_table = '\n'.join(gap_rows) if gap_rows else '| _No high-impact gaps!_ |  |'

    collabs = []
    for art in collaboration_articles:
        # Create breadcrumb link with max 2 upstream folders like contribute section
        parts = art['rel_path'].split(os.sep)
        if parts[-1].endswith('.md'):
            parts[-1] = parts[-1][:-3]
        upstreams = parts[:-1][-2:]  # Max 2 upstreams
        crumb_text = []
        for i, part in enumerate(upstreams):
            folder_path = os.path.join(ROOT_DIR, *parts[:-(len(upstreams)-i)])
            title = get_section_title(folder_path)
            crumb_text.append(title)
        art_title = art['title']
        crumb_text.append(art_title)
        text = " > ".join(crumb_text)
        
        # Create link to the collaboration page
        collab_id = f"collaborate-{normalize_id(art['rel_path'])}"
        collab_link = f'<a href="/docs/contribute/{collab_id}" target="_blank" rel="noopener noreferrer">{text}</a>'
        
        author = art.get('author', '')
        eta = art.get('eta', '')
        collaboration_topic = art.get('collaboration-topic', 'Help needed')
        collabs.append(f'| {collab_link} | {author} | {eta} | {collaboration_topic} |')
    open_to_collaboration_table = '\n'.join(collabs) if collabs else '| _No open collaborations!_ |  |  |  |'

    reviews = []
    for art in review_articles:
        # Create breadcrumb link with max 2 upstream folders like contribute section
        parts = art['rel_path'].split(os.sep)
        if parts[-1].endswith('.md'):
            parts[-1] = parts[-1][:-3]
        upstreams = parts[:-1][-2:]  # Max 2 upstreams
        crumb_text = []
        for i, part in enumerate(upstreams):
            folder_path = os.path.join(ROOT_DIR, *parts[:-(len(upstreams)-i)])
            title = get_section_title(folder_path)
            crumb_text.append(title)
        art_title = art['title']
        crumb_text.append(art_title)
        text = " > ".join(crumb_text)
        
        # Create link to the review page
        review_id = f"review-{normalize_id(art['rel_path'])}"
        review_link = f'<a href="/docs/contribute/{review_id}" target="_blank" rel="noopener noreferrer">{text}</a>'
        
        # Get review reason
        review_reason = art.get('review-reason', 'Needs review')
        reviews.append(f'| {review_link} | {review_reason} |')
    needs_review_table = '\n'.join(reviews) if reviews else '| _No articles need review!_ |  |'

    recents = []
    for art in recent_articles:
        link = make_dashboard_breadcrumb_link(art['rel_path'], article_title=art['title'], to_contribute_page=False, root_dir=ROOT_DIR)
        recents.append(f'| {link} |')
    recently_published_table = '\n'.join(recents) if recents else '| _No recent articles!_ |'

    # Generate dashboard (same as before)
    dashboard_template = load_dashboard_template()
    dashboard_content = dashboard_template.format(
        high_impact_gaps_table=high_impact_gaps_table,
        open_to_collaboration_table=open_to_collaboration_table,
        needs_review_table=needs_review_table,
        recently_published_table=recently_published_table
    )
    with open(DASHBOARD_OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write(dashboard_content)
    print(f"✅ Dashboard written: {DASHBOARD_OUTPUT_PATH}")

if __name__ == "__main__":
    clean_contribute_folder()
    extract_contrib_guide()
    walk_docs()