# Tidemark v0.2.1 release-candidate verification

Status: **not deployed**.

The final candidate commit and source SHA-256 are recorded below after the
release gate completes.

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
