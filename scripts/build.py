#!/usr/bin/env python3
"""Maintained HTML → Nift raw composition. No Markdown renderer/imports."""
from pathlib import Path
import argparse,json,shutil,subprocess,time
ROOT=Path(__file__).resolve().parents[1]
parser=argparse.ArgumentParser();parser.add_argument('--all',action='store_true');args=parser.parse_args()
def write_changed(file,value):
    file.parent.mkdir(parents=True,exist_ok=True)
    if not file.exists() or file.read_text()!=value:file.write_text(value)
def emit(file):
    literal=json.dumps(file);return '@dep('+literal+')$[rawHtml('+literal+')]'
start=time.perf_counter();manifest=json.loads((ROOT/'data/composition.json').read_text())
for record in manifest['pages']:
    source='@dep("data/composition.json")'+''.join(emit(piece if piece else record['body']) for piece in record['pieces'])
    write_changed(ROOT/'.generated/content'/((record['name'] if record['name']!='/' else 'index')+'.html'),source)
prepare=time.perf_counter()-start;asset_start=time.perf_counter();count=0
for file in (ROOT/'public-assets').rglob('*'):
    if not file.is_file():continue
    target=ROOT/'public'/file.relative_to(ROOT/'public-assets');target.parent.mkdir(parents=True,exist_ok=True)
    if not target.exists() or target.stat().st_size!=file.stat().st_size or target.read_bytes()!=file.read_bytes():shutil.copy2(file,target)
    count+=1
assets=time.perf_counter()-asset_start;compose_start=time.perf_counter();subprocess.run(['nift','build',*(['--all'] if args.all else [])],cwd=ROOT,check=True)
report={'model':'maintained HTML → Nift composition','composition_prepare_s':prepare,'asset_publication_s':assets,'asset_files':count,'nift_composition_s':time.perf_counter()-compose_start,'total_s':time.perf_counter()-start,'search':'C2 frozen reference search fixture; fresh publication/indexing is not benchmarked.'}
write_changed(ROOT/'.generated/build-report.json',json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
