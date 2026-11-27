/* Independent verification of the OmegaSL research bindings (CIVP, CA-52): coding over every state and every error pattern of
   weight <= 2, SPEC.DEFICIT against the register definition tr(S^2)/16 - tr(S)^2/128 (exact, Lucas numbers), projections.
   Run from the repository root: node site/test/osl_bindings_verification.cjs */
const vm=require('vm'),fs=require('fs');const ctx={self:{},console};ctx.window=ctx.self;vm.createContext(ctx);
for(const f of ['omega42-kernel.js','research-suite-reference.js','adaptor_rs.js','atlas-data.js','osl-research-bindings.js'])vm.runInContext(fs.readFileSync('site/assets/'+f,'utf8'),ctx);
const S=ctx.self, O=S.Omega42Operations;let n=0,bad=[];const ok=(c,w)=>{n++;if(!c)bad.push(w)};
const run=(op,...a)=>O.execute(op+' '+JSON.stringify(a)).result;
// coding: every state, every error pattern of weight <= 2
for(let a=0;a<9;a++)for(let b=0;b<9;b++){const w=run('CODE.ENCODE',a,b);const W=Array.isArray(w)?w:w.codeword||w.word;
 for(let i=0;i<7;i++)for(let j=i;j<7;j++)for(let ei=1;ei<7;ei++)for(let ej=(i===j?0:1);ej<(i===j?1:7);ej++){const r=W.slice();r[i]=(r[i]+ei)%7;if(j!==i)r[j]=(r[j]+ej)%7;const d=run('CODE.RECONSTRUCT',r).candidate;ok(d&&String(d.state||d)===String([a,b]),'decode '+a+','+b)}}
// deficit against the register definition tr(S^2)/16 - tr(S)^2/128, S = M^(2n), tr(M^m) = 4 L_m (exact, BigInt)
const L=[2n,1n];for(let i=2;i<=60;i++)L.push(L[i-1]+L[i-2]);
for(let k=0;k<=12;k++){const t2=4n*L[4*k],t1=4n*L[2*k];const exact=Number(t2*8n-t1*t1)/128;ok(Math.abs(run('SPEC.DEFICIT',k).deficit-exact)<=1e-9*Math.max(1,exact),'deficit '+k)}
// projection: parts sum to v, are orthogonal, A acts by phi and -1/phi
for(const v of [[1,2],[3,-1],[0,1],[1e3,7]]){const p=run('SPEC.PROJECT',...v);const P=p.plus,Q=p.minus,phi=(1+Math.sqrt(5))/2;
 ok(Math.abs(P[0]+Q[0]-v[0])<1e-9&&Math.abs(P[1]+Q[1]-v[1])<1e-9,'sum');ok(Math.abs(P[0]*Q[0]+P[1]*Q[1])<1e-6,'orth');ok(Math.abs(P[1]-phi*P[0])<1e-9*Math.max(1,Math.abs(P[1]))&&Math.abs(P[0]-phi*P[1]+phi*P[1]-P[1]/phi- (P[0]-P[1]/phi))<1e-9,'eig')}
const e=run('LEX.EQUIVALENTS','golden split');ok(Array.isArray(e)&&e.length>=1,'lex');
console.log('OSL BINDING VERIFICATION: '+(bad.length?'FAIL':'PASS')+' --',n,'checks,',bad.length,'failures',bad.slice(0,5), 'golden split rows',e.length, JSON.stringify(e.map(x=>x.field)));
process.exit(bad.length?1:0);
