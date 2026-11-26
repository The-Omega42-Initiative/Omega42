// Standalone exact integer audit; no dependencies.
const X=Array.from({length:81},(_,i)=>[Math.floor(i/9),i%9]);
const id=([a,b])=>9*a+b;
const A=([a,b])=>[b,(a+b)%9];
const perm=X.map(x=>id(A(x)));
const pow=(i,t)=>{while(t--)i=perm[i];return i};
const neg=i=>id(X[i].map(x=>(9-x)%9));
const C=i=>id(X[i].map(x=>3*x%9));
const assert=(b,m)=>{if(!b)throw Error(m)};
let counts={};for(let i=0;i<81;i++){let l=1;while(pow(i,l)!==i)l++;counts[l]=(counts[l]||0)+1;assert(pow(i,12)===neg(i),'antipode');assert(C(perm[i])===perm[C(i)],'compression commutes');assert(C(C(i))===0,'nilpotence')}
assert(JSON.stringify(counts)===JSON.stringify({1:1,8:8,24:72}),'census');
// Integer numerator of orbit-average projector: 24 P0.
const B=Array.from({length:81},(_,i)=>Array.from({length:81},(_,j)=>Array.from({length:24},(_,t)=>pow(i,t)).filter(k=>k===j).length));
let trace=0;for(let i=0;i<81;i++){trace+=B[i][i];for(let j=0;j<81;j++){assert(B[i][j]===B[j][i],'symmetry');assert(B[i].reduce((s,v,k)=>s+v*B[k][j],0)===24*B[i][j],'projector');assert(B[perm[i]][j]===B[i][j],'invariance')}}
assert(trace===120,'rank five');
const fibers=Array(81).fill(0);for(let i=0;i<81;i++)fibers[C(i)]++;
assert(fibers.filter(x=>x===9).length===9,'nine fibers');
const result={counts,projectorRank:trace/24,projectorEntriesChecked:6561,compressionFibers:fibers.filter(Boolean),stateChecks:81,compressionSquared:'zero'};
console.log(JSON.stringify(result,null,2));
