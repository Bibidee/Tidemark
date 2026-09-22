# Tidemark manual smoke test

After deployment, run the read-only smoke check first:

```powershell
python scripts/smoke_test.py --contract 0xYOUR_TIDEMARK_ADDRESS
```

With a known record, add `--attestation-id TM-ID --proposer 0x...` to read its
canonical state. The script never handles private keys. Use the normal SDK or
CLI account workflow for signed proposal, review, consume, and cancel calls,
with the four-field source manifest (`url`, `hash`, `publisher`,
`source_type`). Record only finalized receipts.

The reviewer should exercise these paths:

- Approved: `propose` -> inspect `pending` -> `review` -> finalized
  `approved` -> designated `consume` -> verify `consumed`.
- Blocked: propose contradictory or insufficient evidence -> review -> verify
  finalized `blocked` and confirm it cannot be consumed.
- Negative checks: unauthorized consume, consume twice, invalid/future window,
  duplicate provenance, hash mismatch, explicit redirect response, and the
  pending/retryable cancellation rules.

Example v0.2.1 manifest shape (replace values with exact raw-byte hashes):

```json
[
  {"url":"https://source-a.example/record.txt","hash":"0x...","publisher":"publisher-a","source_type":"archive"},
  {"url":"https://source-b.example/record.txt","hash":"0x...","publisher":"publisher-b","source_type":"archive"}
]
```
