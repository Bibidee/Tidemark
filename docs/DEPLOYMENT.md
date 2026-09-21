# Deployment

Tidemark v0.1.0 is currently undeployed. Do not add a contract address until
the frozen source has passed the full release gate and its deployed source has
been retrieved and compared byte-for-byte through the strongest available
Studionet source interface.

Required release evidence:

- exact Git commit and raw SHA-256 of `contracts/tidemark.py`;
- Direct Mode and helper test results;
- GenVM lint and ABI/schema results;
- finalized deployment and GenVM execution result;
- `get_info()` output;
- Explorer source-parity comparison;
- at least one finalized proposal, review, and approved-consumer flow.
