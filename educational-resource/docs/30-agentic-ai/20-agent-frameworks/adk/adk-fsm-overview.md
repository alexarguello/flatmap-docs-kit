---
title: "Finite State Machines in ADK"
sidebar_position: 3
hide_title: true

# REQUIRED TAGS — fill in all of these:

level: intermediate      # beginner / intermediate / advanced / expert
type: overview         # tutorial / overview / code / benchmark / opinion / api-doc
status: published      # draft / review-needed / published / missing
visibility: public     # public

topics:
  - adk
  - fsm
  - design-patterns
  - java

# 🧩 OPTIONAL TAGS:

# article-priority: high   # high / medium — omit if not important

# collaboration: open      # set if author welcomes collaborators
# collaboration-topic: "need help implementing Spring Boot starter examples"  
#                        # explain what help is welcome (appears on the dashboard & collab page)

# review-reason: "seems not to be on the right topic"
#                        # required when status: review-needed — will show on the article and in the dashboard

author: "Dr. Alice Nguyen (@aliceng)"

# eta: 2025-07-01           # Set only if status is draft

# Feature-related tags (only if this doc describes a feature or gap in Java+AI):
# feature-status: preview        # missing / experimental / preview / stable / specified
# feature-priority: high         # suggested / medium / high
# feature-responsible: openjdk   # community / openjdk / oracle-architects / jsr / vendor:redhat / project-lead:<name>
---

# Finite State Machines in ADK

Finite State Machines (FSMs) are at the core of ADK's logic coordination model. This overview introduces how states and transitions are declared and managed within the ADK framework.

ADK uses FSMs to model agent behavior and coordinate complex workflows. Each agent can have multiple states representing different phases of operation, with transitions triggered by events or conditions. This approach provides clear structure and predictable behavior for agent interactions.

```java
fsm.state("Idle")
   .on("Start", "Running");

fsm.state("Running")
   .on("Stop", "Idle");
```

