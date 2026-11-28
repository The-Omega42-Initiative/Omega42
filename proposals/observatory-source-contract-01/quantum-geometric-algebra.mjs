export function geometricAlgebra(){
const S=[0,1,2,4,5,7,8,10,11],g=[[2,12],[3,24],[4,16]],mod=x=>(x%12+12)%12;
const basis=[];for(let c=0;c<3;c++)for(const r of S)for(const s of S)basis.push({c,r,s,k:mod(r-s)});
const cols=g.flatMap(([k,n])=>basis.filter(v=>v.k===k).slice(0,n));
const results=[];let checks=0;
for(let c=0;c<3;c++){
const edges=cols.filter(v=>v.c===c),adj=new Map(S.map(r=>[r,new Set()]));for(const {r,s} of edges){adj.get(r).add(s);adj.get(s).add(r)}
const seen=new Set(),components=[];for(const r of S){if(seen.has(r))continue;const queue=[r];seen.add(r);for(let i=0;i<queue.length;i++)for(const s of adj.get(queue[i]))if(!seen.has(s)){seen.add(s);queue.push(s)}components.push(queue)}
const initial=new Set(edges.flatMap(({r,s})=>[r+','+s,s+','+r]));const closure=new Set(initial);let changed=true;while(changed){changed=false;for(const a of [...closure])for(const b of [...closure]){const [r,s]=a.split(',').map(Number),[u,v]=b.split(',').map(Number);checks++;if(s===u&&r!==v&&!closure.has(r+','+v)){closure.add(r+','+v);changed=true}}}
const off=components.reduce((t,a)=>t+a.length*(a.length-1),0),diag=components.reduce((t,a)=>t+a.length-1,0);if(closure.size!==off)throw Error('closure');
results.push({component:c,edges:edges.length,components,offDiagonal:off,diagonal:diag,lieDimension:off+diag,newDirections:off+diag-2*edges.length});
}
return {schema:'omega42.quantum.geometric.algebra.v1',initial:104,results,lieDimension:results.reduce((t,r)=>t+r.lieDimension,0),checks,boundary:'Componentwise matrix commutator; graph closure in inherited spectral basis; no physical symplectic identification.'};
}