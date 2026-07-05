"""
gc_assess.py -- Reference implementation of the HCFM global-coherence
assessment verdict algebra.

This is the artifact referenced by slot (P1) of the audit contract in
"A Conditional Construction of Human-Centric Functional Modeling from Globally
Lawful Material Flow" (main paper). It is TYPED AS AN IMPLEMENTATION OBLIGATION
(T4), NOT as a premise of any theorem in the paper.

WHAT THIS DECIDES (slot C1)
---------------------------
The recursive VERDICT ALGEBRA over a declared hypothesis tree, returning exactly
one of:

    COHERENT     -- every child discharged coherent within budget
    INCOHERENT   -- some child returned incoherent (short-circuits)
    UNDETERMINED -- budget exhausted (or a node left undetermined) with no
                    incoherent child found

The two structural properties the paper states in prose are made explicit here:

  * INCOHERENT SHORT-CIRCUIT. As soon as any child returns INCOHERENT, the
    parent verdict is settled INCOHERENT and remaining siblings are NOT visited.
    Consequence: INCOHERENT is reachable on a strictly smaller budget than
    COHERENT, because COHERENT requires completing the full traversal within
    budget while INCOHERENT requires reaching a single incoherent leaf.

  * BUDGET-RELATIVE UNDETERMINED. UNDETERMINED is a first-class outcome, not a
    failure: it is returned when the declared coherence budget is exhausted, or
    when a node is judged undetermined, and no incoherent child was reached. It
    is order- and budget-relative BY DESIGN. What is NOT allocation-dependent is
    SOUNDNESS: a returned COHERENT means every leaf on the traversed tree was
    judged coherent; a returned INCOHERENT means a genuine incoherent leaf was
    reached.

WHAT THIS DOES NOT DECIDE (slot B1 -- the load-bearing boundary)
----------------------------------------------------------------
The algebra decides the *bookkeeping* of an assessment. It does NOT decide the
substantive, perspective-dependent coherence judgment at a node -- whether a
child claim coheres, whether a bridge preserves its invariant, whether a
counter-witness is genuine. Those are supplied to this code as declared ORACLE
inputs (the `leaf_verdict` field, or the `oracle` callback). This is not a
limitation to be engineered away: it is an instance of the paper's own thesis.
The transportable bookkeeping of an assessment is mechanizable and auditable;
the perspective-dependent coherence judgment is exactly the condition the
observer-inclusion blind spot hides when it is left outside the system model.
This code makes that boundary explicit rather than hiding it: every node whose
verdict came from the oracle is stamped `oracle_supplied=True` in the trace.

Pure standard library. Demonstrator-grade. Python 3.8+.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Callable, List, Optional


# ---------------------------------------------------------------------------
# Verdict lattice (slot C1)
# ---------------------------------------------------------------------------
class Verdict(Enum):
    COHERENT = "coherent"
    INCOHERENT = "incoherent"
    UNDETERMINED = "undetermined"  # within-budget: honest non-verdict

    def __str__(self) -> str:
        return self.value


# ---------------------------------------------------------------------------
# Declared input representation (slot D1)
# ---------------------------------------------------------------------------
@dataclass
class Hypothesis:
    """A node in the declared hypothesis tree (slot D1).

    Fields:
      name          -- identifier used in the trace.
      system_model  -- declared system model / perspective / horizon label.
                       Recorded, not interpreted, by the algebra.
      cost          -- declared budget cost to *assess this node* (>= 1).
      leaf_verdict  -- for a leaf: the ORACLE-supplied verdict at this node
                       (Verdict) or None if it is to be requested from the
                       `oracle` callback. Ignored when `children` is nonempty.
      children      -- declared child hypotheses; an internal node is coherent
                       iff all children are coherent within budget.
    """
    name: str
    system_model: str = ""
    cost: int = 1
    leaf_verdict: Optional[Verdict] = None
    children: List["Hypothesis"] = field(default_factory=list)


@dataclass
class TraceEntry:
    name: str
    system_model: str
    verdict: Verdict
    oracle_supplied: bool          # slot B1: True iff verdict came from the oracle
    budget_before: int
    budget_after: int
    short_circuited_siblings: int  # siblings skipped due to incoherent short-circuit
    depth: int


@dataclass
class Result:
    verdict: Verdict
    budget_spent: int
    budget_limit: int
    trace: List[TraceEntry]

    def render_trace(self) -> str:
        lines = [
            f"{'node':<28}{'model':<16}{'verdict':<13}"
            f"{'oracle':<8}{'budget':<12}{'skipped'}"
        ]
        lines.append("-" * 84)
        for e in self.trace:
            indent = "  " * e.depth
            node = (indent + e.name)[:27]
            lines.append(
                f"{node:<28}{e.system_model[:15]:<16}{str(e.verdict):<13}"
                f"{('yes' if e.oracle_supplied else '--'):<8}"
                f"{f'{e.budget_before}->{e.budget_after}':<12}"
                f"{e.short_circuited_siblings if e.short_circuited_siblings else ''}"
            )
        lines.append("-" * 84)
        lines.append(
            f"VERDICT: {self.verdict}   "
            f"budget spent {self.budget_spent}/{self.budget_limit}"
        )
        return "\n".join(lines)


# Oracle callback type: given a leaf Hypothesis, return its substantive verdict.
Oracle = Callable[[Hypothesis], Verdict]


def _default_oracle(h: Hypothesis) -> Verdict:
    if h.leaf_verdict is None:
        raise ValueError(
            f"leaf '{h.name}' has no declared leaf_verdict and no oracle "
            f"was supplied; the substantive judgment is an oracle input (B1)."
        )
    return h.leaf_verdict


class _Budget:
    def __init__(self, limit: int) -> None:
        self.limit = limit
        self.spent = 0

    def remaining(self) -> int:
        return self.limit - self.spent

    def try_spend(self, cost: int) -> bool:
        if self.spent + cost > self.limit:
            return False
        self.spent += cost
        return True


def assess(
    root: Hypothesis,
    budget: int,
    oracle: Optional[Oracle] = None,
) -> Result:
    """Run the recursive global-coherence verdict algebra over `root`.

    Returns a Result carrying the verdict and a full auditable trace (the
    'auditable trace' the paper attributes to external certification).
    """
    oracle = oracle or _default_oracle
    b = _Budget(budget)
    trace: List[TraceEntry] = []

    def visit(h: Hypothesis, depth: int) -> Verdict:
        before = b.remaining()

        # Charge the declared cost of assessing this node. If the budget cannot
        # cover it, this node is UNDETERMINED-within-budget (and, being a
        # non-incoherent outcome, it propagates as undetermined upward unless a
        # sibling short-circuits with incoherent).
        if not b.try_spend(h.cost):
            trace.append(TraceEntry(
                h.name, h.system_model, Verdict.UNDETERMINED,
                oracle_supplied=False, budget_before=before,
                budget_after=b.remaining(), short_circuited_siblings=0,
                depth=depth,
            ))
            return Verdict.UNDETERMINED

        # Leaf: the substantive verdict is an ORACLE input (slot B1).
        if not h.children:
            v = oracle(h)
            trace.append(TraceEntry(
                h.name, h.system_model, v, oracle_supplied=True,
                budget_before=before, budget_after=b.remaining(),
                short_circuited_siblings=0, depth=depth,
            ))
            return v

        # Internal node: coherent iff all children coherent; incoherent
        # short-circuits; otherwise undetermined.
        saw_undetermined = False
        verdict = Verdict.COHERENT
        for i, child in enumerate(h.children):
            cv = visit(child, depth + 1)
            if cv is Verdict.INCOHERENT:
                skipped = len(h.children) - (i + 1)  # siblings not visited
                verdict = Verdict.INCOHERENT
                trace.append(TraceEntry(
                    h.name, h.system_model, verdict, oracle_supplied=False,
                    budget_before=before, budget_after=b.remaining(),
                    short_circuited_siblings=skipped, depth=depth,
                ))
                return verdict  # SHORT-CIRCUIT: siblings i+1.. are never visited
            if cv is Verdict.UNDETERMINED:
                saw_undetermined = True

        if saw_undetermined:
            verdict = Verdict.UNDETERMINED
        trace.append(TraceEntry(
            h.name, h.system_model, verdict, oracle_supplied=False,
            budget_before=before, budget_after=b.remaining(),
            short_circuited_siblings=0, depth=depth,
        ))
        return verdict

    final = visit(root, 0)
    return Result(
        verdict=final, budget_spent=b.spent, budget_limit=budget, trace=trace
    )


# ---------------------------------------------------------------------------
# Worked example: run directly to emit a reproducible trace (slot P1).
# ---------------------------------------------------------------------------
def _example() -> None:
    # A declared hypothesis tree. Leaf verdicts are ORACLE inputs (B1):
    # here supplied inline as `leaf_verdict` and stamped oracle_supplied.
    root = Hypothesis(
        name="H_root", system_model="material-flow/H0", children=[
            Hypothesis("H_completion", "P-space/H1", children=[
                Hypothesis("leaf_inverse_limit", "P-space/H1",
                           leaf_verdict=Verdict.COHERENT),
                Hypothesis("leaf_grounding", "P-space/H1",
                           leaf_verdict=Verdict.COHERENT),
            ]),
            Hypothesis("H_emission", "P-space/H1", children=[
                Hypothesis("leaf_mobius", "P-space/H1",
                           leaf_verdict=Verdict.COHERENT),
            ]),
            Hypothesis("H_registration", "A(R)-space/H2", children=[
                Hypothesis("leaf_quotient", "A(R)-space/H2",
                           leaf_verdict=Verdict.COHERENT),
                Hypothesis("leaf_bridge", "A(R)-space/H2",
                           leaf_verdict=Verdict.COHERENT),
            ]),
        ],
    )

    print("=" * 84)
    print("RUN 1 -- ample budget: expect COHERENT, full traversal")
    print("=" * 84)
    r1 = assess(root, budget=20)
    print(r1.render_trace())

    print()
    print("=" * 84)
    print("RUN 2 -- incoherent leaf under H_emission: expect INCOHERENT,")
    print("         siblings after it skipped (short-circuit)")
    print("=" * 84)
    root2 = Hypothesis(
        name="H_root", system_model="material-flow/H0", children=[
            Hypothesis("H_emission", "P-space/H1", children=[
                Hypothesis("leaf_bad", "P-space/H1",
                           leaf_verdict=Verdict.INCOHERENT),
            ]),
            Hypothesis("H_registration", "A(R)-space/H2", children=[
                Hypothesis("leaf_quotient", "A(R)-space/H2",
                           leaf_verdict=Verdict.COHERENT),
            ]),
        ],
    )
    r2 = assess(root2, budget=20)
    print(r2.render_trace())

    print()
    print("=" * 84)
    print("RUN 3 -- tight budget: expect UNDETERMINED-within-budget (no")
    print("         incoherent leaf reached before budget exhausted)")
    print("=" * 84)
    r3 = assess(root, budget=3)
    print(r3.render_trace())


if __name__ == "__main__":
    _example()
