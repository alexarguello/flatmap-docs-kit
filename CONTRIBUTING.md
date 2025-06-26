# 🤝 Contributing to Java & AI Resource Hub

Thanks for helping build the most useful, well-structured resource landscape for Java and AI!

We aim to make the resource:

- **Easy to navigate**, even at depth
- **Structured**, tagged, and filterable
- **Low maintenance**, yet dynamically visualized
- **Equally useful for beginners and experts**

---

## 📝 How to Add a New Resource

Not sure where to start? Have a look at the last topic in the sidebar, `Contribute` for a dashboard with resources / reviews we'd love to have. If you have your own idea, go ahead as follow:

1. Find the correct folder inside [`/docs/`](./docs)
2. Copy the [`docs/.template.md`](./docs/.template.md) into that folder
3. Rename the file (e.g., `overview.md`, `setup-guide.md`, etc.). Attention: `intro.md` and `index.md are reserved.
4. Fill in the frontmatter (YAML block at the top) as described in the template
5. Make a PR 🙌 

---

## ✍️ Metadata: Required & Optional Tags

**All required and optional metadata fields are documented directly in [`docs/.template.md`](./docs/.template.md)**.

Please follow that template closely — it includes:

- Required fields like `title`, `type`, `level`, `status`, `topics`, etc.
- Optional fields like `author`, `eta`, `feature-priority`, `feature-responsible`, etc.
- Tagging examples and allowed values

These tags ensure:

- Resources are **findable** and **well-classified**
- Flatmaps and dashboards reflect up-to-date context
- Maintainers can triage what’s missing or in progress

**Some tags are visualized** on the site:
- `level` and `type` may impact box **borders**, **colors**, or **icons**
- `status` will guide visual styling for clarity (`wip`, `published`, etc.)

---

## 📌 About `intro.md` Pages

Each folder can contain a `intro.md` file that:

- Serves as the **landing page** for that topic
- Appears **above the visual “flatmap” diagram**
- Should be **short and to the point** (2–3 paragraphs max)
- The flatmap that comes after should remain **partially visible without scrolling**, so viewers realize it's there
- Should **dispatch readers** toward subtopics depending on their persona:
    - **Expected readers**: new to the topic / experienced / educators

We recommend thinking of the `intro.md` as a **landing tile or dispatch hub**. It helps the user orient themselves before diving into the deeper levels of the structure.

Please limit subfolders to 4, max 5. If adding more, try to group in a new subfolder.

---

## ✅ Pull Request Guidelines

We will soon enable **automated PR checks** that validate:

- Presence of all required fields
- Correct format of tag values (e.g., known `type`, valid `visibility`)
- Optional `eta` only present if `status` is `planned` or `wip`

If your PR is missing tags or uses incorrect values, the check will comment with what’s wrong.

---

### ⏳ Claimed or Planned Resources

When marking a resource as `status: planned` or `status: wip`, you **must include** an estimated completion date via the `eta` field (see example in [`docs/.template.md`](./docs/.template.md))

This allows us to:

- **Send automatic reminders** to contributors and maintainers when a resource is overdue
- Keep the roadmap and site fresh and realistic
- Help others avoid duplicate efforts

⏰ ETA can be updated later if needed — it's not punishment, just visibility 🙂

---

Thanks again for contributing 🙌  
If you have ideas, improvements, or need support, open a Discussion or contact the maintainers.
