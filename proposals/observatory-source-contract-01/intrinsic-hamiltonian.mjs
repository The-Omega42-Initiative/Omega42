export function intrinsicHamiltonian(){
const S=[0,1,2,4,5,7,8,10,11],target=[12,24,16],ks=[2,3,4];
// All exact edges of length 2,3,4 form components of diameter <=32.
// Normalize each component by a multiple of 12 so its minimum lies in [0,11].
// For the required k=3 capacity all eight modular edges must be exact in each copy.
const edges=k=>S.flatMap(r=>S.filter(s=>(r-s+12)%12===k).map(s=>[r,s]));
const e=ks.map(edges);const adj=new Map(S.map(r=>[r,[]]));for(const [r,s] of e[1]){adj.get(s).push([r,3]);adj.get(r).push([s,-3])}
let contradiction=null;const potentials=new Map();for(const r of S){if(potentials.has(r))continue;potentials.set(r,r);const q=[r];for(let i=0;i<q.length;i++)for(const [v,d] of adj.get(q[i])){const p=potentials.get(q[i])+d;if(!potentials.has(v)){potentials.set(v,p);q.push(v)}else if(potentials.get(v)!==p)contradiction={from:q[i],to:v,expected:p,actual:potentials.get(v)}}}
const cuts=S.map(c=>{const lifts=S.map(r=>r<c?r+12:r);const counts=ks.map(k=>lifts.reduce((n,r)=>n+lifts.filter(s=>r-s===k).length,0));return {cut:c,counts}});
if(!contradiction)throw Error('expected cycle obstruction');
return {schema:'omega42.intrinsic.hamiltonian.v1',modularCapacities:e.map(x=>x.length),frequency3Edges:e[1],contradiction,cuts,maxFrequency3PerCopy:6,threeCopyBound:18,target, boundary:'Same native logarithm or independent logarithms per copy; positive exact frequencies; no arbitrary superoperator.'};
}