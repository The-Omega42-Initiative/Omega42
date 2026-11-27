/* Independent cross-check of the Research Suite: ChatGPT's kernel (site/assets/research-suite-kernel.js) against Claude's
   reference kernel (site/assets/research-suite-reference.js), with negative controls that must fail (CIVP, proposed).
   Run: node records/osl/suite/crosscheck.js [site/assets]. Exits 0 only with no disagreement. */
const A=require('path').resolve(process.argv[2]||'site/assets');
const C=require(A+'/research-suite-kernel.js'),M=require(A+'/research-suite-reference.js'),K=require(A+'/omega42-kernel.js');let n=0,bad=[];
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
// adaptor composition: both kernels, every triple of lengths 1..30
for(let a=1;a<=30;a++)for(let b=1;b<=30;b++)for(let c=1;c<=30;c++){const x=C.compose(a,b,c),y=M.compose(a,b,c);eq([x.L,x.composite,x.bound,x.withinBound],[y.lipschitz,y.composite,y.bound,true],'compose '+a+','+b+','+c)}
// memory still point: 3^j s and the reduced invariant s/3^k
for(let k=1;k<=6;k++)for(let s=0;s<3**k;s+=Math.max(1,Math.floor(3**k/20)))for(let j=0;j<=5;j++){const x=C.memory(k,0,j,s),y=M.trajectory(0,s,k,j).rows[j];eq([x.stillValue,s?x.stillFraction:'0'],[String(y.still),y.invariant],'still '+k+','+s+','+j)}
// negative controls: each must fail
const neg=[['false closure period 23',C.discover(2,23).closureViolations>0],['seven readings do not separate W_6',!M.partition([0,10,1346,716,147,1005,1218],6).separates],
 ['24 -> 7 is no factor',!C.adaptor(24,7).factor&&M.defect(24,7).defect>0],['AV does not generate W_2',!M.navigate('AV',2).generates],['truncated observer does not attain',!M.adaptive(4,3).attains],
 ['incomplete completion has no mean',M.complete([0,1],2,[2]).mean===null]];
neg.forEach(([w,ok])=>{n++;if(!ok)bad.push('negative control did not fail: '+w)});
const closure=(x,P)=>{let z=x;for(let i=0;i<P;i++)z=K.step(z,9);return z.join()===x.join()};n++;if(!(closure([2,5],24)&&!closure([2,5],23)))bad.push('stepped closure');
console.log('RESEARCH SUITE CROSS-CHECK: '+n+' checks, '+bad.length+' disagreements: '+(bad.length?'FAIL':'PASS'));bad.slice(0,8).forEach(b=>console.log(b));process.exit(bad.length?1:0);
