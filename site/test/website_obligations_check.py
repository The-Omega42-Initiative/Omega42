"""Check structural coverage, not semantic coherence or visitor resonance."""
import json, pathlib, sys
root=pathlib.Path(__file__).resolve().parents[2]
data=json.loads((root/'site/assets/website-obligations.json').read_text())
ids=set()
for item in data['items']:
    assert item['id'] not in ids, item['id']
    ids.add(item['id'])
    assert item['status'] in {'IMPLEMENTED_UNVERIFIED','PARTIAL','OUTSTANDING'}
    if item['source']: assert (root/item['source']).is_file(), item['source']
    if item['page']: assert (root/'site/pages'/ (item['page']+'.html')).is_file(), item['page']
    if item['status']=='IMPLEMENTED_UNVERIFIED': assert item['source']
print(f'{len(ids)} obligation records: structural checks passed; verification not implied')
