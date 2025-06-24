---
title: Finite State Machines in ADK
type: concept
level: intermediate
topics: [fsm, design-patterns]
status: published
visibility: public
author: Dr. Alice Nguyen (@aliceng)
---

Finite State Machines (FSMs) are at the core of ADK’s logic coordination model. This overview introduces how states and transitions are declared and managed.

```java
fsm.state("Idle")
   .on("Start", "Running");

fsm.state("Running")
   .on("Stop", "Idle");
```

