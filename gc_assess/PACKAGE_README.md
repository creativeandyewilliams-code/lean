# `gc_assess` — reference implementation and Lean development for the HCFM global-coherence assessment

Supplementary material for **"A Conditional Construction of Human-Centric
Functional Modeling from Globally Lawful Material Flow."** This package realizes
the five-slot audit contract stated in the main paper (the "A serialized
reference implementation" paragraph). It is typed as an **implementation
obligation (T4)**, not as a premise of any theorem in the paper. A reviewer who
chooses not to engage with it loses nothing on the paper's results.

Its purpose is narrow and stated up front: to let a reviewer already disposed to
run a global-coherence assessment do so at low activation cost, and to fix
precisely **where mechanical bookkeeping ends and assessor judgment begins.**

## The contract, file by file

| Slot | Claim | Artifact |
|------|-------|----------|
| **C1** | What the assessment algorithm decides: the recursive **verdict algebra** returning `coherent` / `incoherent` / `undetermined-within-budget`, with the incoherent short-circuit and the budget-relative undetermined outcome explicit. It does **not** decide domain truth. | `python/gc_assess.py` (`Verdict`, `combine`/`assess`); `lean/GCAssess.lean` (`Verdict`, `combine`, `foldVerdicts`) |
| **D1** | The formal input representation: each hypothesis carries a declared system model, perspective/horizon, and per-child certificate/verdict. | `python/gc_assess.py` (`Hypothesis`); `lean/GCAssess.lean` (`HTree`) |
| **P1** | A Python run emitting a **reproducible trace** of the recursion, its short-circuit behavior, and its termination outcome. | `python/gc_assess.py` (`python3 gc_assess.py`); `tests/test_gc_assess.py` |
| **L1** | A Lean development establishing the **decision semantics are internally consistent**: the verdict lattice is well-formed and three-valued; `combine` is a monoid (identity + associativity), so a node's folded verdict is well-defined; the coherent and incoherent stopping conditions are exactly characterised; the tree evaluator computes the algebra's fold. Packaged as a Lean **build package with certificate** (`build.sh`, `verify_structure.py`, `BUILD_CERTIFICATE.txt`). | `lean/GCAssess.lean` + `lean/` build package |
| **B1** | The boundary, stated as first-class content: the substantive per-node judgments — whether a child claim coheres, whether a bridge preserves its invariant, whether a counter-witness is genuine — remain **assessor-supplied oracle inputs**, typed as such and not mechanically discharged. Every oracle-sourced verdict is stamped `oracle_supplied=True` in the trace; in Lean, leaf verdicts are inputs to `evalTree`. | `python/gc_assess.py` (`oracle` / `leaf_verdict`, trace stamp); `lean/GCAssess.lean` (`HTree.leaf`) |

B1 is the load-bearing line, not a caveat. The algebra mechanizes the
*transportable bookkeeping* of an assessment; the *perspective-dependent
coherence judgment* is exactly the condition the observer-inclusion blind spot
hides when it is left outside the system model. This package surfaces that
boundary rather than hiding it.

## How to run (P1)

```
cd python
python3 gc_assess.py          # emits three reproducible traces:
                              #   RUN 1  ample budget      -> coherent (full traversal)
                              #   RUN 2  incoherent leaf   -> incoherent (siblings skipped)
                              #   RUN 3  tight budget       -> undetermined-within-budget
```

Conformance tests (12 checks, mapped to C1 / B1 / soundness):

```
cd tests
python3 test_gc_assess.py     # built-in runner, no dependencies
# or:  python3 -m pytest test_gc_assess.py -q
```

Expected: `12/12 passing`. The suite pins the two structural properties the
paper states in prose:

* **incoherent is reachable on a strictly smaller budget than coherent**
  (`test_incoherent_cheaper_than_coherent`) — coherent requires completing the
  traversal within budget; incoherent requires reaching one incoherent leaf;
* **undetermined is order/budget-relative but soundness is not**
  (`test_coherent_is_allocation_independent`,
  `test_incoherent_is_allocation_independent_once_reachable`) — a returned
  determinate verdict does not depend on the allocation.

## Build and verification (L1) — honest status

`lean/` is now a self-contained **Lean build package with a certificate**,
mirroring the discipline of the project's other Lean companions:

| File | Role |
|------|------|
| `lean/GCAssess.lean` | the development (11 theorems, Lean 4 core only). |
| `lean/lakefile.lean`, `lean/lean-toolchain` | Lake config; pins `leanprover/lean4:v4.9.0`. |
| `lean/verify_structure.py` | kernel-**independent** structural + semantic verifier. |
| `lean/build.sh` | runs the verifier, then `lake build`, then `#print axioms`. |
| `lean/BUILD_CERTIFICATE.txt` | what was verified, file hashes, reproduction, expected axiom output. |
| `lean/gc_assess_lean_build_report.txt` | short status summary. |

`GCAssess.lean` is written against Lean 4 core with `deriving DecidableEq` and
standard `cases`/`simp`/`induction` tactics. It contains **no `axiom` and no
`sorry`** in proof position; the two textual occurrences of "sorry" are in
comments.

**What was executed in the environment that produced this package** — the
kernel-independent verifier (`python3 lean/verify_structure.py lean/GCAssess.lean`),
which **passed 44/44 checks**. It confirms (a) the source is free of
`sorry`/`admit`/`axiom`/`native_decide` in proof position and all 11
load-bearing theorems are present and closed by kernel-checkable tactics, and
(b) — via an *independent executable model* of `combine`/`foldVerdicts`/
`evalForest` — that the full mathematical content of the monoid laws,
`combine_assoc`, `fold_coherent_iff`, `fold_incoherent_iff`, and
`evalForest_eq_fold` is **true by exhaustive / large-sample enumeration**, and
that this model **agrees with the Python reference** on every small determinate
tree in the shared representable domain.

**What was NOT executed here:** the Lean kernel build itself. No Lean toolchain
was installable in this environment (the pinned release archive is outside this
session's network access scope). Before the manuscript claims "machine-checked,"
run, with the pinned toolchain:

```
cd lean
./build.sh          # verifier -> lake build -> #print axioms
# or just:  lake build
```

A clean `lake build` (exit 0) with `#print axioms` reporting only
`[propext, Classical.choice, Quot.sound]` for `combine_assoc`,
`fold_coherent_iff`, `fold_incoherent_iff`, and `evalForest_eq_fold` is the
kernel-level certificate. Until that run is attached, describe the artifact in
the paper as a **Lean development (source provided), structurally and
semantically cross-checked**, and upgrade to "machine-checked" only after
attaching the `build.sh` output. Full details, hashes, and expected output are
in `lean/BUILD_CERTIFICATE.txt`.

### Python/Lean scope gap (disclose in slot L1)

The two artifacts verify overlapping but not identical objects. In Python,
`UNDETERMINED` arises **only** from budget exhaustion, and budget accounting is
exercised by the conformance tests, not by Lean. In Lean, `undetermined` is a
leaf **input** and budget is not modelled; `node []` folds to the empty-fold
value `coherent`, a case the Python `Hypothesis` does not represent. So Lean
certifies the verdict **monoid** and the fold characterisations, while the
**budget dynamics** that generate `UNDETERMINED` are verified on the Python side
only. The manuscript's slot-L1 sentence should say so.

## What this package is not

It is not a mechanization of the paper's load-bearing mathematical theorem (the
global material-law completion / observability blind spot). Those results are
proved in the article and supplement in the ordinary way. This package
mechanizes only the **assessment procedure** the paper describes operationally —
its verdict algebra and the boundary at which assessor judgment enters.
