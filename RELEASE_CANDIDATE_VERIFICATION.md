# Tidemark v0.2.0 release-candidate verification

Status: **not deployed**.

Frozen candidate commit: `81649dcf7ce4055ec24f77f8c11f38c43fdd5a8a`

Frozen contract SHA-256: `86c48d1a7abfff4d7d35ccf2d409b7cb0845163ecb76e7f52fa7dc3429882042`

The candidate adds deterministic historical-window validation, explicit
publisher/source metadata, prompt-injection boundaries, emitted lifecycle
events, and expanded Direct Mode coverage. Before release, freeze the commit,
record the raw source SHA-256, run the full release gate, deploy once, retrieve
the source with `gen_getContractCode`, and require byte-for-byte parity.

Acceptance checklist:

- [ ] exactly one deployable source under `contracts/`
- [ ] strict historical-window and provenance tests pass
- [ ] Direct Mode and helper tests pass with no skips
- [ ] GenVM lint and ABI/schema generation pass
- [ ] deployment is FINALIZED / MAJORITY_AGREE / GenVM SUCCESS
- [ ] retrieved deployed source matches exact local bytes
- [ ] live pending -> approved or blocked -> consumed/cancelled evidence is recorded
- [ ] README and `docs/DEPLOYMENT.md` contain only verified current evidence
