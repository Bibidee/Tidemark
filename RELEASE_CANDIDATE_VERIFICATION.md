# Tidemark v0.2.1 release-candidate verification

Status: **deployed; live semantic review remained retryable**.

Frozen candidate commit: `36dd2dcf2530317e0994d6e0d7505c1d33ee2309`

Frozen contract SHA-256: `3e79386adf1f21d94a1c590c8bb4796b9a1f4a125d6980cf167f4762664f34d7`

The candidate adds deterministic historical-window validation, explicit
publisher/source metadata, prompt-injection boundaries, emitted lifecycle
events, and expanded Direct Mode coverage. Before release, freeze the commit,
record the raw source SHA-256, run the full release gate, deploy once, retrieve
the source with `gen_getContractCode`, and require byte-for-byte parity.

Acceptance checklist:

- [x] exactly one deployable source under `contracts/`
- [x] strict historical-window and provenance tests pass
- [x] Direct Mode and helper tests pass with no skips (22 passed)
- [x] GenVM lint and ABI/schema generation pass
- [x] redirect-header rejection and event-payload identity tests pass
- [x] deployment is FINALIZED / MAJORITY_AGREE / GenVM SUCCESS
- [x] retrieved deployed source matches exact local bytes
- [x] live proposal and pending read evidence is recorded
- [x] live semantic review finalized fail-closed as retryable/malformed_model_output
- [ ] approved -> consumed lifecycle (not possible without a live approved verdict)
- [x] README and `docs/DEPLOYMENT.md` contain only verified current evidence
