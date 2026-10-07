#!/usr/bin/env python3
"""Maintained HTML → Nift raw composition. No Markdown renderer/imports."""
from pathlib import Path
import argparse,json,shutil,subprocess,time,sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from publication.chrome import Chrome
from publication.ownership import reconcile
from publication.publish import publish
ROOT=Path(__file__).resolve().parents[1]
parser=argparse.ArgumentParser();parser.add_argument('--all',action='store_true');parser.add_argument('--setup',action='store_true');args=parser.parse_args()
if args.setup:
    subprocess.run(['npm','install','--prefix',str(ROOT/'.cache/publication-tools'),'--cache',str(ROOT/'.cache/npm-cache'),'--no-audit','--no-fund','pagefind@1.5.2'],cwd=ROOT,check=True)
    print('Pinned Pagefind setup completed; no Markdown renderer in this project.');raise SystemExit()
def write_changed(file,value):
    file.parent.mkdir(parents=True,exist_ok=True)
    if not file.exists() or file.read_text()!=value:file.write_text(value)
def emit(file):
    literal=json.dumps(file);return '@dep('+literal+')$[rawHtml('+literal+')]'
start=time.perf_counter();publication_model=json.loads((ROOT/'data/publication.json').read_text());chrome=Chrome(ROOT,publication_model,force=args.all);manifest=json.loads((ROOT/'data/composition.json').read_text());reconcile(ROOT,manifest)
for record in manifest['pages']:
    dependencies=chrome.render(record)
    source=''.join('@dep('+json.dumps(v)+')' for v in dependencies)+'@dep("data/composition.json")'+''.join(emit(piece if piece else record['body']) for piece in record['pieces'])
    write_changed(ROOT/'.generated/content'/((record['name'] if record['name']!='/' else 'index')+'.html'),source)
chrome.close();prepare=time.perf_counter()-start;asset_start=time.perf_counter();count=0
for file in (ROOT/'public-assets').rglob('*'):
    if not file.is_file():continue
    target=ROOT/'public'/file.relative_to(ROOT/'public-assets');target.parent.mkdir(parents=True,exist_ok=True)
    if not target.exists() or target.stat().st_size!=file.stat().st_size or target.read_bytes()!=file.read_bytes():shutil.copy2(file,target)
    count+=1
assets=time.perf_counter()-asset_start;compose_start=time.perf_counter();subprocess.run(['nift','build',*(['--all'] if args.all else [])],cwd=ROOT,check=True)
nift_wall=time.perf_counter()-compose_start;publication_report=publish(model=publication_model,force=args.all)
report={'model':'maintained HTML → Nift composition','composition_prepare_s':prepare,'asset_publication_s':assets,'asset_files':count,'nift_composition_s':nift_wall,'total_s':time.perf_counter()-start,'publication':publication_report}
write_changed(ROOT/'.generated/build-report.json',json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
