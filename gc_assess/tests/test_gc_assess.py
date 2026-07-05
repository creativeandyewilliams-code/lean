"""
test_gc_assess.py -- Conformance tests for the HCFM global-coherence
assessment verdict algebra (gc_assess.py).

Each test is mapped to the audit-contract slot / property it discharges:

  C1  verdict lattice + the two structural properties (short-circuit;
      budget-relative undetermined)
  B1  oracle boundary: substantive leaf verdicts are inputs, stamped as such
  SND soundness: a returned COHERENT/INCOHERENT is allocation-independent

Run with:  python3 -m pytest test_gc_assess.py -q
       or:  python3 test_gc_assess.py         (built-in runner, no pytest)
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "python"))

from gc_assess import Hypothesis, Verdict, assess  # noqa: E402


def leaf(name, v, cost=1, model="M"):
    return Hypothesis(name, system_model=model, cost=cost, leaf_verdict=v)


# --- C1: all-coherent leaves -> COHERENT, full traversal -------------------
def test_all_coherent_returns_coherent():
    root = Hypothesis("r", children=[
        leaf("a", Verdict.COHERENT), leaf("b", Verdict.COHERENT),
    ])
    r = assess(root, budget=10)
    assert r.verdict is Verdict.COHERENT


# --- C1: any incoherent child -> INCOHERENT --------------------------------
def test_one_incoherent_returns_incoherent():
    root = Hypothesis("r", children=[
        leaf("a", Verdict.COHERENT), leaf("b", Verdict.INCOHERENT),
    ])
    r = assess(root, budget=10)
    assert r.verdict is Verdict.INCOHERENT


# --- C1: short-circuit -- siblings after an incoherent child are skipped ----
def test_incoherent_short_circuits_siblings():
    root = Hypothesis("r", children=[
        leaf("bad", Verdict.INCOHERENT),
        leaf("never_visited", Verdict.COHERENT),
    ])
    r = assess(root, budget=10)
    visited = {e.name for e in r.trace}
    assert "never_visited" not in visited
    # the parent entry records exactly one skipped sibling
    parent = [e for e in r.trace if e.name == "r"][0]
    assert parent.short_circuited_siblings == 1


# --- C1: INCOHERENT reachable on strictly smaller budget than COHERENT ------
def test_incoherent_cheaper_than_coherent():
    coherent_tree = Hypothesis("r", children=[
        leaf("a", Verdict.COHERENT), leaf("b", Verdict.COHERENT),
        leaf("c", Verdict.COHERENT),
    ])
    incoherent_tree = Hypothesis("r", children=[
        leaf("a", Verdict.INCOHERENT),  # short-circuits immediately
        leaf("b", Verdict.COHERENT), leaf("c", Verdict.COHERENT),
    ])
    rc = assess(coherent_tree, budget=100)
    ri = assess(incoherent_tree, budget=100)
    assert ri.verdict is Verdict.INCOHERENT
    assert rc.verdict is Verdict.COHERENT
    assert ri.budget_spent < rc.budget_spent


# --- C1: budget exhaustion with no incoherent leaf -> UNDETERMINED ----------
def test_budget_exhaustion_returns_undetermined():
    root = Hypothesis("r", children=[
        leaf("a", Verdict.COHERENT, cost=5),
        leaf("b", Verdict.COHERENT, cost=5),
    ])
    r = assess(root, budget=6)  # can pay root(1)+a(5)=6, cannot reach b
    assert r.verdict is Verdict.UNDETERMINED


# --- C1: undetermined does NOT mask an incoherent that WAS reached ----------
def test_incoherent_beats_undetermined_when_reached():
    root = Hypothesis("r", children=[
        leaf("bad", Verdict.INCOHERENT, cost=1),
        leaf("expensive", Verdict.COHERENT, cost=999),
    ])
    r = assess(root, budget=5)
    # 'bad' is reached first and short-circuits; verdict is INCOHERENT, not U
    assert r.verdict is Verdict.INCOHERENT


# --- B1: leaf verdicts are oracle inputs, stamped oracle_supplied ------------
def test_leaf_verdicts_are_stamped_oracle_supplied():
    root = Hypothesis("r", children=[leaf("a", Verdict.COHERENT)])
    r = assess(root, budget=10)
    leaf_entry = [e for e in r.trace if e.name == "a"][0]
    internal_entry = [e for e in r.trace if e.name == "r"][0]
    assert leaf_entry.oracle_supplied is True      # substantive judgment: oracle
    assert internal_entry.oracle_supplied is False  # bookkeeping: mechanical


# --- B1: an external oracle callback overrides inline leaf verdicts ----------
def test_external_oracle_callback_is_used():
    root = Hypothesis("r", children=[
        Hypothesis("a", leaf_verdict=Verdict.COHERENT),
    ])
    # Oracle says INCOHERENT regardless of the inline COHERENT declaration.
    r = assess(root, budget=10, oracle=lambda h: Verdict.INCOHERENT)
    assert r.verdict is Verdict.INCOHERENT


# --- SND: soundness of COHERENT is allocation-independent -------------------
def test_coherent_is_allocation_independent():
    root = Hypothesis("r", children=[
        leaf("a", Verdict.COHERENT), leaf("b", Verdict.COHERENT),
    ])
    for budget in (5, 10, 50, 1000):
        assert assess(root, budget=budget).verdict is Verdict.COHERENT


# --- SND: soundness of INCOHERENT is allocation-independent -----------------
def test_incoherent_is_allocation_independent_once_reachable():
    root = Hypothesis("r", children=[leaf("bad", Verdict.INCOHERENT)])
    for budget in (2, 10, 50, 1000):
        assert assess(root, budget=budget).verdict is Verdict.INCOHERENT


# --- SND: recursion terminates and budget accounting is conserved ----------
def test_budget_never_exceeds_limit():
    root = Hypothesis("r", children=[
        Hypothesis("m", children=[
            leaf("a", Verdict.COHERENT), leaf("b", Verdict.COHERENT),
        ]),
        leaf("c", Verdict.COHERENT),
    ])
    for budget in range(1, 12):
        r = assess(root, budget=budget)
        assert r.budget_spent <= budget


# --- structural: nested tree resolves bottom-up ----------------------------
def test_nested_tree_resolves():
    root = Hypothesis("r", children=[
        Hypothesis("m1", children=[
            leaf("a", Verdict.COHERENT), leaf("b", Verdict.COHERENT),
        ]),
        Hypothesis("m2", children=[
            leaf("c", Verdict.COHERENT), leaf("d", Verdict.INCOHERENT),
        ]),
    ])
    r = assess(root, budget=100)
    assert r.verdict is Verdict.INCOHERENT


def _run_builtin():
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    passed = 0
    for t in tests:
        t()
        passed += 1
        print(f"PASS  {t.__name__}")
    print(f"\n{passed}/{len(tests)} passing")


if __name__ == "__main__":
    _run_builtin()
