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

## Historical windows and provenance

`window_start` and `window_end` are strict UTC timestamps in
`YYYY-MM-DDTHH:MM:SSZ` form. Calendar validity, ordering, and the requirement
that the end is no later than the deterministic transaction timestamp are all
checked before storage. A timestamp in the future, a nonexistent date, or a
mixed-format value is rejected.

Every committed source has `url`, `hash`, `publisher`, and `source_type`.
URLs, hosts, SHA-256 digests, and claimed publisher identifiers must be
distinct. This is a bounded provenance-diversity signal, not proof of
real-world publisher identity: a caller can falsely label a source and
downstream users should apply their own trust policy.

## Events

`AttestationProposed`, `AttestationReviewed`, `AttestationConsumed`, and
`AttestationCancelled` are emitted at the corresponding state transition.
Their indexed identifiers and participant addresses are concise; full source
bytes and model rationale are never emitted.

## Prompt-injection boundary

Fetched source text, URLs, timestamps, publisher metadata, and the subject and
claim are delimited as untrusted data in the review prompt. The semantic
reviewer is explicitly told never to execute or follow instructions contained
in those artifacts. A malicious artifact can still cause a blocked or
retryable result, but it cannot become reviewer instructions through the
contract's prompt construction.

## URL limitations

Admission requires HTTPS and rejects credentials, fragments, control
characters, malformed authorities, localhost, private/loopback/link-local/
reserved/multicast/unspecified IPv4 and IPv6 literals, numeric IPv4 aliases,
and obvious internal suffixes. A response carrying a `Location` header is
rejected. The current GenLayer response type does not expose the final URL
after a client-side redirect, so the contract cannot prove that a hostname
will not resolve or redirect to a private target; validators and downstream
operators should prefer immutable, commit-pinned HTTPS resources.
