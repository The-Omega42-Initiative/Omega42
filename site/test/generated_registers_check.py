import json, pathlib, sys
from html.parser import HTMLParser
root=pathlib.Path(__file__).resolve().parents[2]
out=pathlib.Path(sys.argv[1])
class IDs(HTMLParser):
    def __init__(self):
        super().__init__(); self.ids=[]
    def handle_starttag(self,tag,attrs):
        for k,v in attrs:
            if k=='id': self.ids.append(v)
for record,key,page in [('discoveries','discoveries','discovery-register.html'),('open','items','open-register.html')]:
    items=json.loads((root/'records'/record/'register.json').read_text())[key]
    parser=IDs();parser.feed((out/page).read_text())
    for item in items:
        assert parser.ids.count(item['id'].lower())==1, (page,item['id'])
    print(page,len(items),'canonical identifiers present exactly once')
