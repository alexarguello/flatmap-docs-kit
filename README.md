# 🧠 AI Resource Navigator (Docusaurus + Flatmap)

This project is a template for building a **structured, deep, and navigable technical knowledge base**—perfect for documentation, developer onboarding, industry insight sharing, and feature roadmapping.

---

## 🚀 Why This Is Cool

- 🗺️ **Each folder (or "chapter") gets its own visual flatmap**: a clickable overview of all nested topics, up to 3 levels deep — so anyone can see the structure **at a glance** and jump directly to the content.
- 🔁 **Multiple paths to the same resource**: organize docs the way readers think, not the way folders are stored.
- 🌐 **External resources behave like first-class citizens**: they show up in the flatmap, open directly in a new tab, and are clearly marked.
- 🛠️ **Great for contributors & feature architects**: internal content, WIP notes, and roadmap items can live side by side with polished docs — and stay organized.
- 🧭 Helps both **users** and **strategists** navigate large projects with many moving parts.

> 📸 _Flatmap preview here_  
> _[insert screenshot placeholder]_

---

## 🏗 How It Works

- This uses [Docusaurus](https://docusaurus.io/) to render the contents of the docs/ folder as a static navigable site.
- Python scripts auto-generate `index.md` files with Mermaid flatmaps for each folder.
- If a folder contains an `intro.md`, it's shown above the flatmap (recommended: 1–2 paragraphs max).

---

## Build your own version

- Clone this repo
- Update docusaurus-resource/docs/.template.md with your own 'frontmatter' (header) and tags
- Drop in your own content under /docs/ (for now it is populated with sample articles)

### 🔄 External vs Internal Resources

#### Internal `.md`:
- Renders directly on the site
- Appears in flatmaps with a regular label

#### External `.md` with frontmatter:
```yaml
---
title: Official ADK Docs
type: external
link: https://docs.agent-dev-kit.org
---
```
Shows up with a 🔗 icon in the map

Clicking it takes you directly to the external site

---

## 🧪 Run It (Local Setup)

```bash
# 1. Clone
git clone https://github.com/your-username/java-ai-docs.git
cd java-ai-docs

# 2. Install
npm install

# 3. Generate flatmaps
python tools/generate-mermaids.py

# 4. Start the local site
npm run start
```

Then open: http://localhost:3000/docs

---

## 🛣️ Features Coming Soon
- Configurable tags and rendering options
- 🏷️ Tag-based views — tags will appear in flatmaps (e.g. feature, bug, tutorial)
- 📊 Dashboards — see missing docs, upcoming content, and WIP summaries
- 🤖 Chatbot integration — ask natural-language questions across your structured docs
