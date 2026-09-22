# Tidemark v0.2.1 release-candidate verification

Status: **not deployed**.

Frozen candidate commit: `36dd2dcf2530317e0994d6e0d7505c1d33ee2309`

Frozen contract SHA-256: `3e79386adf1f21d94a1c590c8bb4796b9a1f4a125d6980cf167f4762664f34d7`

The candidate adds deterministic historical-window validation, explicit
publisher/source metadata, prompt-injection boundaries, emitted lifecycle
events, and expanded Direct Mode coverage. Before release, freeze the commit,
record the raw source SHA-256, run the full release gate, deploy once, retrieve
the source with `gen_getContractCode`, and require byte-for-byte parity.

Acceptance checklist:

- [ ] exactly one deployable source under `contracts/`
- [x] strict historical-window and provenance tests pass
- [x] Direct Mode and helper tests pass with no skips (22 passed)
- [x] GenVM lint and ABI/schema generation pass
- [x] redirect-header rejection and event-payload identity tests pass
- [ ] deployment is FINALIZED / MAJORITY_AGREE / GenVM SUCCESS
- [ ] retrieved deployed source matches exact local bytes
- [ ] live pending -> approved or blocked -> consumed/cancelled evidence is recorded
- [ ] README and `docs/DEPLOYMENT.md` contain only verified current evidence
