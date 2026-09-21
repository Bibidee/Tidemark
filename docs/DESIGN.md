# Tidemark design

Tidemark turns a bounded historical claim into a reusable authorization
primitive. The proposer commits the exact source URLs and SHA-256 digests,
along with the subject, claim, and observation window. Validators fetch those
same sources independently. Only verified content is shown to the semantic
reviewer, and artifact text is explicitly treated as untrusted quoted data.

The approval tuple is deterministic: `window_match=yes`,
`claim_supported=yes`, `source_agreement=yes`, `risk=no`, and confidence at
least 75. Validators must agree on all four material classifications and on
which side of the confidence threshold they fall. They may use different
rationales, but disagreement that could change approval fails closed. Fetch,
network, or malformed-output failures are retryable and never authorize.

The state machine is `pending -> approved|blocked|retryable -> consumed` only
for approved attestations, with `pending|retryable -> cancelled`. The
designated consumer is the only account allowed to consume an approved record.
Tidemark does not assert that a source is true in the world; it attests that
independent validators found the committed sources mutually support the exact
claim for the exact window.
