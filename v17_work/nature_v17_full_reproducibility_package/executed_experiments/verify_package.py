#!/usr/bin/env python3
from pathlib import Path
import hashlib,json,sys
root=Path(__file__).resolve().parent
mf=root/'package_manifest.json'
if not mf.exists():
    print('missing package_manifest.json');sys.exit(1)
data=json.loads(mf.read_text())
bad=[]
for rec in data['files']:
    p=root/rec['path']
    if not p.is_file():bad.append({'path':rec['path'],'error':'missing'});continue
    h=hashlib.sha256(p.read_bytes()).hexdigest()
    if h!=rec['sha256']:bad.append({'path':rec['path'],'error':'hash','expected':rec['sha256'],'actual':h})
    if p.stat().st_size!=rec['size_bytes']:bad.append({'path':rec['path'],'error':'size'})
listed={x['path'] for x in data['files']}
excluded={'package_manifest.json','MANIFEST.sha256'}
actual={str(p.relative_to(root)) for p in root.rglob('*') if p.is_file() and str(p.relative_to(root)) not in excluded}
extra=sorted(actual-listed);missing=sorted(listed-actual)
ok=not bad and not extra and not missing
print(json.dumps({'pass':ok,'listed_files':len(listed),'bad':bad,'extra':extra,'missing':missing},indent=2))
sys.exit(0 if ok else 1)
