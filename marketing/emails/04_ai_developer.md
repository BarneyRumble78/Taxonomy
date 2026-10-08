# Email or DM: AI / RAG developer, startup or lab team

**Subject:** Warrant-aware retrieval: tag every chunk with the evidence it carries

Hi [Name],

Quick one. Your RAG pipeline probably filters by topic. Taxonomy adds two filters: which field owns a claim, and what kind of evidence backs it (proof, measurement, trial, record, argument, and so on).

That gives you:
- retrieval that answers "what was measured?" with measurements, not opinions
- a cheap, deterministic check for answers that claim more certainty than their sources give
- a routing table for multi-agent systems

API (beta): [link], with a free key. There is also a 50-line notebook: [link].

Would you try it on one of your own evaluation sets and tell me where it breaks?

Chris
