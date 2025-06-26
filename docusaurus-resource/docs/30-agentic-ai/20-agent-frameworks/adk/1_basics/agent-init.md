---
title: "Initializing an ADK Agent"
sidebar_position: 1
hide_title: true

# REQUIRED TAGS — fill in all of these:

level: beginner        # beginner / intermediate / advanced / expert
type: tutorial         # tutorial / overview / code / benchmark / opinion / api-doc
status: review-needed   # draft / review-needed / published / missing
visibility: public     # public

topics:
  - adk
  - agent-initialization
  - setup
  - java

# 🧩 OPTIONAL TAGS:

article-priority: high   # high / medium — omit if not important

# collaboration: open
# set if author welcomes collaborators
# collaboration-topic: "need help implementing Spring Boot starter examples"  
#                        # explain what help is welcome (appears on the dashboard & collab page)

review-reason: "needs more detailed error handling examples and configuration options"
#                        # required when status: review-needed — will show on the article and in the dashboard

author: ["John Smith (@johnsmith)", "Jane Doe (@janedoe)"]

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

# Initializing an ADK Agent

This guide walks through creating a basic ADK agent from scratch, using the default configuration. You'll learn how to set up the agent lifecycle, configure basic parameters, and start your first agent instance.

ADK (Agent Development Kit) provides a comprehensive framework for building production-ready AI agents. The initialization process involves creating an agent builder, configuring the agent's capabilities, and starting the agent lifecycle. Here's a simple example:

```java
Agent agent = new AgentBuilder()
    .withName("DemoAgent")
    .withModel("gpt-4")
    .withTools(Arrays.asList(new CalculatorTool(), new WeatherTool()))
    .build();
agent.start();
```

This creates a basic agent with a name, language model, and a set of tools. The agent will be ready to process requests and execute tasks using the configured tools and model.
