---
title: "Get Started with LangGraph4j"
sidebar_position: 1
hide_title: true

# REQUIRED TAGS — fill in all of these:

level: intermediate      # beginner / intermediate / advanced / expert
type: tutorial         # tutorial / overview / code / benchmark / opinion / api-doc
status: published      # draft / review-needed / published / missing
visibility: public     # public

topics:
  - langgraph4j
  - agent-frameworks
  - workflow
  - java

# 🧩 OPTIONAL TAGS:

article-priority: high   # high / medium — omit if not important

# collaboration: open      # set if author welcomes collaborators
# collaboration-topic: "need help implementing Spring Boot starter examples"  
#                        # explain what help is welcome (appears on the dashboard & collab page)

# review-reason: "seems not to be on the right topic"
#                        # required when status: review-needed — will show on the article and in the dashboard

author: "Lize Raes (@lizeraes)"

# eta: 2025-09-10           # Set only if status is draft

# Feature-related tags (only if this doc describes a feature or gap in Java+AI):
# feature-status: preview        # missing / experimental / preview / stable / specified
# feature-priority: high         # suggested / medium / high
# feature-responsible: openjdk   # community / openjdk / oracle-architects / jsr / vendor:redhat / project-lead:<name>
---

# Get Started with LangGraph4j

LangGraph4j is the Java implementation of LangGraph, enabling you to build stateful, multi-step AI applications with complex workflows. This guide will walk you through setting up your first LangGraph4j project.

## 🎯 What You'll Build

In this tutorial, you'll create a simple workflow that:
- Processes user input
- Makes decisions based on context
- Executes multiple steps in sequence
- Maintains state throughout the conversation

## 🔧 Prerequisites

Before starting, ensure you have:
- Java 17+ installed
- Maven or Gradle build tool
- Basic understanding of Java development
- An OpenAI API key (or other LLM provider)

## 📦 Project Setup

### 1. Create a New Maven Project

```xml
<dependency>
    <groupId>dev.langchain4j</groupId>
    <artifactId>langgraph4j</artifactId>
    <version>0.27.1</version>
</dependency>
```

### 2. Add LLM Provider

```xml
<dependency>
    <groupId>dev.langchain4j</groupId>
    <artifactId>langchain4j-open-ai</artifactId>
    <version>0.27.1</version>
</dependency>
```

## 🚀 Your First Workflow

Let's create a simple customer service workflow:

```java
@Slf4j
public class CustomerServiceWorkflow {
    
    private final Graph<CustomerState> graph;
    
    public CustomerServiceWorkflow() {
        this.graph = Graph.builder()
            .addNode("analyze", this::analyzeRequest)
            .addNode("route", this::routeRequest)
            .addNode("respond", this::generateResponse)
            .addEdge("analyze", "route")
            .addEdge("route", "respond")
            .build();
    }
    
    private CustomerState analyzeRequest(CustomerState state) {
        // Analyze customer request and determine intent
        log.info("Analyzing customer request: {}", state.getUserMessage());
        return state.withIntent("support_request");
    }
    
    private CustomerState routeRequest(CustomerState state) {
        // Route to appropriate handler based on intent
        log.info("Routing request with intent: {}", state.getIntent());
        return state.withHandler("general_support");
    }
    
    private CustomerState generateResponse(CustomerState state) {
        // Generate appropriate response
        log.info("Generating response for handler: {}", state.getHandler());
        return state.withResponse("Thank you for your inquiry. How can I help you today?");
    }
    
    public String processRequest(String userMessage) {
        CustomerState initialState = new CustomerState(userMessage);
        CustomerState finalState = graph.execute(initialState);
        return finalState.getResponse();
    }
}
```

## 🔄 State Management

LangGraph4j uses state objects to maintain context across workflow steps:

```java
public class CustomerState {
    private final String userMessage;
    private String intent;
    private String handler;
    private String response;
    
    // Constructor and methods...
    
    public CustomerState withIntent(String intent) {
        this.intent = intent;
        return this;
    }
    
    // Other builder methods...
}
```

## 🎉 Next Steps

Now that you have a basic workflow running, explore:
- **Conditional Routing** - Add decision nodes
- **Tool Integration** - Connect to external services
- **Memory Management** - Maintain conversation history
- **Error Handling** - Add robust error recovery

Ready to build more complex workflows? Check out our advanced tutorials!