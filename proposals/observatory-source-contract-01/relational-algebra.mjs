export function relationalAlgebra(q=7){
 if(![7,9,27].includes(q))throw Error('supported fields: 7,9,27');
 const p=q===7?7:3,n=q===7?1:q===9?2:3;
 const digits=x=>Array.from({length:n},(_,i)=>Math.floor(x/p**i)%p);
 const enc=a=>a.reduce((s,x,i)=>s+((x%p+p)%p)*p**i,0);
 const add=(a,b)=>enc(digits(a).map((x,i)=>x+digits(b)[i]));
 const mul=(a,b)=>{const x=digits(a),y=digits(b),z=Array(2*n-1).fill(0);for(let i=0;i<n;i++)for(let j=0;j<n;j++)z[i+j]+=x[i]*y[j];for(let k=z.length-1;k>=n;k--){z[k-n]+=(n===3?-1:1)*z[k];z[k-n+1]+=z[k]}return enc(z.slice(0,n))};
 const inv=Array.from({length:q},(_,a)=>Array.from({length:q},(_,b)=>b).find(b=>mul(a,b)===1));
 const maps=[];for(let a=1;a<q;a++)for(let b=0;b<q;b++)maps.push([a,b]);
 const apply=([a,b],x)=>add(mul(a,x),b);
 const compose=([a,b],[c,d])=>[mul(a,c),add(mul(a,d),b)];
 const images=new Set(maps.map(f=>apply(f,0)+','+apply(f,1)));
 if(images.size!==maps.length||inv.slice(1).some(x=>x===undefined))throw Error('field or sharp transitivity');
 let checks=0;for(const f of maps)for(const g of maps){const h=compose(f,g);for(const x of [0,1]){if(apply(h,x)!==apply(f,apply(g,x)))throw Error('composition');checks++}}
 return {schema:'omega42.relational.algebra.v1',q,affineOrder:maps.length,orderedPairImages:images.size,compositionChecks:checks,fieldModel:n===1?'F7':n===2?'F3[x]/(x²-x-1)':'F3[x]/(x³-x+1)',boundary:'F9 affine group has 72 elements; the 81-state Z9 module is not this field or group.'};
}
