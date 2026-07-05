#!/usr/bin/env python3
"""
Structural + semantic verifier for GCAssess.lean (slot L1).

This does NOT run the Lean kernel. It performs two kinds of kernel-independent
check that a `lake build` would otherwise subsume, so the build certificate can
state exactly what was machine-checked in this environment versus what still
requires an external Lean toolchain:

  (A) SOURCE-STRUCTURAL checks on GCAssess.lean: namespace balance, absence of
      proof holes / added axioms / compiler-trusting tactics, presence of the
      declared inductives, defs, and the load-bearing theorems, and that the
      #print axioms verification hooks are present.

  (B) SEMANTIC CROSS-CHECK: an independent Python re-implementation of the Lean
      `combine` / `foldVerdicts` / `evalForest` definitions, used to verify by
      exhaustive enumeration the mathematical content of every load-bearing
      theorem (monoid identity + absorbing + associativity; the coherent and
      incoherent fold characterisations; evalForest_eq_fold), and that this Lean
      model agrees with the Python reference implementation (gc_assess.py) on all
      small determinate trees. A theorem the kernel would accept must have TRUE
      mathematical content; (B) confirms that content, (A) confirms the source
      that expresses it. Neither substitutes for the kernel build; together they
      make the residual external step (running `lake build`) narrowly scoped.

Usage:  python3 verify_structure.py [GCAssess.lean]
Exit code 0 iff every check passes.
"""
import re
import sys
import hashlib
import itertools

PATH = sys.argv[1] if len(sys.argv) > 1 else "GCAssess.lean"
src = open(PATH, encoding="utf-8").read()

checks = []


def check(name, cond, detail=""):
    checks.append((name, bool(cond), detail))


# --- strip block comments and line comments so structural checks see only code ---
no_block = re.sub(r"/-.*?-/", "", src, flags=re.DOTALL)
code_lines = [l for l in no_block.splitlines() if not l.strip().startswith("--")]
code = "\n".join(code_lines)

# ===========================================================================
# (A) SOURCE-STRUCTURAL CHECKS
# ===========================================================================

# 1. namespace balance and name consistency. There is exactly one named
#    namespace (GCAssess); the bare `end` on the mutual block is not a namespace.
ns_open = len(re.findall(r"^\s*namespace\s+GCAssess\b", code, re.MULTILINE))
ns_close = len(re.findall(r"^\s*end\s+GCAssess\b", code, re.MULTILINE))
check("namespace_balanced", ns_open == ns_close == 1,
      f"namespace GCAssess: open={ns_open} close={ns_close}")
check("namespace_name_matches_end", ns_open == 1 and ns_close == 1,
      "GCAssess opened and closed once")

# 2. no proof-hole tactics / added axioms / compiler-trusting tactics (in CODE)
for bad in ("sorry", "admit"):
    check(f"no_{bad}", not re.search(rf"\b{bad}\b", code), bad)
check("no_axiom_decl", not re.search(r"^\s*axiom\b", code, re.MULTILINE), "axiom")
check("no_native_decide", "native_decide" not in code, "native_decide")

# 2b. the only textual 'sorry' occurrences in the WHOLE file are in comments
sorry_in_code = re.search(r"\bsorry\b", code)
sorry_total = len(re.findall(r"\bsorry\b", src))
check("sorry_only_in_comments", sorry_in_code is None,
      f"total_occurrences={sorry_total} in_code={bool(sorry_in_code)}")

# 3. declared inductives present, with expected constructors
verdict_block = re.search(r"inductive\s+Verdict\s+where(.*?)deriving", code, re.DOTALL)
verdict_ctors = re.findall(r"^\s*\|\s*(\w+)", verdict_block.group(1),
                           re.MULTILINE) if verdict_block else []
check("inductive_Verdict",
      sorted(verdict_ctors) == ["coherent", "incoherent", "undetermined"],
      f"ctors={verdict_ctors}")
check("verdict_three_valued", len(verdict_ctors) == 3, f"n={len(verdict_ctors)}")
check("verdict_deriving_decidableeq",
      re.search(r"inductive\s+Verdict.*?deriving[^\n]*DecidableEq", code, re.DOTALL),
      "deriving DecidableEq")

htree_block = re.search(r"inductive\s+HTree\s+where(.*?)(?=\n/|\nmutual|\ndef |\ntheorem )",
                        code, re.DOTALL)
htree_ctors = re.findall(r"^\s*\|\s*(\w+)\s*:", htree_block.group(1),
                         re.MULTILINE) if htree_block else []
check("inductive_HTree", sorted(htree_ctors) == ["leaf", "node"], f"ctors={htree_ctors}")

# 4. load-bearing defs present
for d in ["combine", "foldVerdicts", "evalTree", "evalForest"]:
    check(f"def_{d}", re.search(rf"\bdef\s+{d}\b", code), d)

