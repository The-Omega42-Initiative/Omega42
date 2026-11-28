export function eyeObstruction(){
 const mod=x=>(x%9+9)%9, dr=x=>mod(x)||9;
 const orbit=[];let a=2,b=5;for(let i=0;i<24;i++){orbit.push([a,b]);[a,b]=[b,mod(a+b)]}
 const hist={},nonlinear=[];let checks=0;
 for(let u=0;u<9;u++)for(let v=0;v<9;v++)for(let j=0;j<24;j++){
 const vals=Array.from({length:6},(_,i)=>{const [a,b]=orbit[(j+4*i)%24];return dr(u*a+v*b)});
 const sum=vals.reduce((a,b)=>a+b,0);if(![27,36,45,54].includes(sum))throw Error('obstruction');hist[sum]=(hist[sum]||0)+1;checks++;
 }
 // A scalar affine offset is an exploratory alternative, not canonical authentication.
 const target=[3,6,6,9,9,9].join(',');
 for(let u=0;u<9;u++)for(let v=0;v<9;v++)for(let c=0;c<9;c++)for(let j=0;j<24;j++){
 const vals=Array.from({length:6},(_,i)=>{const [a,b]=orbit[(j+4*i)%24];return dr(u*a+v*b+c)});
 if(vals.slice().sort((a,b)=>a-b).join(',')===target)nonlinear.push({u,v,c,j,vals});
 }
 return {schema:'omega42.eye.obstruction.v1',checks,hist,affineTargetMatches:nonlinear.length,examples:nonlinear.slice(0,6),boundary:'Affine matches are not authenticated Eye operators.'};
}
