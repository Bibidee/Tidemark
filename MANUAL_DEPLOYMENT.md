# Tidemark manual deployment

This candidate is intentionally not deployed by this repository pass. A
maintainer performs deployment only after the source is frozen and the release
gate is green.

Verify the exact candidate before deployment:

```powershell
git checkout 36dd2dcf2530317e0994d6e0d7505c1d33ee2309
git status --short
git rev-parse HEAD
Get-FileHash contracts/tidemark.py -Algorithm SHA256
python scripts/preflight.py
```

Require the contract hash to equal:

`3e79386adf1f21d94a1c590c8bb4796b9a1f4a125d6980cf167f4762664f34d7`

In a private terminal with the operator's configured GenLayer account:

```powershell
genlayer network set studionet
genlayer account show
genlayer deploy --contract contracts/tidemark.py
```

Record the deployment transaction and address. Poll until the receipt is
`FINALIZED`, consensus is `MAJORITY_AGREE`, and GenVM execution is `SUCCESS`.
Retrieve the deployed source with `gen_getContractCode`, hash the exact
returned bytes, and require byte-for-byte equality with the local source. The
deployed hash must equal the frozen v0.2.1 hash above before recording the
deployment as valid.

Never put a private key, keystore password, or exported wallet in this
repository. The historical v0.1.0 deployment remains labelled superseded
until a new deployment is actually proven.
