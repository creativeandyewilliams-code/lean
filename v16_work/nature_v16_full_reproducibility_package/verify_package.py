#!/usr/bin/env python3
"""Package verification for the Nature v16 reproducibility package.
Returns nonzero on any failure. Run from the package root."""
import json, os, re, sys, hashlib, glob

ROOT = os.path.dirname(os.path.abspath(__file__))
os.chdir(ROOT)
fail = []
def check(cond, msg):
    print(("  ok  " if cond else "FAIL  ") + msg)
    if not cond:
        fail.append(msg)

print("== required paths ==")
required = [
 "README.md","CHANGELOG_v16.md","release_metadata.json","package_manifest.json",
 "MANIFEST.sha256","run_all.sh","Makefile","verify_package.py","requirements.lock",
 "original_inputs/nature_v8_full_reproducibility_package.zip",
 "lean/lean-toolchain","lean/lakefile.toml","lean/FmiCns.lean",
 "lean/reports/static_audit.txt","lean/reports/theorem_coverage.json",
 "lean/reports/toolchain_block_evidence.txt",
 "experiments/gate_zero_v16/reports/gate_zero_v16.json",
 "experiments/gate_zero_v16/reports/result_crosswalk.csv",
 "experiments/direct_recurrence/code/run_recurrence.py",
 "experiments/direct_recurrence/derived/summary.json",
 "experiments/direct_recurrence/derived/recurrence_table.csv",
 "experiments/direct_recurrence/figures/recurrence_backlog.png",
 "experiments/semantic_equivalence/reports/semantic_equivalence_results.json",
 "experiments/gf_branch_closure/reports/branch_hazard_results.json",
 "receiver/sealed_ground_truth/answer_key.json",
 "receiver/scoring/receiver_scores.json",
 "reports/final_status_vector.json","reports/executive_gate_report.md",
 "reports/gate_zero_v16.md","reports/lean_formal_closure.md",
 "reports/receiver_propagation.md",
 "manuscript/article/nature_article_v16.pdf",
 "manuscript/article/nature_article_v16.tex",
 "manuscript/article/nature_article_v16.docx",
 "manuscript/article/nature_article_v16.md",
 "manuscript/supplement/nature_supplement_v16.pdf",
 "manuscript/supplement/nature_supplement_v16.tex",
 "manuscript/supplement/nature_supplement_v16.docx",
 "manuscript/supplement/nature_supplement_v16.md",
]
for p in required:
    check(os.path.exists(p), f"exists: {p}")

print("== no broken symlinks ==")
broken = [p for p in glob.glob("**/*", recursive=True) if os.path.islink(p) and not os.path.exists(p)]
check(not broken, f"no broken symlinks ({len(broken)} found)")

print("== no forbidden absolute user paths in execution-critical source ==")
pats = re.compile(r"/home/user|/mnt/data|/Users/")
srcs = (glob.glob("tools/*.py") + glob.glob("experiments/*/code/*.py")
        + glob.glob("lean/**/*.lean", recursive=True)
        + ["run_all.sh","Makefile"]  # verify_package.py itself defines the pattern literals
        + glob.glob("manuscript/*/*.mns") + glob.glob("manuscript/*/*.tex")
        + glob.glob("manuscript/*/*.md"))
badpath = [p for p in srcs if os.path.exists(p) and pats.search(open(p,encoding="utf-8",errors="ignore").read())]
check(not badpath, f"no absolute user paths in source ({badpath})")

print("== lean sorry/admit token scan (.lean only) ==")
tok = re.compile(r"\bsorry\b|\bsorryAx\b|\badmit\b")
leanbad = [p for p in glob.glob("lean/**/*.lean", recursive=True) if tok.search(open(p).read())]
check(not leanbad, f"no sorry/admit in .lean ({leanbad})")
axdecl = [p for p in glob.glob("lean/**/*.lean", recursive=True)
          if re.search(r"^\s*axiom\s", open(p).read(), re.M)]
