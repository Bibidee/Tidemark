# Tidemark v0.1.0

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

This repository intentionally contains exactly one deployable source under
`contracts/`. Run `python scripts/preflight.py` before submission. The release
gate parses the source, executes all tests, runs GenVM lint, and generates the
ABI schema. Tidemark is currently undeployed; deployment evidence will be
added only after a frozen source passes the complete gate and Explorer source
parity is verified.

## Baseline validation

The initial package passes 9 tests (4 helper tests and 5 official GenLayer
Direct Mode contract tests), GenVM lint, ABI/schema generation, and the project
preflight. The contract source SHA-256 is
`bf371d658ced6c4baf7fb0a8ebc03d17fb668f9cfb5ad5d12a3d7a0863df91c5`.
