// Audit envelopes are untrusted self-reports, never canonical verdicts.
export function validateAudit(a, register) {
 const errors=[];
 const fail=(k)=>errors.push(k);
 if(!a || typeof a!=="object" || Array.isArray(a)) return ["object"];
 const keys=["schema","source_blob","revision","record_id","certificate_path","command","environment","execution","output","exit_code","verdict","reason","consent"];
 for(const k of Object.keys(a)) if(!keys.includes(k)) fail("unknown:"+k);
 for(const k of keys) if(!Object.hasOwn(a,k)) fail("missing:"+k);
 if(a.schema!=="omega42.observatory.audit.v1") fail("schema");
 if(a.source_blob!==register.source.blob) fail("source_blob");
 if(typeof a.revision!=="string" || !/^[a-f0-9]{40}$/.test(a.revision)) fail("revision");
 const r=register.records.find(r=>r.id===a.record_id);
 if(!r || a.certificate_path!==r.certificate_path) fail("record/certificate");
 for(const [k,max] of [["command",2000],["environment",2000],["output",50000],["reason",4000]]) if(typeof a[k]!=="string"||a[k].length>max) fail(k);
 if(typeof a.reason==="string"&&!a.reason.trim()) fail("reason");
 if(a.consent!==true) fail("consent");
 if(!["NOT_EXECUTED","SELF_REPORTED_EXECUTION"].includes(a.execution)) fail("execution");
 if(!["ACCEPTED","CORRECTED","DECLINED","INCONCLUSIVE"].includes(a.verdict)) fail("verdict");
 if(a.execution==="NOT_EXECUTED"&&(a.exit_code!==null||a.output!==""||a.verdict!=="INCONCLUSIVE")) fail("unexecuted");
 if(a.execution==="SELF_REPORTED_EXECUTION"){
  if(!Number.isInteger(a.exit_code)||a.exit_code<0||a.exit_code>255) fail("exit_code");
  if(!a.command?.trim?.()||!a.environment?.trim?.()) fail("execution context");
  if(a.verdict==="ACCEPTED"&&(a.exit_code!==0||typeof a.output!=="string"||!r?.expected_marker||!a.output.includes(r.expected_marker))) fail("accepted evidence");
 }
 return errors;
}
