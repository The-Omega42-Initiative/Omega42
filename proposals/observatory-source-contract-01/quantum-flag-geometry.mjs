export function flagGeometry(){
const S=[0,1,2,4,5,7,8,10,11],target=[0,0,12,24,16,0,0],rows=[],bad=[];
for(let i=0;i<9;i++)for(let j=i+1;j<9;j++){const d=Math.min(S[j]-S[i],12-S[j]+S[i]);if(!target[d])bad.push([S[i],S[j]])}
function visit(a,max){if(a.length===9){const h=Array(7).fill(0);for(let i=0;i<9;i++)for(let j=i+1;j<9;j++)if(a[i]!==a[j])h[Math.min(S[j]-S[i],12-S[j]+S[i])]++;rows.push({a,h,n:h.reduce((s,x)=>s+x,0)});return}for(let k=0;k<=max+1;k++)visit([...a,k],Math.max(max,k))}
visit([0],0);
const clean=rows.filter(r=>r.h[1]+r.h[5]+r.h[6]===0);
const hist=new Map();for(const r of rows){const key=r.h.join(',');if(!hist.has(key))hist.set(key,r)}
const adj=new Map(S.map(x=>[x,[]]));for(const [a,b] of bad){adj.get(a).push(b);adj.get(b).push(a)}const reached=[S[0]];for(let i=0;i<reached.length;i++)for(const v of adj.get(reached[i]))if(!reached.includes(v))reached.push(v);
if(rows.length!==21147||clean.length!==1||reached.length!==9)throw Error('audit');
return {schema:'omega42.flag.geometry.v1',partitions:rows.length,distinctHistograms:hist.size,forbiddenEdges:bad,connected:reached,clean:clean.length,cleanDimensions:clean.map(r=>2*r.n),exactTriplePossible:false,boundary:'All invariant unitary orbits with componentwise inherited evolution; real unoriented spectra; conditional on inherited quantum eigenphases.'};
}