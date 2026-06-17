#!/usr/bin/env python3
"""
Structural verifier for pause_paper_v82 / ClaimStatusRoutingV81 RoutingSkeleton.lean

This does NOT run the Lean kernel. It performs source-level structural checks
that a `lake build` would otherwise subsume, so the build certificate can state
exactly what was machine-checked in this sandbox versus what requires an
external Lean toolchain.
"""
import re, sys, hashlib

PATH = sys.argv[1] if len(sys.argv) > 1 else "ClaimStatusRouting/RoutingSkeleton.lean"
src = open(PATH, encoding="utf-8").read()

checks = []
def check(name, cond, detail=""):
    checks.append((name, bool(cond), detail))

# --- strip comments for some checks ---
no_block = re.sub(r"/-.*?-/", "", src, flags=re.DOTALL)
code_lines = [l for l in no_block.splitlines() if not l.strip().startswith("--")]
code = "\n".join(code_lines)

# 1. namespace balance
opens = len(re.findall(r"^\s*namespace\s+\w+", code, re.MULTILINE))
ends  = len(re.findall(r"^\s*end\s+\w+", code, re.MULTILINE))
check("namespace_balanced", opens == ends == 1, f"namespace={opens} end={ends}")

# 2. no proof-hole tactics / axioms
for bad in ("sorry", "admit"):
    check(f"no_{bad}", not re.search(rf"\b{bad}\b", code), bad)
check("no_axiom_decl", not re.search(r"^\s*axiom\b", code, re.MULTILINE), "axiom")
check("no_native_decide", "native_decide" not in code, "native_decide")

# 3. inductive declarations present
for ind in ["Coordinate", "ObjectionKind", "RoutedStatus", "ChannelKind",
            "FailureMode", "ExcludedClaim"]:
    check(f"inductive_{ind}", re.search(rf"inductive\s+{ind}\b", code), ind)

# 4. structure declarations present
for st in ["RiskStatusObject", "WordingObjection", "RouterApparatus"]:
    check(f"structure_{st}", re.search(rf"structure\s+{st}\b", code), st)

# 5. enumerate ObjectionKind constructors and confirm route covers all
obj_block = re.search(r"inductive ObjectionKind where(.*?)deriving", code, re.DOTALL).group(1)
obj_ctors = re.findall(r"^\s*\|\s*(\w+)", obj_block, re.MULTILINE)
route_block = re.search(r"def route :.*?(?=\n/--|\ndef )", code, re.DOTALL).group(0)
routed = re.findall(r"ObjectionKind\.(\w+)\s*=>", route_block)
missing = sorted(set(obj_ctors) - set(routed))
extra   = sorted(set(routed) - set(obj_ctors))
check("route_exhaustive", not missing and not extra,
      f"objection_ctors={len(obj_ctors)} routed={len(routed)} missing={missing} extra={extra}")

# 6. ChannelKind constructors and confirm retypingCapacity covers all
chan_block = re.search(r"inductive ChannelKind where(.*?)deriving", code, re.DOTALL).group(1)
chan_ctors = re.findall(r"^\s*\|\s*(\w+)", chan_block, re.MULTILINE)
retype_block = re.search(r"def retypingCapacity :.*?(?=\n/--|\ndef )", code, re.DOTALL).group(0)
retyped = re.findall(r"ChannelKind\.(\w+)\s*=>", retype_block)
missing_c = sorted(set(chan_ctors) - set(retyped))
extra_c   = sorted(set(retyped) - set(chan_ctors))
check("retypingCapacity_exhaustive", not missing_c and not extra_c,
      f"channel_ctors={len(chan_ctors)} mapped={len(retyped)} missing={missing_c} extra={extra_c}")

# 7. theorems present and each has a tactic proof block (rfl/decide/simp/cases/rcases/exact)
thm_names = re.findall(r"^\s*theorem\s+(\w+)", code, re.MULTILINE)
check("theorems_present", len(thm_names) >= 40, f"count={len(thm_names)}")
bodies = re.split(r"^\s*theorem\s+\w+", code, flags=re.MULTILINE)[1:]
TACTIC_RE = re.compile(r"\b(rfl|decide|simp|cases|rcases|exact)\b")
closed = all(TACTIC_RE.search(b.split(":=")[-1] if ":= by" not in b else b.split(":= by", 1)[1])
             for b in bodies)
check("theorems_have_terminal_tactic", closed,
      "rfl/decide/simp/cases/rcases/exact present in each body")

# 8. provesExcludedClaim is constant false
check("provesExcludedClaim_false",
      re.search(r"def provesExcludedClaim.*?:=\s*false", code, re.DOTALL), "constant false")

# 9. balanced anonymous-constructor brackets
check("angle_brackets_balanced", code.count("⟨") == code.count("⟩"),
      f"⟨={code.count('⟨')} ⟩={code.count('⟩')}")

# 10. namespace name consistency
ns = re.search(r"namespace\s+(\w+)", code).group(1)
endns = re.search(r"end\s+(\w+)", code).group(1)
check("namespace_name_matches_end", ns == endns == "ClaimStatusRoutingV81", f"{ns}/{endns}")

# 11. every ExcludedClaim has a corresponding lean_does_not_prove_* theorem
excl_block = re.search(r"inductive ExcludedClaim where(.*?)deriving", code, re.DOTALL).group(1)
excl_ctors = re.findall(r"^\s*\|\s*(\w+)", excl_block, re.MULTILINE)
excl_refs = re.findall(r"provesExcludedClaim\s+ExcludedClaim\.(\w+)\s*=\s*false", code)
missing_e = sorted(set(excl_ctors) - set(excl_refs))
check("all_excluded_claims_have_nonentailment_theorem", not missing_e,
      f"excluded_claims={len(excl_ctors)} covered={len(set(excl_refs))} missing={missing_e}")

# --- report ---
digest = hashlib.sha256(src.encode("utf-8")).hexdigest()
passed = sum(1 for _,ok,_ in checks if ok)
total = len(checks)
print(f"FILE: {PATH}")
print(f"SHA256: {digest}")
print(f"OBJECTION_KINDS: {len(obj_ctors)}  CHANNEL_KINDS: {len(chan_ctors)}  THEOREMS: {len(thm_names)}")
print("-"*64)
for name, ok, detail in checks:
    print(f"[{'PASS' if ok else 'FAIL'}] {name:46s} {detail}")
print("-"*64)
print(f"RESULT: {passed}/{total} structural checks passed")
sys.exit(0 if passed == total else 1)
