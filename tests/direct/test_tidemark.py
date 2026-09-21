import hashlib
import json
import sys
from gltest.direct import sdk_loader

sdk_loader.get_latest_version = lambda: "v0.2.12"

CONTRACT = "contracts/tidemark.py"
ONE = 10**18
SOURCES = [
    {"url": "https://alpha.example/tidemark-001", "body": b"At 2026-01-01, the system was operational."},
    {"url": "https://beta.example/tidemark-001", "body": b"Independent record: the system was operational on 2026-01-01."},
]
SAFE = {"window_match": "yes", "claim_supported": "yes", "source_agreement": "yes", "risk": "no", "confidence": 90, "rationale": "Both records support the bounded historical claim."}


def digest(raw):
    return "0x" + hashlib.sha256(raw).hexdigest()


def manifest():
    return json.dumps([{"url": x["url"], "hash": digest(x["body"])} for x in SOURCES])


def deploy(direct_deploy, direct_vm):
    contract = direct_deploy(CONTRACT)
    direct_vm.sender = None
    return contract


def propose(contract, direct_vm, direct_alice, direct_bob, aid="TM-001"):
    direct_vm.sender = direct_alice
    contract.propose(aid, direct_bob, "service-alpha", "Service alpha was operational during 2026-01-01.", "2026-01-01T00:00:00Z", "2026-01-02T00:00:00Z", manifest())


def configure(direct_vm, result=SAFE):
    for source in SOURCES:
        direct_vm.mock_web(source["url"], {"status": 200, "body": source["body"]})
    direct_vm.mock_llm("Service alpha", json.dumps(result))


def test_propose_read_and_approve(direct_vm, direct_deploy, direct_alice, direct_bob):
    contract = deploy(direct_deploy, direct_vm)
    propose(contract, direct_vm, direct_alice, direct_bob)
    item = contract.get_attestation("TM-001", direct_alice)
    assert item["status"] == "pending"
    assert item["consumer"].lower() == "0x" + direct_bob.hex()
    configure(direct_vm)
    direct_vm.sender = direct_alice
    contract.review("TM-001", direct_alice)
    assert contract.get_attestation("TM-001", direct_alice)["status"] == "approved"


def test_consumer_only_and_one_time_consumption(direct_vm, direct_deploy, direct_alice, direct_bob):
    contract = deploy(direct_deploy, direct_vm)
    propose(contract, direct_vm, direct_alice, direct_bob)
    configure(direct_vm)
    direct_vm.sender = direct_alice
    contract.review("TM-001", direct_alice)
    direct_vm.sender = direct_alice
    with direct_vm.expect_revert():
        contract.consume("TM-001", direct_alice)
    direct_vm.sender = direct_bob
    contract.consume("TM-001", direct_alice)
    assert contract.get_attestation("TM-001", direct_alice)["status"] == "consumed"
    with direct_vm.expect_revert():
        contract.consume("TM-001", direct_alice)


def test_semantic_disagreement_blocks_consensus(direct_vm, direct_deploy, direct_alice, direct_bob):
    contract = deploy(direct_deploy, direct_vm)
    propose(contract, direct_vm, direct_alice, direct_bob)
    configure(direct_vm)
    direct_vm.sender = direct_alice
    contract.review("TM-001", direct_alice)
    direct_vm._llm_mocks.clear()
    direct_vm.mock_llm("Service alpha", json.dumps(dict(SAFE, risk="yes")))
    assert direct_vm.run_validator(leader_result={"kind": "analysis", "result": SAFE}) is False


def test_retryable_artifact_failure_does_not_approve(direct_vm, direct_deploy, direct_alice, direct_bob):
    contract = deploy(direct_deploy, direct_vm)
    propose(contract, direct_vm, direct_alice, direct_bob)
    direct_vm.mock_web(SOURCES[0]["url"], {"status": 503, "body": b""})
    direct_vm.mock_web(SOURCES[1]["url"], {"status": 200, "body": SOURCES[1]["body"]})
    direct_vm.mock_llm("Service alpha", json.dumps(SAFE))
    direct_vm.sender = direct_alice
    contract.review("TM-001", direct_alice)
    assert contract.get_attestation("TM-001", direct_alice)["status"] == "retryable"


def test_cancel_pending_and_reject_invalid_consume(direct_vm, direct_deploy, direct_alice, direct_bob):
    contract = deploy(direct_deploy, direct_vm)
    propose(contract, direct_vm, direct_alice, direct_bob)
    direct_vm.sender = direct_bob
    with direct_vm.expect_revert():
        contract.cancel("TM-001")
    direct_vm.sender = direct_alice
    contract.cancel("TM-001")
    assert contract.get_attestation("TM-001", direct_alice)["status"] == "cancelled"
    with direct_vm.expect_revert():
        contract.cancel("TM-001")
