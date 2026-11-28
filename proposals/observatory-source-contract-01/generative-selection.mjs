export function select(limit=12){
 const gcd=(a,b)=>b?gcd(b,a%b):a;
 const pairs=[];for(let a=2;a<=limit;a++)for(let b=a+1;b<=limit;b++)if(gcd(a,b)===1)pairs.push({a,b,degree:a*b});
 pairs.sort((x,y)=>x.degree-y.degree||x.a-y.a);
 const depths=[];for(let k=1;k<=5;k++){const n=3**k,order=8*3**(k-1);depths.push({k,n,states:n*n,order,primitiveOrbits:3**(k-1),nontrivialLift:k>1,distinctPrimitiveOrbits:k>1})}
 const primes=[2,3,5,7,11,13,17,19,23,29,31];const alternatives=primes.map(p=>({p,distinctPolarity:p!==2,inert:Array.from({length:p},(_,x)=>((x*x-x-1)%p+p)%p).every(Boolean),quotient:p*p-p+1}));
 return {pairs,depths,alternatives,selectedPair:pairs[0],selectedDepth:depths.find(x=>x.nontrivialLift),selectedPrime:alternatives.find(x=>x.distinctPolarity&&x.inert)};
}
