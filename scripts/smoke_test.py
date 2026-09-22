"""Read-only post-deployment smoke check; no wallet or private-key handling."""

import argparse
import json
import os
import sys


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--contract", required=True)
    parser.add_argument("--proposer")
    parser.add_argument("--attestation-id")
    args = parser.parse_args()
    if (args.proposer is None) != (args.attestation_id is None):
        parser.error("--proposer and --attestation-id must be supplied together")
    try:
        from genlayer_py import create_client, studionet
    except ImportError as exc:
        print(f"Install the supported GenLayer Python client first: {exc}", file=sys.stderr)
        return 2
    client = create_client(chain=studionet)
    info = client.read_contract(address=args.contract, function_name="get_info", args=[])
    print(json.dumps({"contract": args.contract, "get_info": info}, sort_keys=True))
    if args.proposer:
        result = client.read_contract(address=args.contract, function_name="get_attestation", args=[args.attestation_id, args.proposer])
        print(json.dumps({"get_attestation": result}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
