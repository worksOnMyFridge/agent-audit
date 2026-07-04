"""Integrity of the checklist data itself."""

import re

from agent_audit.domains import ALL_DOMAINS, TOTAL_CHECKS
from agent_audit.model import SEVERITY_ORDER


def test_six_domains_in_exam_order():
    assert [d.id for d in ALL_DOMAINS] == ["D1", "D2", "D3", "D4", "D5", "D6"]


def test_total_checks():
    assert TOTAL_CHECKS == sum(len(d.checks) for d in ALL_DOMAINS)
    assert TOTAL_CHECKS == 36


def test_check_ids_unique_and_well_formed():
    ids = [c.id for d in ALL_DOMAINS for c in d.checks]
    assert len(ids) == len(set(ids)), "duplicate check id"
    for c_id in ids:
        assert re.fullmatch(r"d[1-6]\.\d+", c_id), f"bad id {c_id}"


def test_check_id_prefix_matches_its_domain():
    for d in ALL_DOMAINS:
        for c in d.checks:
            assert c.id.split(".")[0].upper() == d.id


def test_every_check_has_valid_severity_and_guidance():
    for d in ALL_DOMAINS:
        for c in d.checks:
            assert c.severity in SEVERITY_ORDER
            assert c.title and c.guidance
