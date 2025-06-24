---
title: Initializing an ADK Agent
type: how-to
level: beginner
topics: [agents, initialization, setup]
status: published
visibility: public
author:
  - John Smith (@johnsmith)
  - Jane Doe (@janedoe)
---

This guide walks through creating a basic ADK agent from scratch, using the default configuration.

```java
Agent agent = new AgentBuilder().withName("DemoAgent").build();
agent.start();
```

It’s intended for first-time users and educators wanting a minimal reproducible example.

---
