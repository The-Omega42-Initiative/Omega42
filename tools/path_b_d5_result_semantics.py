#!/usr/bin/env python3
"""Proposal-only pure D5 result classifier; no certificate execution.

Classifies supplied execution observations, never runs or authorizes commands.
Only VERIFIED means a CERTIFIED certificate reproduced with exit code zero and
an exact SHA-256 digest of raw stdout bytes.
"""
import hashlib
import re

HEX = re.compile(r"^[0-9a-f]{64}$")


def classify(status, expected_sha256, observation):
    """Return (verdict, reason) from untrusted observation metadata.

    observation: None, or a dict with exit_code (int), stdout (bytes),
    timed_out (bool), truncated (bool). Never infer success from missing data.
    """
    if status in ("REGISTERED", "WITHDRAWN"):
        return "SKIPPED", "non-executable certificate lifecycle status"
    if status not in ("CERTIFIED", "NOT CERTIFIED"):
        return "INVALID", "unrecognized certificate lifecycle status"
    if not isinstance(expected_sha256, str) or not HEX.fullmatch(expected_sha256):
        return "INVALID", "expected raw-stdout SHA-256 missing or invalid"
    if observation is None:
        return "NOT_RUN", "no execution observation supplied"
    if not isinstance(observation, dict):
        return "INVALID", "observation must be a mapping"
    if observation.get("timed_out") is not False:
        return "FAILED", "timeout status missing or procedure timed out"
    if observation.get("truncated") is not False:
        return "FAILED", "capture truncation status missing or output truncated"
    rc = observation.get("exit_code")
    if type(rc) is not int or rc != 0:
        return "FAILED", "nonzero or missing exit code"
    stdout = observation.get("stdout")
    if not isinstance(stdout, bytes):
        return "INVALID", "stdout must be exact raw bytes"
    actual = hashlib.sha256(stdout).hexdigest()
    if actual != expected_sha256:
        return "MISMATCH", "raw stdout digest does not reproduce certificate"
    if status != "CERTIFIED":
        return "NOT_CERTIFIED", "matching output does not confer CERTIFIED status"
    return "VERIFIED", "exit zero and exact raw stdout digest match"


if __name__ == "__main__":
    raise SystemExit("Library only; does not execute procedures")
