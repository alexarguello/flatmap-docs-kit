# 📚 Java & AI Resource Hub

Welcome to the most **clickable**, **contributor-friendly**, and **carefully curated** knowledge map for **Java and Artificial Intelligence**.

This resource is:

- 🧠 Maintained by [Java Champions](https://www.javachampions.org/) and friends  
- 🚀 Built for **newcomers**, **experienced engineers**, and **educators**  
- 🧭 Structured to help you **navigate**, **compare**, and **go deep** on the right topics  
- ❤️ Always growing — with clear ways to **contribute**  
- 📦 Collects high-quality tutorials, benchmarks, comparisons, guides, and insights — curated and tagged for easy filtering  
- 🌐 A mix of specifically written articles and well-chosen external links — so you don't miss anything important  
- 🔍 TODO: Add a **search bar** for easier discovery  
- 🤖 TODO: Integrate a **chatbot** to guide users interactively  

**Jump to:**
- [How to Use the Resource](#️-how-to-use-the-resource)
- [Tag System & Styling](#-tag-system--styling)
- [How to Contribute](#️-how-to-contribute)
- [Coming Soon](#-coming-soon)

---

## 🗺️ How to Use the Resource

You can explore the content in a few ways:

### 📌 Get Started Path  
Start here if you're new to Java + AI, or want a guided path:  
→ [`/docs/getting-started`](./docs/00-getting-started)

### 🔍 Flatmaps (Clickable Topic Diagrams)  
Each folder or topic area comes with a visual **flatmap** — a clickable diagram showing what's inside, how it relates, and what's missing.

Want the full overview?  
→ [`Site Overview`](./docs/site-overview)

### 🧭 Jump to Any Section  
Browse deeply structured folders, or skim via the site's sidebar.

---

## 🏷️ Tag System & Styling

This resource uses a comprehensive tag system to visually organize and categorize content. Tags are defined in frontmatter and automatically styled in the flatmaps.

### Available Tags

#### Content Types
- `type:code` - Code samples and implementations
- `type:tutorial` - Step-by-step guides
- `type:benchmark` - Performance comparisons
- `type:api-doc` - API documentation
- `type:overview` - High-level introductions
- `type:external` - Links to external resources

#### Difficulty Levels
- `level:beginner` - Green border
- `level:intermediate` - Yellow border  
- `level:advanced` - Orange border
- `level:expert` - Red border

#### Status
- `status:draft` - Grey background
- `status:review-needed` - Grey background
- `status:published` - Default styling
- `status:missing` - Grey background
- `status:placeholder` - 🚧 icon (always shown first)

#### Special Tags
- `author:not_empty AND status:draft` - 👤 icon (appears when author field is not empty AND status is draft)
- `visibility:internal` - Excluded from public view
- `visibility:archived` - Excluded from public view

### Conditional Tags

You can use conditional logic in your frontmatter:

```yaml
---
title: My Article
author: "John Doe"
status: draft
# author:not_empty AND status:draft will be automatically added since both conditions are met
---
```

The system automatically detects:
- `author:not_empty` - When `author` field is not empty
- `author:is_empty` - When `author` field is empty or missing
- `status:draft` - When status is draft
- `status:published` - When status is published
- `field:is_empty` - When any field is empty or missing
- `field:is_not_empty` - When any field has content

### Complex Conditions (AND Logic)

You can combine conditions using AND logic in the style config:

```json
{
  "tags": {
    "author:not_empty AND status:draft": { "icon": "👤", "icon_side": "right" }
  }
}
```

This will only show the icon when BOTH conditions are true:
- `author` field is not empty
- `status` is "draft"

### Icon Positioning

Icons can be positioned on the left (default) or right side of node labels:
- `icon_side: left` - Icon appears before the title
- `icon_side: right` - Icon appears after the title

Example:
```yaml
---
title: Draft Article
author: "Jane Smith"
status: draft
# author:not_empty AND status:draft will show 👤 on the right side
---
```

---

## ✍️ How to Contribute

You can help improve this resource in multiple ways:

### ➕ Add a New Resource  
If you want to contribute a new tutorial, article, benchmark, or code sample, follow:  
→ [`CONTRIBUTING.md`](./CONTRIBUTING.md)

We explain:
- Where to place your file
- How to structure metadata
- How to submit a PR

### ❤️ See What We're Missing  
Jump to the last folder in the structure:  
→ [`Contribute`](./docs/contribute-dashboard)

There you'll find:
- 🔥 Articles we'd love to have
- 🤝 Open collaborations
- 📝 Drafts needing review
- 🆕 Recently published resources

Each entry has:
- **Click-to-claim** instructions  
- **Context so you know exactly where the resource fits in and what's expected**  
- PR examples and templates to make your life easy

---

## 🧪 Coming Soon

- 🧑‍🏫 **Maintainer Dashboard** — overdue drafts, tag warnings, folder health  
- 🧠 **Ecosystem Dashboard** — missing Java+AI features, priorities for OpenJDK, and long-term roadmap  
- 🔍 **Search** and 🤖 **chatbot** to improve discovery

---

Thanks for being part of this evolving resource.  
Your contribution helps shape the future of Java in AI. 🙌
