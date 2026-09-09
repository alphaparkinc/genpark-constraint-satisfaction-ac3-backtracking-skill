# GenPark Constraint Satisfaction AC-3 Backtracking Skill

Constraint Satisfaction Problem (CSP) solver implementing Arc Consistency AC-3 and Minimum Remaining Values (MRV) search.

Read more at [GenPark](https://genpark.ai) and the [GenPark MCP Catalog](https://genpark.ai/mcp).

```mermaid
graph TD
    A[CSP Variables & Domains] --> B[AC-3 Arc Consistency Revision]
    B --> C{Any Domain Empty?}
    C -->|Yes| D[Inconsistent CSP: No Solution]
    C -->|No| E[MRV Variable Selection]
    E --> F[Backtracking Search with Conflict Checks]
    F --> G[Complete Valid Assignment]
```

## Features
- AC-3 binary constraint domain pruning.
- Minimum Remaining Values (MRV) variable selection heuristic.
- Pure Python standard library.
