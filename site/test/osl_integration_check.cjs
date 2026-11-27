const assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path');const base=path.resolve(__dirname,'../assets');const M=require(base+'/research-suite-reference.js'),A=require(base+'/atlas-data.js'),B=require(base+'/osl-research-bindings.js');const w={};new Function('window',fs.readFileSync(base+'/adaptor_rs.js','utf8'))(w);const x=B(M,w.Omega42AD008,A);const tests=[
['LEX.EQUIVALENTS ["golden split"]',r=>r.length===3],
['SPEC.PROJECT [1,2]',r=>r.plus.every((v,i)=>Math.abs(v+r.minus[i]-[1,2][i])<1e-12)],
['SPEC.DEFICIT [1]',r=>Math.abs(r.deficit-0.625)<1e-12],
['CODE.ENCODE [2,5]',r=>JSON.stringify(r)==='[2,0,4,0,2,3,3]'],
['CODE.RECONSTRUCT [[3,0,4,0,2,3,5]]',r=>r.candidate.state.join(',')==='2,5'&&r.candidate.errors===2],
['OBS.PARTITION [2,[0,2,5]]',r=>r.classes===81&&r.pairs===0],
['OBS.DESCEND [2,[0,2,5]]',r=>r.consistent&&r.below.classes===9],
['OBS.COMPLETE [2,[0,2],[1,3,4,5]]',r=>r.ambiguous===24&&r.unresolved===0],
['MEM.INVARIANT [3,3]',r=>r.text==='1/9'],
['MEM.EXTINCTION [3,3]',r=>r===2],
['MEM.LIFT [3,1,3,3]',r=>r.rows.at(-1).moving===0&&r.invariant==='1/9'],
['DESIGN.RING [2]',r=>r.pass&&r.pairs===3240],
['GEN.DISTANCE [3,"ACS",1,1]',r=>r.distance===7&&r.reached===729],
['GEN.MINSET [2]',r=>r.map(v=>v.ops).sort().join(',')==='ACS,AVC'],
['ADAPT.DEFECT [24,7]',r=>r.defect===3],
['ADAPT.COMPOSE [24,12,7]',r=>r.composite===2&&r.bound===2]];
assert.equal(A.length,17);assert.equal(x.names.length,tests.length);for(const [c,check] of tests)assert.ok(check(x.execute(c).result),c);
for(const c of ['LEX.EQUIVALENTS [""]','OBS.PARTITION [9,[]]','CODE.ENCODE [9,0]','GEN.DISTANCE [3,"AA",1,1]'])assert.throws(()=>x.execute(c));
console.log('16 positive assertions, 4 negative controls passed');
