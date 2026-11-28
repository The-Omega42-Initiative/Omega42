export function authenticateEye(){
 const dr=x=>((x%9+9)%9)||9;const cycle=[2,5];while(cycle.length<24)cycle.push(dr(cycle.at(-1)+cycle.at(-2)));
 const positions=cycle.flatMap((x,i)=>x%3===0?[i]:[]),eyes=positions.map(i=>cycle[i]),sum=eyes.reduce((a,b)=>a+b,0);
 const overlap=positions.length,span=2*cycle.length-overlap;
 if(positions.join()!= '3,7,11,15,19,23'||eyes.join()!='3,9,6,6,9,3'||sum!==36||span!==42)throw Error('historical signature mismatch');
 const vertices=new Set();for(let i=0;i<24;i++){vertices.add('F'+i);vertices.add(positions.includes(i)?'F'+i:'R'+i)}
 if(vertices.size!==span)throw Error('quotient count');
 return {schema:'omega42.eye.authentication.v1',cycle,positions,indexing:'zero-based',eyes,localSum:sum,overlap,span,unitPositions:24-overlap,quotientVertices:vertices.size,source:'Companion V335 Rev450 STABLE math-gate; historical Protocol V150 GOLD',boundary:'Two copies glued at matching Eye positions is a specified construction, not forced by the recurrence alone.'};
}
