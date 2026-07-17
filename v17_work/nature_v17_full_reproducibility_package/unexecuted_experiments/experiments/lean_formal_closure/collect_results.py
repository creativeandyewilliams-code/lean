#!/usr/bin/env python3
from pathlib import Path
import argparse, json, re, hashlib
ap=argparse.ArgumentParser();ap.add_argument('--out',required=True);a=ap.parse_args();o=Path(a.out)
ax=(o/'axiom_report.txt').read_text(errors='replace')
forbidden=['sorryAx','propext','Classical.choice','Quot.sound']
summary={'build_exit':int((o/'lake_build.exit').read_text()),'axiom_report_present':bool(ax.strip()),'forbidden_axiom_mentions':{x:len(re.findall(re.escape(x),ax)) for x in forbidden},'source_unchanged':not (o/'source_mutation.diff').read_text().strip()}
(o/'summary.json').write_text(json.dumps(summary,indent=2))
h=hashlib.sha256();
for f in ['lake_build.stdout','lake_build.stderr','axiom_report.txt','mutation_checks.txt','summary.json']:h.update((o/f).read_bytes())
(o/'result_fingerprint.txt').write_text(h.hexdigest()+'\n')
print(json.dumps(summary,indent=2))
