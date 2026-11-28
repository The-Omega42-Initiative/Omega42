export function crownRecovery(){
 const dr=x=>((x%9+9)%9)||9;let a=2,b=5;const cycle=[];
 for(let i=0;i<24;i++){cycle.push(dr(a));[a,b]=[b,(a+b)%9]}
 const positions=cycle.map((v,i)=>v%3===0?i+1:0).filter(Boolean);
 // Archived P numbering starts with the second seed, not the first.
 const P=cycle.slice(1).concat(cycle[0]);const eyes=P.map((v,i)=>({position:i+1,value:v})).filter(x=>x.value%3===0);
 const sum=eyes.reduce((s,x)=>s+x.value,0),gap=eyes.length,diameter=sum+gap,index=3*3-3+1;
 if(JSON.stringify(eyes.map(x=>x.position))!=='[3,7,11,15,19,23]'||JSON.stringify(eyes.map(x=>x.value))!=='[3,9,6,6,9,3]'||sum!==36||gap!==6||diameter!==42||diameter!==gap*index)throw Error('crown recovery');
 return {schema:'omega42.crown.recovery.v1',P,eyes,sum,gap,diameter,index,unitPositions:24-gap,source:'Archived V334 Rev.389 Crown Eyes and Constitutional Constants; P indexing inferred by exact matching',boundary:'Gap equals eye count and scalar unit count here; quotient correspondence is numerical, not an operator isomorphism.'};
}
