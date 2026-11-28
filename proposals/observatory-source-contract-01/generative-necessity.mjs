export function necessity(){
 const gcd=(a,b)=>b?gcd(b,a%b):a;
 const primes=[2,3,5,7,11,13,17,19,23,29,31];
 const candidates=[];
 for(const p of primes)for(let k=1;k<=3;k++)for(let d=2;d<=6;d++)for(let t=0;t<=3;t++) {
 const inert=Array.from({length:p},(_,x)=>((x*x-t*x-1)%p+p)%p).every(Boolean);
 candidates.push({p,k,d,t,inert,polarity:p!==2,expansion:t>0,differentiation:k>1,complementarity:gcd(2,d)===1});
 }
 const rules=['expansion','inert','polarity','differentiation','complementarity'];
 const choose=omit=>{const eligible=candidates.filter(c=>rules.every(r=>r===omit||c[r]));return {count:eligible.length,minimum:eligible[0]??null}};
 return {schema:'omega42.necessity.v1',candidate_count:candidates.length,ordering:'lexicographic p,k,d,t',baseline:choose(null),ablations:rules.map(rule=>({removed:rule,...choose(rule)})),boundary:'Differentiation is a depth proxy, not an orbit test for arbitrary primes or generators. Reversibility is built into the matrix family. Minimality is an ordering, not a predicate.'};
}
