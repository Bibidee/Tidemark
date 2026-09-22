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

## v0.2.1 Live Deployment Verification

Deployment:

```yaml
Contract: 0xDD75312f65f11d3C7d848e74B6C4a2AFA0f1D4dA
Deployment tx: 0xb6374d201fd64c23ce9e2f6a3a32e80d6f8aefcb6233b7a25ce68d5393a38001
Source SHA-256: 3e79386adf1f21d94a1c590c8bb4796b9a1f4a125d6980cf167f4762664f34d7
```

The deployment finalized with `MAJORITY_AGREE` and GenVM `SUCCESS`; source
parity was verified byte-for-byte through `gen_getContractCode`.

### Controlled live review

The prior retryable review
[`0x294ff43bfbcd8a3910ca24966d0616d5533fd41248f38ff1998cd9cf8f32d265`](https://explorer-studio.genlayer.com/tx/0x294ff43bfbcd8a3910ca24966d0616d5533fd41248f38ff1998cd9cf8f32d265)
was correctly fail-closed as `retryable / malformed_model_output`; no code
change was made.

A fresh high-confidence historical fixture was then proposed as `TM-LIVE-024`:

- proposal tx: [`0x25fb597cb229880eb94d06ed265edb653c1df316ace707bd17fbf29899f7c183`](https://explorer-studio.genlayer.com/tx/0x25fb597cb229880eb94d06ed265edb653c1df316ace707bd17fbf29899f7c183)
- review tx: [`0x883bb81bfe3d4359265579f909253e245b77fca33e882b1b7e0979a678eb38a5`](https://explorer-studio.genlayer.com/tx/0x883bb81bfe3d4359265579f909253e245b77fca33e882b1b7e0979a678eb38a5)
- both finalized with `MAJORITY_AGREE` / GenVM `SUCCESS`.
- canonical result: `blocked`, confidence `97`.
- rationale: the sources matched the claim and window, but validators identified
  the fixture as self-referential rather than independently corroborated.

The blocked attestation was not consumed. No approved path or consume
transaction exists yet; attempting consumption would be expected to revert.
The deployed source remains unchanged and no redeployment was performed.
- [x] README and `docs/DEPLOYMENT.md` contain only verified current evidence
