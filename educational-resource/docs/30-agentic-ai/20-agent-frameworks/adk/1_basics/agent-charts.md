---
title: "Agent Lifecycle Charts"
sidebar_position: 2
hide_title: true

# REQUIRED TAGS — fill in all of these:

level: intermediate      # beginner / intermediate / advanced / expert
type: overview         # tutorial / overview / code / benchmark / opinion / api-doc
status: review-needed   # draft / review-needed / published / missing
visibility: public     # public

topics:
  - adk
  - agent-lifecycle
  - charts
  - java

# 🧩 OPTIONAL TAGS:

# article-priority: high
# high / medium — omit if not important

# collaboration: open
# set if author welcomes collaborators
# collaboration-topic: "need help implementing Spring Boot starter examples"  
#                        # explain what help is welcome (appears on the dashboard & collab page)

review-reason: "seems not to be on the right topic"
#                        # required when status: review-needed — will show on the article and in the dashboard

author: "Lize Raes (@lizeraes)"

# eta: 2025-07-01
# Set only if status is draft

# Feature-related tags (only if this doc describes a feature or gap in Java+AI):
# feature-status: preview
# missing / experimental / preview / stable / specified
# feature-priority: high
# suggested / medium / high
# feature-responsible: openjdk
# community / openjdk / oracle-architects / jsr / vendor:redhat / project-lead:<name>
---

# Agent Lifecycle Charts

Visual representations of the ADK agent lifecycle, showing the different states and transitions that agents go through during their execution. These charts help developers understand the agent's behavior and debug issues.

The agent lifecycle consists of several key states: Initialized, Running, Processing, Idle, and Terminated. Each state represents a different phase of the agent's operation, with specific transitions triggered by events like receiving a message, completing a task, or encountering an error.

Understanding these lifecycle charts is essential for building robust agents and implementing proper error handling and recovery mechanisms.

```java
agent.on("init", () -> {
    logger.info("Agent initialized");
});
```
You'll learn how to render transitions and triggers using the ADK's lifecycle hooks and logging API.

---