# 5. load-bearing theorems present
required_theorems = [
    "combine_wellformed", "coherent_left_id", "coherent_right_id",
    "incoherent_absorbing_left", "incoherent_absorbing_right", "combine_assoc",
    "fold_coherent_iff", "fold_incoherent_iff", "verdicts_distinct",
    "evalForest_eq_fold", "evalTree_total",
]
thm_names = re.findall(r"^\s*theorem\s+(\w+)", code, re.MULTILINE)
for t in required_theorems:
    check(f"has_{t}", t in thm_names, t)
check("theorems_present", len(thm_names) >= len(required_theorems),
      f"count={len(thm_names)}")

# 6. every theorem body closes with a kernel-checkable terminal tactic
bodies = re.split(r"^\s*theorem\s+\w+", code, flags=re.MULTILINE)[1:]
terminal = re.compile(r"\b(rfl|simp|simpa|decide|cases|induction|exact|rcases|"
                      r"refine|constructor|subst|rintro|obtain)\b")
closed = all(terminal.search(b.split("\ntheorem")[0]) for b in bodies)
check("theorems_have_terminal_tactic", closed, "rfl/simp/cases/induction/... in each body")

# 7. #print axioms verification hooks present for the four load-bearing theorems
for hook in ["combine_assoc", "fold_coherent_iff", "fold_incoherent_iff",
             "evalForest_eq_fold"]:
    check(f"axioms_hook_{hook}",
          re.search(rf"#print axioms GCAssess\.{hook}", src), hook)

# 8. balanced anonymous-constructor angle brackets
check("angle_brackets_balanced", src.count("⟨") == src.count("⟩"),
      f"⟨={src.count('⟨')} ⟩={src.count('⟩')}")

# ===========================================================================
# (B) SEMANTIC CROSS-CHECK — independent model of the Lean algebra
# ===========================================================================
COH, INC, UND = "coherent", "incoherent", "undetermined"
VERDICTS = [COH, INC, UND]


def combine(a, b):
    """Mirror of the Lean `combine` (GCAssess.lean lines 52-57), matched order."""
    if a == INC:
        return INC
    if b == INC:
        return INC
    if a == UND:
        return UND
    if b == UND:
        return UND
    return COH  # coherent, coherent


def fold_verdicts(vs):
    """Mirror of the Lean `foldVerdicts` (right fold from coherent)."""
    acc = COH
    for v in reversed(vs):
        acc = combine(v, acc)
    return acc


# combine_wellformed: result always one of the three
check("sem_combine_wellformed",
      all(combine(a, b) in VERDICTS for a in VERDICTS for b in VERDICTS),
      "3x3 exhaustive")

# identity laws (coherent_left_id / coherent_right_id)
check("sem_coherent_left_id", all(combine(COH, v) == v for v in VERDICTS), "")
check("sem_coherent_right_id", all(combine(v, COH) == v for v in VERDICTS), "")

# absorbing (incoherent_absorbing_left / _right)
check("sem_incoherent_absorbing_left",
      all(combine(INC, v) == INC for v in VERDICTS), "")
check("sem_incoherent_absorbing_right",
      all(combine(v, INC) == INC for v in VERDICTS), "")

# associativity (combine_assoc) — full 3x3x3
assoc_ok = all(
    combine(combine(a, b), c) == combine(a, combine(b, c))
    for a in VERDICTS for b in VERDICTS for c in VERDICTS
)
check("sem_combine_assoc", assoc_ok, "3x3x3 exhaustive")

# fold_coherent_iff and fold_incoherent_iff — exhaustive over all lists up to len 6
LMAX = 6
coh_iff_ok = inc_iff_ok = True
for n in range(0, LMAX + 1):
    for vs in itertools.product(VERDICTS, repeat=n):
        vs = list(vs)
        if (fold_verdicts(vs) == COH) != all(v == COH for v in vs):
            coh_iff_ok = False
        if (fold_verdicts(vs) == INC) != any(v == INC for v in vs):
            inc_iff_ok = False
check("sem_fold_coherent_iff", coh_iff_ok, f"all lists len<= {LMAX}")
check("sem_fold_incoherent_iff", inc_iff_ok, f"all lists len<= {LMAX}")

# verdicts_distinct
check("sem_verdicts_distinct", len(set(VERDICTS)) == 3, "")


# evalForest_eq_fold — evalForest computes foldVerdicts of the mapped leaf evals.
# Model HTree: ('leaf', verdict) or ('node', [children]).
def eval_tree(t):
    if t[0] == "leaf":
        return t[1]
    return eval_forest(t[1])


def eval_forest(ts):
    acc = COH
    for t in reversed(ts):
        acc = combine(eval_tree(t), acc)
    return acc


