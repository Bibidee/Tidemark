# Deployment

## v0.2.1 Studionet deployment

The current repository source is the v0.2.1 frozen source. It is deployed on
Studionet at [`0xDD75312f65f11d3C7d848e74B6C4a2AFA0f1D4dA`](https://explorer-studio.genlayer.com/address/0xDD75312f65f11d3C7d848e74B6C4a2AFA0f1D4dA)
from [`0xb6374d201fd64c23ce9e2f6a3a32e80d6f8aefcb6233b7a25ce68d5393a38001`](https://explorer-studio.genlayer.com/tx/0xb6374d201fd64c23ce9e2f6a3a32e80d6f8aefcb6233b7a25ce68d5393a38001).
The deployment is FINALIZED / MAJORITY_AGREE / GenVM SUCCESS. `gen_getContractCode`
returned 19,364 bytes whose SHA-256 is
`3e79386adf1f21d94a1c590c8bb4796b9a1f4a125d6980cf167f4762664f34d7`, matching
the local frozen source byte-for-byte.

The v0.2.1 contract freeze is commit
`36dd2dcf2530317e0994d6e0d7505c1d33ee2309` with SHA-256
`3e79386adf1f21d94a1c590c8bb4796b9a1f4a125d6980cf167f4762664f34d7`.

`get_info()` returns `{"name":"Tidemark","version":"0.2.1","min_sources":"2","max_sources":"4","min_provenance":"2","min_confidence":"75","max_source_bytes":"16000"}`.

## Historical v0.1.0 source

Tidemark v0.1.0 was frozen at commit
`fbb2239d093c3777f068b79f07ea19800ee28eef`. The deployable source is
15,603 bytes with SHA-256
`bf371d658ced6c4baf7fb0a8ebc03d17fb668f9cfb5ad5d12a3d7a0863df91c5`.

## Historical v0.1.0 Studionet deployment

- Network: GenLayer Studio Network (Studionet)
- Contract: [`0x2503a36B6d6AFFF9E018521cC598E048d4C9FF05`](https://explorer-studio.genlayer.com/address/0x2503a36B6d6AFFF9E018521cC598E048d4C9FF05)
- Deployment transaction: [`0x60793e6f67f67041ba16d43d028b1ca960516e193733f889bec468f3a4e2ce3a`](https://explorer-studio.genlayer.com/tx/0x60793e6f67f67041ba16d43d028b1ca960516e193733f889bec468f3a4e2ce3a)
- Finality: `FINALIZED`
- Consensus: `MAJORITY_AGREE`
- GenVM execution: `SUCCESS`
- Source parity: `YES` — `gen_getContractCode` returned 15,603 bytes with the same SHA-256 as the frozen local source.

`get_info()` returned:

```json
{"name":"Tidemark","version":"0.1.0","min_sources":"2","max_sources":"4","min_confidence":"75","max_source_bytes":"16000"}
```

## Finalized live evidence

The proposer was `0x7C65cE913F5665c11f1219048112C84CD6cb2a4B`; the designated
consumer was `0x2cd419603eBa593074653930Ddc4073d4FD8fc60`. SDK writes used typed
string arguments and receipt polling was throttled below 30 RPC calls/minute.

### Current v0.2.1 immutable approved -> consumed path

`TM-LIVE-027` used two independent stable sources: RFC Editor
(`standards-document`, SHA-256
`0x9d16217614a74a9b064eff900e5cd07a525793cf8227dca1267100e880f0c410`) and
IANA (`registry`, SHA-256
`0xe3e39e76d00b1677335db8e9a805c7b9480ea2f4dc9e33f0b93cd3a905128d73`).
Proposal
[`0x03d8fe2ffa1da78274dc890f417ccebfe7b6783085f0300b1c75755a1f6aaf78`](https://explorer-studio.genlayer.com/tx/0x03d8fe2ffa1da78274dc890f417ccebfe7b6783085f0300b1c75755a1f6aaf78)
finalized `MAJORITY_AGREE` / GenVM `SUCCESS` with canonical `pending` state.
Review
[`0x8515037e142c2e2deeb50c878b1771f7f6d383077ecb96ee77b7f0823aac60db`](https://explorer-studio.genlayer.com/tx/0x8515037e142c2e2deeb50c878b1771f7f6d383077ecb96ee77b7f0823aac60db)
finalized with `approved`, confidence 98. The designated consumer then
completed
[`0xeb33e54cf69d341864607762343ae840797c1fac2d3a9f06e93afc8a25cbb7e0`](https://explorer-studio.genlayer.com/tx/0xeb33e54cf69d341864607762343ae840797c1fac2d3a9f06e93afc8a25cbb7e0),
finalized `MAJORITY_AGREE` / GenVM `SUCCESS`, leaving canonical status
`consumed`.

### Approved -> consumed

Claim `TM-APPROVAL-002` used two commit-pinned, distinct-host sources:

- `https://cdn.jsdelivr.net/gh/Bibidee/Tidemark@e02648d677faa093ecd31a647470e6f75af5ad21/fixtures/live/approval2-a.txt`
  - SHA-256 `0xf9152bddababecacdba50859a94eb0d8c0c0a1808c2b76f6de5d51f320db1a26`
- `https://raw.githubusercontent.com/Bibidee/Tidemark/e02648d677faa093ecd31a647470e6f75af5ad21/fixtures/live/approval2-b.txt`
  - SHA-256 `0x2cbf7e05431c29f9a189a813649727b9727f5d21fcef7182f4abc1011bb38121`

Evidence:

1. Proposal [`0xa0ba894f73a6c8eeb97ea1cc4803679237f407a29e0dfaefe98fa2748ed8b440`](https://explorer-studio.genlayer.com/tx/0xa0ba894f73a6c8eeb97ea1cc4803679237f407a29e0dfaefe98fa2748ed8b440) — `FINALIZED`, `MAJORITY_AGREE`, GenVM `SUCCESS`; canonical read `pending`.
2. Review [`0xc11c19dbe1395e840aecc608bcb096157584b41ee693654acb2e76790f87660d`](https://explorer-studio.genlayer.com/tx/0xc11c19dbe1395e840aecc608bcb096157584b41ee693654acb2e76790f87660d) — `FINALIZED`, `MAJORITY_AGREE`, GenVM `SUCCESS`; canonical status `approved`, confidence `100`.
3. Consume [`0xc01f69804f2d25e49e8930f215884465edbbf9ba0fb081a4d0633a9a4a3b4786`](https://explorer-studio.genlayer.com/tx/0xc01f69804f2d25e49e8930f215884465edbbf9ba0fb081a4d0633a9a4a3b4786) — `FINALIZED`, `MAJORITY_AGREE`, GenVM `SUCCESS`; canonical final status `consumed`.

### Blocked review

Claim `TM-LIVE-001` proposal [`0xa37088bdf1be803a4aceab0cdb4d47bcec51745e405df2ab7b1afecd24818d90`](https://explorer-studio.genlayer.com/tx/0xa37088bdf1be803a4aceab0cdb4d47bcec51745e405df2ab7b1afecd24818d90) finalized successfully. Review [`0xe7d0c86e006122c987ccdd5070b8ecf0d3ca1255317bc2427ef815975dad6066`](https://explorer-studio.genlayer.com/tx/0xe7d0c86e006122c987ccdd5070b8ecf0d3ca1255317bc2427ef815975dad6066) finalized `MAJORITY_AGREE` / GenVM `SUCCESS` as `blocked` with confidence `96` and `risk = unclear`. No consume was attempted.

## Historical v0.1.0 release gate

- Direct Mode and helper tests: 13 passed, 0 skipped, 0 failed.
- `python scripts/preflight.py`: PASS.
- GenVM lint: PASS (informational I200 newer-runner notice only).
- ABI/schema generation: PASS.
- Exactly one deployable contract source: PASS.

The source file remains unchanged after deployment; documentation and fixture
commits do not alter deployed-source parity.

## v0.2.1 release gate and live evidence

The frozen source has 22 tests (16 Direct Mode and 6 helper tests), with
preflight, GenVM lint, and ABI/schema generation passing. Proposal
`TM-LIVE-023` finalized in [`0x88121ef12eab90a1e156fed985ddd1aa5609e5430c0d05041dde3126bf58006b`](https://explorer-studio.genlayer.com/tx/0x88121ef12eab90a1e156fed985ddd1aa5609e5430c0d05041dde3126bf58006b)
and canonical state was `pending`. Review
`0x294ff43bfbcd8a3910ca24966d0616d5533fd41248f38ff1998cd9cf8f32d265` finalized
with `MAJORITY_AGREE` / GenVM `SUCCESS`, but the semantic result was the
fail-closed `retryable / malformed_model_output`. No consumption transaction
exists because the claim was not approved. The earlier `TM-LIVE-021` proposal
was intentionally rejected for a future window, demonstrating deterministic
timestamp validation.
