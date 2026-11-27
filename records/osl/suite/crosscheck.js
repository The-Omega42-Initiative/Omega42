/* Independent cross-check of the Research Suite kernel (proposal/research-suite-v1) against records/osl/suite/omega42-suite.js.
   Run: node records/osl/suite/crosscheck.js <path to site/assets>. Exits after printing the number of checks and disagreements. */
const C=require(process.argv[2]+'/research-suite-kernel.js'),M=require('./omega42-suite.js'),K=require(process.argv[2]+'/omega42-kernel.js');let n=0,bad=[];
const eq=(a,b,w)=>{n++;if(JSON.stringify(a)!==JSON.stringify(b))bad.push(w+': '+JSON.stringify(a)+' vs '+JSON.stringify(b))};
// memory
for(let k=1;k<=8;k++)for(let w=0;w<3**k;w+=Math.max(1,Math.floor(3**k/40)))for(let j=0;j<=6;j++){const c=C.memory(k,w,j),m=M.trajectory(w,0,k,j).rows[j];eq(c.moving,String(m.moving),'moving '+k+','+w+','+j);eq(c.extinction,M.extinctionDepth(w,k),'ext '+k+','+w)}
// partitions on random teams
let s=1;const rnd=N=>{s=(s*48271)%2147483647;return s%N};
for(let k=2;k<=5;k++)for(let r=0;r<20;r++){const N=8*3**(k-1),T=[0];for(let i=1;i<k+1;i++)T.push(rnd(N));const c=C.partition(k,T),m=M.partition(T,k);eq([c.debt,c.max,c.classes],[m.pairs,m.largest,m.classes],'part '+k+' '+T)}
{const T=[0,10,1346,716,147,1005,1218],c=C.complete(6,T),m=M.complete(T,6,[...Array(1944).keys()]);eq([c.unresolved,Object.keys(c.phases).length,c.meanIfComplete],[m.unresolved,m.distinctPhases,m.mean],'complete6')}
// golden: output with native gains equals A v
for(let i=0;i<200;i++){const x=rnd(2001)/100-10,y=rnd(2001)/100-10,g=C.golden(x,y,(1+Math.sqrt(5))/2,-2/(1+Math.sqrt(5)));n++;if(Math.abs(g.output[0]-y)>1e-9||Math.abs(g.output[1]-x-y)>1e-9)bad.push('golden '+x+','+y)}
// incidence vs certificate
for(let k=1;k<=3;k++){for(let a=0;a<3**k;a++)for(let b=0;b<3**k;b++){if(!a&&!b)continue;const c=C.incidence(k,a,b);n++;if(c.actual!==c.expected)bad.push('inc '+k+' '+a+','+b)};eq(M.verifyDesign(k).pass,true,'design '+k)}
for(let k=1;k<=4;k++)for(let r=0;r<4*3**(k-1);r++){eq(C.schedule(k,r).covered,9**k,'cover');eq(C.schedule(k,r).direction,M.round(k,r).direction,'dir')}
// navigation
for(let k=1;k<=5;k++)for(const o of ['AC','ACS','AVC','AVCS','AS','AV']){const c=C.navigation(k,o,1,1),m=M.navigate(o,k,[1,1]);eq([c.reached,c.eccentricityOfReached,c.targetDistance],[m.reached,m.eccentricity,m.route?m.route.length:-1],'nav '+k+o)}
// discover closure: is it a real test?
const xx=[2,5];let manual=xx;for(let i=0;i<24;i++)manual=K.step(manual,9);
console.log('A^24 by stepping on W_2:',manual,'| kernel power(x,24):',K.power(xx,24,2),'| power(x,25) vs power(x,1):',K.power(xx,25,2),K.power(xx,1,2));
console.log('checks',n,'disagreements',bad.length);bad.slice(0,8).forEach(b=>console.log(b));
