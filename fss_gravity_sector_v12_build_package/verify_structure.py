#!/usr/bin/env python3
"""
Structural verifier for fss_gravity_sector_v12_routing_skeleton.lean

This does NOT run the Lean kernel. It performs source-level structural checks
that a `lake build` would otherwise subsume, so the build certificate can state
exactly what was machine-checked in this sandbox versus what requires an
external Lean toolchain.
"""
import re, sys, hashlib

PATH = sys.argv[1] if len(sys.argv) > 1 else "fss_gravity_sector_v12_routing_skeleton.lean"
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
for ind in ["ClaimKind","PhysicsGate","ObjectionKind","RoutedStatus","ExcludedClaim"]:
    check(f"inductive_{ind}", re.search(rf"inductive\s+{ind}\b", code), ind)

# 4. enumerate ObjectionKind constructors and confirm route covers all
obj_block = re.search(r"inductive ObjectionKind where(.*?)deriving", code, re.DOTALL).group(1)
obj_ctors = re.findall(r"^\s*\|\s*(\w+)", obj_block, re.MULTILINE)
route_block = re.search(r"def route :.*?(?=\n/--|\ndef |\nstructure )", code, re.DOTALL).group(0)
routed = re.findall(r"ObjectionKind\.(\w+)\s*=>", route_block)
missing = sorted(set(obj_ctors) - set(routed))
extra   = sorted(set(routed) - set(obj_ctors))
check("route_exhaustive", not missing and not extra,
      f"objection_ctors={len(obj_ctors)} routed={len(routed)} missing={missing} extra={extra}")

# 5. allObjections lists every constructor exactly once
all_block = re.search(r"def allObjections.*?\]", code, re.DOTALL).group(0)
listed = re.findall(r"ObjectionKind\.(\w+)", all_block)
check("allObjections_complete",
      sorted(listed) == sorted(obj_ctors) and len(listed) == len(set(listed)),
      f"listed={len(listed)} unique={len(set(listed))} ctors={len(obj_ctors)}")

# 6. every theorem closes with a tactic block (rfl/decide/refine) — no dangling
thm_names = re.findall(r"^\s*theorem\s+(\w+)", code, re.MULTILINE)
check("theorems_present", len(thm_names) >= 30, f"count={len(thm_names)}")
# each theorem body must contain at least one terminal tactic
bodies = re.split(r"^\s*theorem\s+\w+", code, flags=re.MULTILINE)[1:]
closed = all(re.search(r"\b(rfl|decide)\b", b.split("theorem")[0]) for b in bodies)
check("theorems_have_terminal_tactic", closed, "rfl/decide present in each body")

# 7. provesExcludedClaim is constant false
check("provesExcludedClaim_false",
      re.search(r"def provesExcludedClaim.*?:=\s*false", code, re.DOTALL), "constant false")

# 8. v12 required new lemmas present
for req in ["provesExcludedClaim_is_constant_false",
            "route_never_yields_projectionDefeat",
            "route_total_over_enumeration",
            "stability_concerns_share_status",
            "quantum_boundary_concerns_share_status",
            "provenance_version_is_12"]:
    check(f"has_{req}", req in code, req)

# 9. balanced anonymous-constructor brackets in refine proofs
check("angle_brackets_balanced", code.count("⟨") == code.count("⟩"),
      f"⟨={code.count('⟨')} ⟩={code.count('⟩')}")

# 10. namespace name consistency
ns = re.search(r"namespace\s+(\w+)", code).group(1)
endns = re.search(r"end\s+(\w+)", code).group(1)
check("namespace_name_matches_end", ns == endns == "FSSGravitySectorV12", f"{ns}/{endns}")

# --- report ---
digest = hashlib.sha256(src.encode("utf-8")).hexdigest()
passed = sum(1 for _,ok,_ in checks if ok)
total = len(checks)
print(f"FILE: {PATH}")
print(f"SHA256: {digest}")
print(f"OBJECTION_KINDS: {len(obj_ctors)}  THEOREMS: {len(thm_names)}")
print("-"*64)
for name, ok, detail in checks:
    print(f"[{'PASS' if ok else 'FAIL'}] {name:42s} {detail}")
print("-"*64)
print(f"RESULT: {passed}/{total} structural checks passed")
sys.exit(0 if passed == total else 1)
