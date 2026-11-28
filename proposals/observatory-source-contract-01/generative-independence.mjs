export function independence(){
 const gcd=(a,b)=>b?gcd(b,a%b):a;
 const rows=[];
 for(const p of [2,3,5,7,11])for(let k=1;k<=2;k++)for(let t=0;t<=3;t++){
 const n=p**k,seen=new Set();let primitiveOrbits=0,periods={};
 for(let a=0;a<n;a++)for(let b=0;b<n;b++){if(a%p===0&&b%p===0)continue;if(seen.has(a*n+b))continue;let x=a,y=b,l=0;do{seen.add(x*n+y);[x,y]=[y,(x+t*y)%n];l++}while(x!==a||y!==b);primitiveOrbits++;periods[l]=(periods[l]||0)+1}
 if(seen.size!==n*n-(n/p)**2)throw Error('primitive census mismatch');
 for(let d=2;d<=6;d++)rows.push({p,k,t,d,primitiveOrbits,periods,expansion:t>0,inert:Array.from({length:p},(_,x)=>((x*x-t*x-1)%p+p)%p).every(Boolean),polarity:p!==2,differentiation:primitiveOrbits>1,complementarity:gcd(2,d)===1});
 }
 const rules=['expansion','inert','polarity','differentiation','complementarity'];
 const implications=[];for(const a of rules)for(const b of rules)if(a!==b){const witness=rows.find(r=>r[a]&&!r[b]);implications.push({from:a,to:b,counterexample:witness??null})}
 const eligible=rows.filter(r=>rules.every(a=>r[a])).sort((a,b)=>a.p-b.p||a.k-b.k||a.d-b.d||a.t-b.t);
 return {schema:'omega42.independence.v1',candidateCount:rows.length,eligibleCount:eligible.length,minimum:eligible[0],implications,proxyFailures:rows.filter(r=>r.differentiation!==(r.k>1)).length,scope:'Five primes, depths 1–2, coefficients 0–3, companion degrees 2–6; no universal implication inferred from absence of counterexample.'};
}