check(not axdecl, f"no axiom declarations in .lean ({axdecl})")

print("== placeholder scan (manuscripts + README) ==")
ph = re.compile(r"REPOSITORY DOI|PRIVATE REVIEWER LINK|\bTODO\b|\bTBD\b|PLACEHOLDER|\[INSERT")
phbad = []
for p in ["README.md"] + glob.glob("manuscript/*/*.mns") + glob.glob("manuscript/*/*.md"):
    if os.path.exists(p) and ph.search(open(p,encoding="utf-8",errors="ignore").read()):
        phbad.append(p)
check(not phbad, f"no unapproved placeholders ({phbad})")

print("== Gate Zero crosswalk exact ==")
gz = json.load(open("experiments/gate_zero_v16/reports/gate_zero_v16.json"))
check(gz["disposition"] == "closed-positive", "gate zero closed-positive")
check(gz["key_value_crosswalk_exact_matches"] == gz["key_value_crosswalk_total"],
      f"gate zero crosswalk {gz['key_value_crosswalk_exact_matches']}/{gz['key_value_crosswalk_total']}")
check(gz["model_hash_matches"] and gz["registry_hash_matches"], "gate zero hashes match")

print("== recurrence table/summary consistency ==")
summ = json.load(open("experiments/direct_recurrence/derived/summary.json"))["summary"]
import csv
tab = list(csv.reader(open("experiments/direct_recurrence/derived/recurrence_table.csv")))
tab_fixed = [r for r in tab if r and r[0] == "Fixed post-lift"]
check(bool(tab_fixed), "recurrence table has Fixed post-lift row")
check(abs(summ["fixed_post_lift"]["final_backlog_mean"] - 694.1) < 5, "fixed final backlog ~694")
check(summ["fixed_post_lift"]["recurrence_prop"] == 1.0
      and summ["proportional_service"]["recurrence_prop"] == 0.0,
      "recurrence verdicts (fixed=1, proportional=0)")

print("== receiver study ==")
rs = json.load(open("receiver/scoring/receiver_scores.json"))
check(rs["second_generation_success"] is True, "receiver second-generation success")
check(rs["author_repair_count"] == 0, "receiver 0 author repairs")
check(rs["by_condition"]["formal_package"]["theorem_identity_recovery"] >
      rs["by_condition"]["prose_only"]["theorem_identity_recovery"],
      "formal > prose on theorem-identity recovery")

print("== manuscripts render + availability ==")
try:
    from pdfminer.pdfpage import PDFPage
    for pdf in ["manuscript/article/nature_article_v16.pdf",
                "manuscript/supplement/nature_supplement_v16.pdf"]:
        n = len(list(PDFPage.get_pages(open(pdf, "rb"))))
        check(n > 0, f"{pdf} has {n} pages")
except Exception as e:
    check(False, f"pdf page check error: {e}")
readme = open("README.md").read() if os.path.exists("README.md") else ""
for claimed in ["lean/", "experiments/", "receiver/", "original_inputs/"]:
    check(os.path.isdir(claimed.rstrip("/")), f"README-claimed dir exists: {claimed}")

print("\n== MANIFEST.sha256 integrity (sample) ==")
if os.path.exists("MANIFEST.sha256"):
    lines = [l for l in open("MANIFEST.sha256").read().splitlines() if l.strip()]
    bad = 0
    for l in lines[:200]:
        h, _, path = l.partition("  ")
        if path == "MANIFEST.sha256": continue
        if not os.path.exists(path):
            bad += 1; continue
        actual = hashlib.sha256(open(path, "rb").read()).hexdigest()
        if actual != h: bad += 1
    check(bad == 0, f"manifest hash sample verified (mismatches={bad})")

print("\n" + ("VERIFY: PASS" if not fail else f"VERIFY: FAIL ({len(fail)} issues)"))
sys.exit(0 if not fail else 1)
