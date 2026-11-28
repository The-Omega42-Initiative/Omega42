// Read-only dispatcher; no evaluation or subprocess execution.
export function dispatch(register, contract, operation, args = {}) {
 const reject = error => ({status:"REJECTED",error});
 if(register?.schema !== "omega42.observatory.source.v1" || contract?.schema !== "omega42.observatory.instrument.v1" || register.source?.blob !== contract.source?.blob || !Array.isArray(register.records)) return reject("source contract mismatch");
 if(!args || typeof args !== "object" || Array.isArray(args)) return reject("arguments must be an object");
 if(operation === "INSTRUMENT_DESCRIBE") {
  if(Object.keys(args).length) return reject("unexpected arguments");
  return {status:"READ_ONLY",contract};
 }
 if(!["RECORD_LOOKUP","CERTIFICATE_PLAN"].includes(operation)) return reject("unknown operation");
 if(Object.keys(args).length!==1 || typeof args.id!=="string" || !/^MF-[0-9]{2,3}$/.test(args.id)) return reject("expected one MF identifier");
 const record=register.records.find(r=>r.id===args.id);
 if(!record) return reject("record not found");
 const provenance={source:register.source,register_blob:contract.register_blob,integrity:"DECLARED_NOT_HASH_VERIFIED"};
 if(operation==="RECORD_LOOKUP") return {status:"READ_ONLY",provenance,record,certificate_execution:"NOT_EXECUTED"};
 return {status:"PLAN_ONLY",provenance,id:record.id,certificate_path:record.certificate_path,expected_marker:record.expected_marker,boundary:record.boundary,dependencies:record.dependencies,execution:"NOT_EXECUTED",revision_required:true};
}
