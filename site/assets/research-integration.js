(()=>{"use strict";
const el=id=>document.getElementById(id);
el("ri-observe").addEventListener("click",()=>{
 const raw=el("ri-phases").value.trim();
 if(!/^\d+(\s*,\s*\d+)*$/.test(raw)){el("ri-observation").textContent="Enter comma-separated phases.";return;}
 const p=[...new Set(raw.split(",").map(Number))];
 if(p.some(t=>t<0||t>23)){el("ri-observation").textContent="Phases must be 0–23.";return;}
 const counts=new Map();
 for(let a=0;a<9;a++)for(let b=0;b<9;b++){let x=a,y=b,h=[];for(let t=0;t<24;t++){h.push(x%7);[x,y]=[y,(x+y)%9];}let key=p.map(t=>h[t]).join(",");counts.set(key,(counts.get(key)||0)+1);}
 const collisions=[...counts.values()].reduce((s,n)=>s+n*(n-1)/2,0);
 el("ri-observation").textContent=counts.size+" / 81 distinct signatures; "+collisions+" unresolved pairs.";
});
el("ri-generate").addEventListener("click",()=>{
 const k=Number(el("ri-depth").value),ops=el("ri-ops").value;
 if(![2,3,4,5].includes(k)||!["ACS","AVC","AVCS","A"].includes(ops))return;
 const q=3**k,queue=[[2,5,0]],seen=new Set([2*q+5]);let max=0;
 for(let i=0;i<queue.length;i++){let [a,b,d]=queue[i];for(let op of ops){let [x,y]=op==="A"?[b,(a+b)%q]:op==="V"?[2*a%q,2*b%q]:op==="C"?[3*a%q,3*b%q]:[a,(3*a+b)%q];let key=x*q+y;if(!seen.has(key)){seen.add(key);queue.push([x,y,d+1]);max=Math.max(max,d+1);}}}
 el("ri-generation").textContent=seen.size+" / "+q*q+" reachable states; maximum distance "+max+"; native period "+8*3**(k-1)+"; zero harmonic multiplicity "+(3**k+1)/2+".";
});
})();