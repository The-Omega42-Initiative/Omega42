export function universalGenerator(bound=8){
 if(!Number.isInteger(bound)||bound<1||bound>15)throw Error('bound 1..15');
 let reversible=0,expanding=0,minimal=0,positiveTrace=0,negativeTrace=0,conjugateWitnesses=0;const unresolved=[],nonexpandingUnity=[];
 for(let a=-bound;a<=bound;a++)for(let b=-bound;b<=bound;b++)for(let c=-bound;c<=bound;c++)for(let d=-bound;d<=bound;d++){
 const det=a*d-b*c,tr=a+d;if(Math.abs(det)!==1)continue;reversible++;
 const grows=det===-1?tr!==0:Math.abs(tr)>2;
 if(!grows){if(Array.from({length:3},(_,x)=>((x*x-tr*x+det)%3+3)%3).every(Boolean)&&nonexpandingUnity.length<5)nonexpandingUnity.push({matrix:[a,b,c,d],tr,det});continue}
 expanding++;if(det!==-1||Math.abs(tr)!==1)continue;minimal++;if(tr===1)positiveTrace++;else negativeTrace++;
 // Normalize sign, then P=[v,Mv] satisfies MP=PA by Cayley-Hamilton.
 const s=tr;let found=false;
 for(let x=-bound;x<=bound&&!found;x++)for(let y=-bound;y<=bound&&!found;y++){
 const u=s*(a*x+b*y),v=s*(c*x+d*y);
 if(Math.abs(x*v-y*u)===1){found=true;conjugateWitnesses++}
 }
 if(!found)unresolved.push([a,b,c,d]);
 }
 return {schema:'omega42.universal.generator.v1',bound,reversible,expanding,minimal,positiveTrace,negativeTrace,conjugateWitnesses,unresolved,nonexpandingUnity,scope:'Bounded entry enumeration and bounded integral basis witness search; analytic spectral minimum is separate.'};
}
