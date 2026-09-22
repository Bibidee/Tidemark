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
