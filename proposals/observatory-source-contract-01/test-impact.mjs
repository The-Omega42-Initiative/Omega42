import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {impact} from './impact-engine.mjs';
const read=p=>JSON.parse(readFileSync(new URL(p,import.meta.url),'utf8'));
const g=read('./knowledge-graph.json'),r=read('./register.json');
assert.equal(g.nodes.length,221);
assert.equal(g.edges.length,283);
for(const record of r.records){
 const p=impact(g,r,record.id);
 const expected=new Set([record.id]);
 let changed=true;
 while(changed){changed=false;for(const e of g.edges){if(expected.has(e.to)&&!expected.has(e.from)){expected.add(e.from);changed=true}}}
 assert.deepEqual(new Set(p.affected.map(x=>x.id)),expected);
 assert.equal(p.affected.length,1+p.direct+p.indirect);
 assert.equal(p.mutation,'NONE');
}
const p=impact(g,r,'MF-01');
assert.equal(p.direct,17);assert.equal(p.indirect,134);assert.equal(p.certificates.length,23);
assert.throws(()=>impact(g,r,'MF-999'));
assert.throws(()=>impact({...g,source:{blob:'wrong'}},r,'MF-01'));
console.log('Impact regression: 221 independent fixed-point comparisons passed');
