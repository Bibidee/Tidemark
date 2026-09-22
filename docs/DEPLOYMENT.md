# Deployment

## v0.2.1 release candidate (not deployed)

The current repository source is the v0.2.1 release candidate. It has not
been deployed to Studionet. Before deployment, freeze the commit, record the
raw source SHA-256, run the full release gate, deploy once, retrieve the
deployed source with `gen_getContractCode`, and require byte-for-byte parity.
The candidate adds strict historical-window checks, explicit publisher/source
metadata, emitted lifecycle events, and expanded adversarial tests.

The v0.2.1 contract freeze is commit
`36dd2dcf2530317e0994d6e0d7505c1d33ee2309` with SHA-256
`3e79386adf1f21d94a1c590c8bb4796b9a1f4a125d6980cf167f4762664f34d7`.

No v0.2.1 address, transaction, or live evidence is claimed here.

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

## v0.2.1 candidate verification

The current candidate has 22 tests (16 Direct Mode and 6 helper tests), with
preflight, GenVM lint, and ABI/schema generation passing. The candidate source
is not deployed and has no live v0.2.1 transaction evidence yet.
