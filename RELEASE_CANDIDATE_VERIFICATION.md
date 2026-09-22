# Tidemark v0.2.1 release-candidate verification

Status: **deployed; complete approved -> consumed lifecycle verified**.

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
- [x] live semantic reviews include retryable and blocked fail-closed outcomes
- [x] approved -> consumed lifecycle finalized for TM-LIVE-027

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

The blocked attestation was not consumed. This remains preserved as historical
fail-closed evidence; the complete approved path is recorded below.
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

## Complete v0.2.1 Live Lifecycle

The immutable approval fixture `TM-LIVE-027` used two independent, stable
artifacts for the same historical fact:

- claim: `RFC 5737 and the IANA IPv4 special registry both identify 192.0.2.0/24 as the documentation TEST-NET-1 block.`
- RFC Editor source (`standards-document`): `https://www.rfc-editor.org/rfc/rfc5737.txt`
- RFC hash: `0x9d16217614a74a9b064eff900e5cd07a525793cf8227dca1267100e880f0c410`
- IANA source (`registry`): `https://www.iana.org/assignments/iana-ipv4-special-registry/iana-ipv4-special-registry-1.csv`
- IANA hash: `0xe3e39e76d00b1677335db8e9a805c7b9480ea2f4dc9e33f0b93cd3a905128d73`

The proposal [`0x03d8fe2ffa1da78274dc890f417ccebfe7b6783085f0300b1c75755a1f6aaf78`](https://explorer-studio.genlayer.com/tx/0x03d8fe2ffa1da78274dc890f417ccebfe7b6783085f0300b1c75755a1f6aaf78) finalized with `MAJORITY_AGREE` / GenVM `SUCCESS`, and the canonical read confirmed `pending` with exact source commitments.

The review [`0x8515037e142c2e2deeb50c878b1771f7f6d383077ecb96ee77b7f0823aac60db`](https://explorer-studio.genlayer.com/tx/0x8515037e142c2e2deeb50c878b1771f7f6d383077ecb96ee77b7f0823aac60db) finalized with `MAJORITY_AGREE` / GenVM `SUCCESS`. It produced `approved` with confidence `98`; the stored rationale states that RFC 5737 and the IANA registry identify the same TEST-NET-1 block within the historical window.

The designated consumer then completed the one-time consume transaction [`0xeb33e54cf69d341864607762343ae840797c1fac2d3a9f06e93afc8a25cbb7e0`](https://explorer-studio.genlayer.com/tx/0xeb33e54cf69d341864607762343ae840797c1fac2d3a9f06e93afc8a25cbb7e0), finalized with `MAJORITY_AGREE` / GenVM `SUCCESS`. The final canonical state is `consumed`.

This completes the live `pending -> approved -> consumed` lifecycle on the
source-matched v0.2.1 deployment. Earlier retryable and blocked attempts remain
preserved above as fail-closed evidence.
