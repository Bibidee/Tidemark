# Tidemark v0.2.1 release-candidate verification

Status: **deployed; live semantic reviews remained fail-closed (retryable or blocked)**.

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

### Final controlled approval attempt (TM-LIVE-026)

To test the approval path without changing the frozen source, a new historical
fixture used two distinct HTTPS APIs and an explicit completed observation date:

- claim ID: `TM-LIVE-026`
- subject: `DATE-2020-01-01`
- claim: `NASA APOD and OpenAlex independently publish records dated 2020-01-01.`
- window: `2020-01-01T00:00:00Z` to `2020-01-02T00:00:00Z`
- NASA source hash: `0x1f890ec393960b69123f07e9e503192f5d1d43939de438e3b966c4688b117807`
- OpenAlex source hash: `0x6042b23caa6e52fe659fb165f9d9641012d5208dc1732019ba1793de4b9734e7`

Proposal: [`0x26c374177fcb5187d3a24e5053034cdecb64d2c8d79488ace988ea73a512fd3e`](https://explorer-studio.genlayer.com/tx/0x26c374177fcb5187d3a24e5053034cdecb64d2c8d79488ace988ea73a512fd3e), finalized with `MAJORITY_AGREE` / GenVM `SUCCESS`; the canonical read confirmed `pending` and exact committed sources.

Review: [`0x3945968b365ef19227c05c6ef378d2b5017acebb24ef1e66165a1a6faa4d861d`](https://explorer-studio.genlayer.com/tx/0x3945968b365ef19227c05c6ef378d2b5017acebb24ef1e66165a1a6faa4d861d), finalized with `MAJORITY_AGREE` / GenVM `SUCCESS`. The canonical result was `blocked`, confidence `0`, with rationale `Committed source verification failed.` The leader's bounded semantic output was `source_agreement=unclear`, `window_match=unclear`, `claim_supported=unclear`, `risk=yes`; this is a legitimate fail-closed result, not an approval.

No consume transaction was submitted because the attestation was not approved. The deployment and contract source remain unchanged; the `approved -> consumed` live path is still unproven.
