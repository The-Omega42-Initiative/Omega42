export function apertureCorrespondence(){
const mod=(x,n)=>(x%n+n)%n;
const vertices=[];for(let s=0;s<6;s++){vertices.push({s,r:0,side:0,j:0});for(let r=1;r<=3;r++)for(const side of [1,-1])vertices.push({s,r,side,j:mod(side*r,7)});}
const key=(s,j)=>s+','+j;
const map=new Map(vertices.map(v=>[key(v.s,v.j),v]));
if(map.size!==42)throw Error('bijection');
const F=v=>map.get(key((v.s+1)%6,3*v.j%7));
const S=v=>map.get(key((v.s+1)%6,v.j));
const R=v=>map.get(key(v.s,mod(-v.j,7)));
const census=f=>{const seen=new Set(),h={};for(const v of vertices){if(seen.has(v))continue;let x=v,n=0;do{seen.add(x);x=f(x);n++}while(x!==v);h[n]=(h[n]||0)+1}return h};
const twisted=v=>mod(v.j*([1,5,4,6,2,3][v.s]),7);
for(const v of vertices){if(twisted(F(v))!==twisted(v)||R(F(v))!==F(R(v)))throw Error('equivariance');}
return {schema:'omega42.aperture.correspondence.v1',vertices:vertices.length,eyeCount:vertices.filter(v=>v.j===0).length,sectorShift:census(S),frobeniusTransport:census(F),reflection:census(R),checks:84,boundary:'Labels j=side*r are chosen; no canonical field generator or graph-edge correspondence established.'};
}