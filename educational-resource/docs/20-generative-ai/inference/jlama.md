---
title: "Jlama"
sidebar_position: 1
hide_title: true

# REQUIRED TAGS — fill in all of these:

level: intermediate      # beginner / intermediate / advanced / expert
type: overview         # tutorial / overview / code / benchmark / opinion / api-doc
status: draft          # draft / review-needed / published / missing
visibility: public     # public

topics:
  - jlama
  - local-inference
  - llama
  - java

# 🧩 OPTIONAL TAGS:

# article-priority: high   # high / medium — omit if not important

# collaboration: open      # set if author welcomes collaborators
# collaboration-topic: "need help implementing Spring Boot starter examples"  
#                        # explain what help is welcome (appears on the dashboard & collab page)

# review-reason: "seems not to be on the right topic"
#                        # required when status: review-needed — will show on the article and in the dashboard

author: "Lize Raes (@lizeraes)"

eta: 2025-07-01           # Set only if status is draft

# Feature-related tags (only if this doc describes a feature or gap in Java+AI):
# feature-status: preview        # missing / experimental / preview / stable / specified
# feature-priority: high         # suggested / medium / high
# feature-responsible: openjdk   # community / openjdk / oracle-architects / jsr / vendor:redhat / project-lead:<name>
---

# Jlama

Jlama is a Java library for running Llama models locally with high performance and low memory usage. It provides a native Java interface to the Llama inference engine, enabling developers to integrate local LLM capabilities into their Java applications.

The library supports various Llama model formats and provides optimized inference for both CPU and GPU environments. Jlama is particularly useful for applications requiring offline AI capabilities or when you need to maintain full control over the inference process.
