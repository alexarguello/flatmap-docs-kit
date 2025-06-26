---
title: "Agent Benchmarking Guide"
sidebar_position: 4
hide_title: true

# REQUIRED TAGS — fill in all of these:

level: advanced        # beginner / intermediate / advanced / expert
type: benchmark        # tutorial / overview / code / benchmark / opinion / api-doc
status: published      # draft / review-needed / published / missing
visibility: public     # public

topics:
  - adk
  - benchmarking
  - performance
  - java

# 🧩 OPTIONAL TAGS:

# article-priority: high   # high / medium — omit if not important

collaboration: open      # set if author welcomes collaborators
collaboration-topic: "need help with additional benchmarking scenarios and performance optimization techniques"  
#                        # explain what help is welcome (appears on the dashboard & collab page)

# review-reason: "seems not to be on the right topic"
#                        # required when status: review-needed — will show on the article and in the dashboard

author: "Jane Doe (@janedoe)"

# eta: 2025-07-12           # Set only if status is draft

# Feature-related tags (only if this doc describes a feature or gap in Java+AI):
# feature-status: preview        # missing / experimental / preview / stable / specified
# feature-priority: high         # suggested / medium / high
# feature-responsible: openjdk   # community / openjdk / oracle-architects / jsr / vendor:redhat / project-lead:<name>
---

# Agent Benchmarking Guide

This guide covers benchmarking setups for comparing ADK agent throughput across different runtime configurations. It provides methodologies and tools for measuring agent performance in various scenarios.

The benchmarking approach uses JMH (Java Microbenchmark Harness) and custom agent event streams to provide accurate performance measurements. This enables developers to optimize their agent implementations and compare different configurations for production deployment.