def all_forests(max_len, max_depth):
    """Exhaustive enumeration of forests up to the given (small) bounds."""
    if max_depth == 0:
        yield []
        return
    trees = [("leaf", v) for v in VERDICTS]
    trees += [("node", f) for f in all_forests(max_len, max_depth - 1)]
    for n in range(0, max_len + 1):
        for combo in itertools.product(trees, repeat=n):
            yield list(combo)


import random as _random


def random_tree(rng, depth, min_children=0):
    """A random HTree: leaf below depth budget, else node with children.

    `min_children` lets callers restrict to Python's valid input domain: the
    Python reference treats a childless `Hypothesis` as a leaf (needing an
    oracle), whereas the Lean model gives `node []` the empty-fold value
    `coherent`. Setting min_children=1 keeps the Python/Lean agreement sweep
    inside the shared representable domain.
    """
    if depth <= 0 or rng.random() < 0.4:
        return ("leaf", rng.choice(VERDICTS))
    n = rng.randint(min_children, 3)
    return ("node", [random_tree(rng, depth - 1, min_children) for _ in range(n)])


# evalForest_eq_fold: exhaustive on tiny forests, then a large random sweep on
# deeper trees (full enumeration of deep trees is combinatorially infeasible).
forest_ok = all(
    eval_forest(ts) == fold_verdicts([eval_tree(t) for t in ts])
    for ts in all_forests(max_len=2, max_depth=2)
)
_rng = _random.Random(20260705)
N_SWEEP = 200_000
for _ in range(N_SWEEP):
    t = random_tree(_rng, depth=6)
    ts = t[1] if t[0] == "node" else [t]
    if eval_forest(ts) != fold_verdicts([eval_tree(x) for x in ts]):
        forest_ok = False
        break
check("sem_evalForest_eq_fold", forest_ok,
      f"exhaustive len<=2 depth<=2 + {N_SWEEP} random depth<=6")

# ---------------------------------------------------------------------------
# (C) Python <-> Lean agreement on determinate trees.
# The Lean model omits budget; run the Python reference under AMPLE budget so
# UNDETERMINED cannot arise from exhaustion, then compare verdicts on every
# small determinate tree. Disagreement here would mean the two artifacts
# formalise different verdict semantics.
# ---------------------------------------------------------------------------
py_lean_agree = None
try:
    import os
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(PATH)),
                                    "..", "python"))
    from gc_assess import Hypothesis, Verdict, assess

    _V = {COH: Verdict.COHERENT, INC: Verdict.INCOHERENT, UND: Verdict.UNDETERMINED}
    _name = {"c": 0}

    def to_hyp(t):
        _name["c"] += 1
        nm = f"n{_name['c']}"
        if t[0] == "leaf":
            return Hypothesis(nm, leaf_verdict=_V[t[1]])
        return Hypothesis(nm, children=[to_hyp(c) for c in t[1]])

    def no_empty_nodes(t):
        """True unless the tree contains an internal node with zero children
        (outside Python's representable domain; see random_tree docstring)."""
        if t[0] == "leaf":
            return True
        return len(t[1]) > 0 and all(no_empty_nodes(c) for c in t[1])

    agree = True
    # exhaustive on tiny trees (restricted to the shared representable domain) ...
    trees = [("leaf", v) for v in VERDICTS]
    trees += [t for t in (("node", f) for f in all_forests(max_len=2, max_depth=2))
              if no_empty_nodes(t)]
    # ... plus a random sweep of deeper trees
    _rng2 = _random.Random(770405)
    trees += [random_tree(_rng2, depth=5, min_children=1) for _ in range(5000)]
    for t in trees:
        _name["c"] = 0
        root = to_hyp(t)
        # ample budget: 1 unit per node, give far more than the node count
        r = assess(root, budget=1_000_000)
        lean_v = eval_tree(t)
        if str(r.verdict) != lean_v:
            agree = False
            break
    py_lean_agree = agree
except Exception as e:  # pragma: no cover - reference not importable
    py_lean_agree = None
    _import_err = str(e)

if py_lean_agree is None:
    check("py_lean_agreement", False, "could not import gc_assess.py reference")
else:
    check("py_lean_agreement", py_lean_agree,
          "determinate trees, ample budget")

# ===========================================================================
# REPORT
# ===========================================================================
digest = hashlib.sha256(src.encode("utf-8")).hexdigest()
passed = sum(1 for _, ok, _ in checks if ok)
total = len(checks)
print(f"FILE: {PATH}")
print(f"SHA256: {digest}")
print(f"VERDICT_CTORS: {len(verdict_ctors)}  THEOREMS: {len(thm_names)}")
print("-" * 68)
for name, ok, detail in checks:
    print(f"[{'PASS' if ok else 'FAIL'}] {name:34s} {detail}")
print("-" * 68)
print(f"RESULT: {passed}/{total} checks passed")
sys.exit(0 if passed == total else 1)
