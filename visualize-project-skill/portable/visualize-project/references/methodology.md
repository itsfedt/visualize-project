# Methodology and Design Basis

This skill uses C4-style zoom levels to avoid forcing different abstraction levels into a single diagram. Useful views include System Context, Container/application landscape, Component (only where useful), Dynamic/runtime flow, and Deployment.

Architecture diagrams should be self-describing: title/scope, named/typed elements, responsibilities, technology where relevant, directional labelled relationships, and protocols where relevant.

Mermaid is the default portable diagram source. Ordinary flowcharts are favored when they provide better cross-renderer portability and semantic styling.

D2 may be used for large architecture/deployment views when installed and when it materially improves layout. D2 supports themes and architecture-oriented icons.

References:
- https://c4model.com/
- https://c4model.com/diagrams/notation
- https://c4model.com/diagrams/checklist
- https://mermaid.js.org/
- https://d2lang.com/
