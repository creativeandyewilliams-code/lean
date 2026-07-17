#!/usr/bin/env python3
from __future__ import annotations
import argparse, csv, hashlib, json, os, subprocess, sys, time, zipfile
from pathlib import Path
PROTOCOL={'id':'EXP-GATE-ZERO-V16-RERUN','required':['generator','raw event log','trajectory table','registry','frozen configuration','conformance suite','environment specification','source data/figures','checksums'],'acceptance':'generator and conformance exit 0; regenerated key results equal frozen record'}

def locate(root):
 cands=list(root.rglob('run_experiment.py'))
 if len(cands)!=1: raise RuntimeError(f'expected one run_experiment.py, found {len(cands)}')
 return cands[0].parent

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--out',required=True);a=ap.parse_args();out=Path(a.out)
 for s in ['raw','derived','logs','reports']:(out/s).mkdir(parents=True,exist_ok=True)
 (out/'protocol.json').write_text(json.dumps(PROTOCOL,indent=2))
 zip_path=Path(__file__).resolve().parents[3]/'original_inputs'/'nature_v8_full_reproducibility_package.zip'
 work=out/'raw'/'extracted';work.mkdir(parents=True,exist_ok=True)
 with zipfile.ZipFile(zip_path) as z:z.extractall(work)
 pkg=locate(work); frozen=json.loads((pkg/'data'/'key_results.json').read_text())
 t=time.time();p=subprocess.run([sys.executable,'run_experiment.py'],cwd=pkg,text=True,capture_output=True);elapsed=time.time()-t
 (out/'logs'/'run_stdout.txt').write_text(p.stdout);(out/'logs'/'run_stderr.txt').write_text(p.stderr);(out/'logs'/'run_exit.txt').write_text(str(p.returncode)+'\n');(out/'logs'/'run_seconds.txt').write_text(f'{elapsed:.6f}\n')
 if p.returncode!=0: raise SystemExit(p.returncode)
 regenerated=json.loads((pkg/'data'/'key_results.json').read_text())
 q=subprocess.run([sys.executable,'tests/test_conformance.py'],cwd=pkg,text=True,capture_output=True)
 (out/'logs'/'conformance_stdout.txt').write_text(q.stdout);(out/'logs'/'conformance_stderr.txt').write_text(q.stderr);(out/'logs'/'conformance_exit.txt').write_text(str(q.returncode)+'\n')
 keys=sorted(set(frozen)|set(regenerated));rows=[]
 for k in keys:
  fv=frozen.get(k);rv=regenerated.get(k);rows.append([k,json.dumps(fv,sort_keys=True),json.dumps(rv,sort_keys=True),int(fv==rv)])
 with open(out/'derived'/'result_crosswalk.csv','w',newline='') as f:
  w=csv.writer(f);w.writerow(['key','frozen','regenerated','exact_match']);w.writerows(rows)
 summary={'generator_exit':p.returncode,'conformance_exit':q.returncode,'key_count':len(rows),'exact_matches':sum(r[3] for r in rows),'all_exact':all(r[3] for r in rows),'elapsed_seconds':elapsed,'zip_sha256':hashlib.sha256(zip_path.read_bytes()).hexdigest()}
 (out/'derived'/'summary.json').write_text(json.dumps(summary,indent=2))
 (out/'reports'/'results.md').write_text(f"""# Gate Zero v16 rerun\n\n- Generator exit: {p.returncode}\n- Conformance exit: {q.returncode}\n- Frozen/regenerated key results: {summary['exact_matches']}/{summary['key_count']} exact\n- v8 input ZIP SHA-256: `{summary['zip_sha256']}`\n\nThis closes computational lineage and exact regeneration for the supplied v8 finite realization. It does not promote the finite realization to external validation.\n""")
 h=hashlib.sha256(); stable={'generator_exit':p.returncode,'conformance_exit':q.returncode,'key_count':len(rows),'exact_matches':sum(r[3] for r in rows),'all_exact':all(r[3] for r in rows),'zip_sha256':summary['zip_sha256']}; h.update(json.dumps(stable,sort_keys=True).encode()); h.update((out/'derived'/'result_crosswalk.csv').read_bytes()); (out/'reports'/'derived_fingerprint.txt').write_text(h.hexdigest()+'\n')
 if q.returncode!=0 or not summary['all_exact']:raise SystemExit(1)
 print(json.dumps(summary,indent=2))
if __name__=='__main__':main()
