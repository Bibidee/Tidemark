# Tidemark v0.2.1 release candidate

Tidemark is a standalone GenLayer Intelligent Contract primitive for
hash-bound, multi-source historical attestations. A proposer commits a subject,
a claim, an observation window, and two to four HTTPS source digests. GenLayer
validators independently fetch and verify the exact raw bytes, then perform a
bounded semantic review of whether those sources support the claim during the
specified window.

The contract does not trust a single model, a summary, or a mutable URL. A
deterministic state machine derives `approved`, `blocked`, or `retryable` from
validated structured results. Approval requires agreement on the window,
claim support, source agreement, risk, and the confidence threshold. Rationale
text is explanatory only. An approved attestation can be consumed exactly once
by its designated consumer; all other callers fail closed.

Lifecycle: `pending -> approved|blocked|retryable -> consumed` (approved only),
or `pending|retryable -> cancelled`. Fetch failures and malformed model output
remain retryable; substantive semantic rejection is blocked. Every committed
source is HTTPS, host-distinct, size-bounded, SHA-256 verified, and decoded only
after the raw-byte digest matches. Private, loopback, link-local, multicast,
reserved, and obvious internal hosts are rejected at admission.

Each source also commits an explicit `publisher` and `source_type`. Publisher
identifiers are caller-claimed provenance labels: the contract requires
distinct publishers, URLs, hosts, and hashes, but cannot prove that a label
matches a real-world organization. Historical windows use strict UTC-second
timestamps and end no later than deterministic transaction time.

This repository intentionally contains exactly one deployable source under
`contracts/`. Run `python scripts/preflight.py` before submission. The release
gate parses the source, executes all tests, runs GenVM lint, and generates the
ABI schema.

Tidemark rejects explicit redirect responses (`Location` headers) and private
or malformed host literals. GenLayer's current response API does not expose a
post-redirect final URL or DNS resolution result, so network-layer policy and
immutable, commit-pinned URLs remain necessary for complete redirect/SSRF
protection.

## Why GenLayer matters

Without GenLayer, a single off-chain verifier or one LLM could selectively
approve a convenient source, hide disagreement, or silently substitute a
different document. Tidemark makes every validator independently fetch the
exact hash-bound bytes, verify them before semantic interpretation, and derive
the same bounded authorization outcome. Disagreement never becomes approval;
only a complete, high-confidence approval tuple can authorize consumption.

## Downstream integration

Another Intelligent Contract can treat Tidemark as an authorization gate:
call `get_attestation(id, proposer)`, require `status == "approved"`, then
call `consume(id, proposer)` from the designated consumer before executing the
protected action. Tidemark enforces the consumer check and one-time transition;
downstream code must still validate its own action parameters and handle
`blocked`, `retryable`, and `cancelled` states.

## Release-candidate status

The v0.1.0 Studionet deployment below is historical and superseded. The v0.2.1
source is frozen at commit `36dd2dcf2530317e0994d6e0d7505c1d33ee2309` with
SHA-256 `3e79386adf1f21d94a1c590c8bb4796b9a1f4a125d6980cf167f4762664f34d7`.
It is not deployed yet and requires a fresh deployment and source-parity proof.

## Historical v0.1.0 deployment evidence

