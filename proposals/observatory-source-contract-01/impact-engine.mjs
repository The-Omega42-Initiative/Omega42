export function impact(graph,register,id){
 if(graph.source.blob!==register.source.blob)throw Error("source mismatch");
 const records=new Map(register.records.map(r=>[r.id,r]));
 if(!records.has(id))throw Error("unknown record");
 const distance=new Map([[id,0]]),queue=[id];
 for(let i=0;i<queue.length;i++){const p=queue[i];for(const e of graph.edges){if(e.to===p&&!distance.has(e.from)){if(!records.has(e.from))throw Error("unknown dependency");distance.set(e.from,distance.get(p)+1);queue.push(e.from)}}}
 const affected=queue.map(id=>({id,distance:distance.get(id),status:records.get(id).status,certificate:records.get(id).certificate_path}));
 return {schema:"omega42.impact.v1",source:register.source,changed:id,direct:affected.filter(x=>x.distance===1).length,indirect:affected.filter(x=>x.distance>1).length,affected,certificates:[...new Set(affected.map(x=>x.certificate).filter(Boolean))].sort(),verdict:"REVIEW_REQUIRED",mutation:"NONE"};
}
