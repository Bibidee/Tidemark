import atexit
import os
import sys
import pytest


if sys.platform == "win32":
    from gltest.direct import loader as _loader
    _leaked = []
    _unlink = os.unlink

    def _tolerant(path, *args, **kwargs):
        try:
            return _unlink(path, *args, **kwargs)
        except PermissionError:
            _leaked.append(os.fspath(path))

    _original = _loader._inject_message_to_fd0

    def _inject(vm):
        os.unlink = _tolerant
        try:
            return _original(vm)
        finally:
            os.unlink = _unlink

    _loader._inject_message_to_fd0 = _inject

    @atexit.register
    def _sweep():
        for path in _leaked:
            try:
                _unlink(path)
            except OSError:
                pass


@pytest.fixture(autouse=True)
def _reset_contract_registry():
    yield
    try:
        import genlayer.gl.genvm_contracts as contracts
    except ImportError:
        return
    contracts.__known_contract__ = None
