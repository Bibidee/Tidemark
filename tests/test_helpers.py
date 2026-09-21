import hashlib
import importlib.util
import json
import sys
import types
from pathlib import Path


def load_module():
    class Decorator:
        def __call__(self, fn): return fn
        @property
        def payable(self): return self
    fake_gl = types.SimpleNamespace()
    fake_gl.Contract = type("Contract", (), {})
    fake_gl.Event = type("Event", (), {})
    fake_gl.public = types.SimpleNamespace(write=Decorator(), view=Decorator())
    fake_gl.vm = types.SimpleNamespace(UserError=ValueError, Return=object)
    fake_gl.evm = types.SimpleNamespace(contract_interface=lambda cls: cls)
    fake = types.ModuleType("genlayer")
    fake.gl = fake_gl
    fake.Address = type("Address", (), {"__init__": lambda self, value="": setattr(self, "as_hex", str(value))})
    fake.u256 = int
    fake.TreeMap = dict
    fake.allow_storage = lambda cls: cls
    old = sys.modules.get("genlayer")
    sys.modules["genlayer"] = fake
    try:
        spec = importlib.util.spec_from_file_location("tidemark_helpers", Path("contracts/tidemark.py"))
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module
    finally:
        if old is None: sys.modules.pop("genlayer", None)
        else: sys.modules["genlayer"] = old


def digest(raw):
    return "0x" + hashlib.sha256(raw).hexdigest()


def test_approval_requires_complete_window_bound_tuple():
    safe = {"window_match": "yes", "claim_supported": "yes", "source_agreement": "yes", "risk": "no", "confidence": 75, "rationale": "supported"}
    m = load_module()
    assert m.derive_verdict(safe) == m.APPROVED
    assert m.derive_verdict(dict(safe, confidence=74)) == m.BLOCKED
    assert m.derive_verdict(dict(safe, risk="yes")) == m.BLOCKED
    assert m.derive_verdict(dict(safe, window_match="unclear")) == m.BLOCKED


def test_equivalence_ignores_rationale_but_not_material_disagreement():
    safe = {"window_match": "yes", "claim_supported": "yes", "source_agreement": "yes", "risk": "no", "confidence": 90, "rationale": "a"}
    m = load_module()
    assert m.equivalent(safe, dict(safe, rationale="b", confidence=100))
    assert not m.equivalent(safe, dict(safe, source_agreement="no"))
    assert not m.equivalent(safe, dict(safe, confidence=74))
    assert not m.equivalent(safe, {"kind": "retryable", "reason": "fetch_unavailable"})


def test_source_manifest_is_canonical_and_hash_bound():
    raw = json.dumps([{"url": "https://alpha.example/a", "hash": digest(b"a")}, {"url": "https://beta.example/b", "hash": digest(b"b")}])
    m = load_module()
    canonical = json.loads(m.parse_sources(raw))
    assert canonical[0]["hash"] == digest(b"a")
    assert canonical[1]["url"] == "https://beta.example/b"


def test_source_manifest_rejects_duplicate_hosts_and_private_targets():
    h = digest(b"a")
    try:
        load_module().parse_sources(json.dumps([{"url": "https://alpha.example/a", "hash": h}, {"url": "https://alpha.example/b", "hash": h}]))
        assert False
    except Exception:
        pass
    try:
        load_module().valid_url("https://127.0.0.1/a")
        assert False
    except Exception:
        pass
