export function reduction(){
 const rows=[];
 for(const p of [2,3,5,7,11])for(let k=1;k<=2;k++)for(let d=2;d<=6;d++)for(let t=0;t<=3;t++){
 const n=p**k,seen=new Set();let count=0;
 for(let a=0;a<n;a++)for(let b=0;b<n;b++){if(a%p===0&&b%p===0||seen.has(a*n+b))continue;let x=a,y=b;do{seen.add(x*n+y);[x,y]=[y,(x+t*y)%n]}while(x!==a||y!==b);count++}
 if(seen.size!==n*n-(n/p)**2)throw Error('census');
 const flags=[Array.from({length:p},(_,x)=>((x*x-t*x-1)%p+p)%p).every(Boolean),p!==2,count>1,d%2===1];
 rows.push({p,k,d,t,flags,primitiveOrbits:count});
 }
 const subsets=[];for(let mask=0;mask<16;mask++){const eligible=rows.filter(r=>r.flags.every((v,i)=>!(mask&(1<<i))||v));const m=eligible[0];subsets.push({mask,requirements:['U','P','D','C'].filter((_,i)=>mask&(1<<i)).join(''),count:eligible.length,minimum:[m.p,m.k,m.d,m.t],selectsTarget:m.p===3&&m.k===2&&m.d===3&&m.t===1,guaranteesAll:eligible.every(r=>r.flags.every(Boolean)),witness:eligible.find(r=>!r.flags.every(Boolean))??null})}
 return {schema:'omega42.constitution.reduction.v1',candidateCount:rows.length,subsets,scope:'Bounded search; lexicographic p,k,d,t; exact primitive orbit counts.'};
}
