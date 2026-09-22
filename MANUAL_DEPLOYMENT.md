# Tidemark manual deployment

This candidate is intentionally not deployed by this repository pass. A
maintainer performs deployment only after the source is frozen and the release
gate is green.

Verify the exact candidate before deployment:

```powershell
git status --short
git rev-parse HEAD
Get-FileHash contracts/tidemark.py -Algorithm SHA256
python scripts/preflight.py
```

In a private terminal with the operator's configured GenLayer account:

```powershell
genlayer network set studionet
genlayer account show
genlayer deploy --contract contracts/tidemark.py
```

Poll the returned transaction until it is `FINALIZED` and GenVM execution is
`SUCCESS`. Retrieve the deployed source with `gen_getContractCode`, hash the
exact returned bytes, and require byte-for-byte equality with the local source
before recording a new address in the deployment documentation.

Never put a private key, keystore password, or exported wallet in this
repository. The historical v0.1.0 deployment remains labelled superseded
until a new deployment is actually proven.