The deployed source was frozen at commit
`fbb2239d093c3777f068b79f07ea19800ee28eef` with raw SHA-256
`bf371d658ced6c4baf7fb0a8ebc03d17fb668f9cfb5ad5d12a3d7a0863df91c5` (15,603
bytes). It is deployed on Studionet at
[`0x2503a36B6d6AFFF9E018521cC598E048d4C9FF05`](https://explorer-studio.genlayer.com/address/0x2503a36B6d6AFFF9E018521cC598E048d4C9FF05)
from deployment transaction
[`0x60793e6f67f67041ba16d43d028b1ca960516e193733f889bec468f3a4e2ce3a`](https://explorer-studio.genlayer.com/tx/0x60793e6f67f67041ba16d43d028b1ca960516e193733f889bec468f3a4e2ce3a).
The deployment finalized with `MAJORITY_AGREE` and GenVM `SUCCESS`. The
deployed source retrieved through `gen_getContractCode` is 15,603 bytes and
matches the frozen source byte-for-byte (identical SHA-256).

`get_info()` returns `{"name":"Tidemark","version":"0.1.0","min_sources":"2","max_sources":"4","min_confidence":"75","max_source_bytes":"16000"}`.

## Live lifecycle evidence

The unlocked CLI account `fresh-alice`
(`0x7C65cE913F5665c11f1219048112C84CD6cb2a4B`) was used as proposer and
`fresh-bob` (`0x2cd419603eBa593074653930Ddc4073d4FD8fc60`) as the independent
designated consumer. All writes used typed SDK string arguments and polling was
throttled below the Studionet limit.

### Approved and consumed path

Claim `TM-APPROVAL-002` committed two UTF-8 sources on distinct hosts:

- [`approval2-a.txt`](https://cdn.jsdelivr.net/gh/Bibidee/Tidemark@e02648d677faa093ecd31a647470e6f75af5ad21/fixtures/live/approval2-a.txt) — `0xf9152bddababecacdba50859a94eb0d8c0c0a1808c2b76f6de5d51f320db1a26`
- [`approval2-b.txt`](https://raw.githubusercontent.com/Bibidee/Tidemark/e02648d677faa093ecd31a647470e6f75af5ad21/fixtures/live/approval2-b.txt) — `0x2cbf7e05431c29f9a189a813649727b9727f5d21fcef7182f4abc1011bb38121`

The proposal
[`0xa0ba894f73a6c8eeb97ea1cc4803679237f407a29e0dfaefe98fa2748ed8b440`](https://explorer-studio.genlayer.com/tx/0xa0ba894f73a6c8eeb97ea1cc4803679237f407a29e0dfaefe98fa2748ed8b440)
finalized `MAJORITY_AGREE` / GenVM `SUCCESS`; `get_attestation()` confirmed
`pending`. Review
[`0xc11c19dbe1395e840aecc608bcb096157584b41ee693654acb2e76790f87660d`](https://explorer-studio.genlayer.com/tx/0xc11c19dbe1395e840aecc608bcb096157584b41ee693654acb2e76790f87660d)
finalized `MAJORITY_AGREE` / GenVM `SUCCESS` with `approved`, confidence `100`,
and rationale confirming exact window/source agreement. The designated consumer
then consumed it in
[`0xc01f69804f2d25e49e8930f215884465edbbf9ba0fb081a4d0633a9a4a3b4786`](https://explorer-studio.genlayer.com/tx/0xc01f69804f2d25e49e8930f215884465edbbf9ba0fb081a4d0633a9a4a3b4786),
also finalized `MAJORITY_AGREE` / GenVM `SUCCESS`. Final state: `consumed`.

### Blocked path

Claim `TM-LIVE-001` used the earlier hash-verified two-host fixture. Its
proposal
[`0xa37088bdf1be803a4aceab0cdb4d47bcec51745e405df2ab7b1afecd24818d90`](https://explorer-studio.genlayer.com/tx/0xa37088bdf1be803a4aceab0cdb4d47bcec51745e405df2ab7b1afecd24818d90)
finalized successfully and its review
[`0xe7d0c86e006122c987ccdd5070b8ecf0d3ca1255317bc2427ef815975dad6066`](https://explorer-studio.genlayer.com/tx/0xe7d0c86e006122c987ccdd5070b8ecf0d3ca1255317bc2427ef815975dad6066)
finalized `MAJORITY_AGREE` / GenVM `SUCCESS` as `blocked` (confidence `96`,
risk `unclear`). It was not consumed.

## Baseline validation

The historical v0.1.0 package passed 13 tests (4 helper tests and 9 official
GenLayer Direct Mode contract tests), GenVM lint, ABI/schema generation, and
the project preflight. The v0.2.1 release candidate currently passes 22 tests
(6 helper tests and 16 Direct Mode tests), GenVM lint, ABI/schema generation,
and preflight. Its final candidate source SHA-256 and commit are recorded in
`RELEASE_CANDIDATE_VERIFICATION.md`.
