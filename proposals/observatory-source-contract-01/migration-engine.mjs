import {impact} from './impact-engine.mjs';
export function migrationPlan(graph,register,claims){
 if(!Array.isArray(claims))throw Error('claims must be an array');
 const allowed=new Set(['RECOVERED','PRESERVED','EXTENDED','REPLACED','UNRESOLVED','INCOMPATIBLE']);
 const ids=new Set(register.records.map(r=>r.id)), byId=new Map();
 for(const c of claims){
  if(!c||!ids.has(c.id)||byId.has(c.id)||!allowed.has(c.classification)||typeof c.evidence!=='string'||!c.evidence.trim())throw Error('invalid claim');
  byId.set(c.id,c);
 }
 const rows=register.records.map(r=>({id:r.id,inherited_status:r.status,classification:byId.get(r.id)?.classification??'UNRESOLVED',evidence:byId.get(r.id)?.evidence??null,review:'NOT_ADJUDICATED'}));
 const review=new Set(),certificates=new Set();
 for(const c of claims){const p=impact(graph,register,c.id);for(const x of p.affected)review.add(x.id);for(const x of p.certificates)certificates.add(x)}
 return {schema:'omega42.migration.v1',source:register.source,rows,review_records:[...review].sort(),certificate_paths:[...certificates].sort(),approval:'NOT_GRANTED',mutation:'NONE'};
}
