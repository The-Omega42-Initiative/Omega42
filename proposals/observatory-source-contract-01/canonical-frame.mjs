export function frameRecovery(){
 const mod=x=>(x%9+9)%9, step=([a,b])=>[b,mod(a+b)], norm=([a,b])=>mod(a*a+a*b-b*b), key=x=>x.join(',');
 const units=[];for(let r=0;r<9;r++)for(let s=0;s<9;s++)if(mod(r*r+r*s-s*s)%3!==0)units.push([r,s]);
 const act=([r,s],[a,b])=>[mod(r*a+s*b),mod(s*a+(r+s)*b)];
 const seed=[2,5], images=new Set(units.map(u=>key(act(u,seed))));
 const orbit=[];let x=seed;do{orbit.push(x);x=step(x)}while(key(x)!==key(seed));
 const preserving=units.filter(u=>mod(norm(u)**2)===1);
 const detOne=units.filter(u=>norm(u)===1);
 const shifts=orbit.map((_,j)=>{const eyes=Array.from({length:6},(_,i)=>orbit[(j+2+4*i)%24][0]||9);return {shift:j,eyes,sum:eyes.reduce((a,b)=>a+b,0)}});
 const reciprocal=Array.from({length:8},(_,i)=>i+1).filter(a=>new Set(Array.from({length:6},(_,k)=>mod(a**k))).size===6);
 if(units.length!==72||images.size!==72||orbit.length!==24||preserving.length!==24||detOne.length!==12||key(reciprocal)!=='2,5')throw Error('audit');
 return {schema:'omega42.frame.recovery.v1',centralizerOrder:units.length,seedImages:images.size,normSquaredPreservers:preserving.length,detOne:detOne.length,orbit,shifts,reciprocal,aperture:4};
}
