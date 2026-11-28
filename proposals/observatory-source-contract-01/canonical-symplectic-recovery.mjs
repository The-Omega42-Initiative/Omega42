export function canonicalSymplecticRecovery(){
const S=[0,1,2,4,5,7,8,10,11],families=[[2,12],[3,24],[4,16]],basis=[];for(let c=0;c<3;c++)for(const r of S)for(const s of S)basis.push({c,r,s,k:(r-s+12)%12});
const cols=families.flatMap(([k,n])=>basis.map((v,i)=>({...v,i})).filter(v=>v.k===k).slice(0,n));
const mul=(a,b)=>a.map(r=>b[0].map((_,j)=>r.reduce((s,x,k)=>s+x*b[k][j],0))),tr=a=>a[0].map((_,i)=>a.map(r=>r[i])),err=(a,b)=>Math.max(...a.flatMap((r,i)=>r.map((x,j)=>Math.abs(x-b[i][j]))));
const O=[[0,1],[-1,0]],results=[];for(let j=1;j<=3;j++){const t=Math.acos(1-j/2),c=Math.cos(t),s=Math.sin(t),d=Math.sqrt(s),U=[[0,1],[-1,2-j]],L=[[-c/d,1/d],[d,0]],R=[[c,-s],[s,c]],G=[[1/s,-c/s],[-c/s,1/s]],K=G.map(r=>r.map(x=>t*x)),A=mul(O,K);
const errors={symplectic:err(mul(mul(tr(U),O),U),O),normalization:err(mul(mul(tr(L),O),L),O.map(r=>r.map(x=>-x))),intertwining:err(mul(L,U),mul(R,L)),metric:err(mul(tr(L),L),G),generator:err(A,U.map((r,i)=>r.map((x,k)=>t/s*(x-c*+(i===k)))))};if(Math.max(...Object.values(errors))>1e-12)throw Error('audit');results.push({j,theta:t,errors});}
if(new Set(cols.map(v=>v.i)).size!==52)throw Error('rank');
return {schema:'omega42.canonical.symplectic.v1',results,rank:52,realDimension:104,columns:cols,boundary:'Canonical pair convention dx wedge dy; target negative imaginary form; abstract spectral embedding, no physical Hamiltonian derivation.'};
}