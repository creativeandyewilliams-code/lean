#!/usr/bin/env python3
from pathlib import Path
import argparse, json, sys
ap=argparse.ArgumentParser(); ap.add_argument('--frozen',required=True); ap.add_argument('--rebuilt',required=True)
a=ap.parse_args(); frozen=Path(a.frozen); rebuilt=Path(a.rebuilt)
mapdirs={
 'gate_zero':'gate_zero',
 'direct_recurrence':'direct_recurrence',
 'semantic_equivalence_structural':'semantic_equivalence_structural',
 'governance_option_monotonicity':'governance_option_monotonicity',
 'gf_branch_hazard_robust':'gf_branch_hazard_robust',
 'cst_computational_geometry':'cst_computational_geometry',
}
fail=[]
for fdir,rdir in mapdirs.items():
    fp=(frozen/fdir/'reports'/'derived_fingerprint.txt').read_text().strip()
    rp=(rebuilt/rdir/'reports'/'derived_fingerprint.txt').read_text().strip()
    ok=fp==rp
    print(f'{fdir}: {"MATCH" if ok else "MISMATCH"} {fp[:16]} {rp[:16]}')
    if not ok: fail.append(fdir)
if fail:
    print('Fingerprint mismatches:', ', '.join(fail), file=sys.stderr); sys.exit(1)
