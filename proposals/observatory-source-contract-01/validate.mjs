// Node.js 18+. Usage: node validate.mjs canonical.json register.json
import {readFileSync} from 'node:fs';
import {createHash} from 'node:crypto';
const validate = (canonical,contract,sha)=>{const errors=[];const map={id:"id",status:"status",statement:"statement",domain:"domain",certificate_path:"tool",expected_marker:"check",boundary:"does_not_follow",dependencies:"depends"};if(contract.schema!=="omega42.observatory.source.v1"||contract.source?.path!=="records/math/results.json"||contract.source?.blob!==sha)errors.push("source");if(contract.execution!=="NOT_EXECUTED")errors.push("execution");const m=new Map(canonical.results.map(r=>[r.id,r]));const seen=new Set();for(const r of contract.records){if(seen.has(r.id)||!m.has(r.id))errors.push("id:"+r.id);seen.add(r.id);for(const [x,y] of Object.entries(map))if(!Object.hasOwn(r,x)||r[x]!==m.get(r.id)?.[y])errors.push(r.id+":"+x);if(r.execution!=="NOT_EXECUTED")errors.push(r.id+":execution");}if(seen.size!==m.size||m.size!==canonical.results.length)errors.push("coverage");return errors;};
const [source,contract]=process.argv.slice(2);
if(!source||!contract) throw new Error('Provide canonical and contract paths');
const bytes=readFileSync(source);
const sha=createHash('sha1').update('blob '+bytes.length+'\0').update(bytes).digest('hex');
const errors=validate(JSON.parse(bytes),JSON.parse(readFileSync(contract,'utf8')),sha);
if(errors.length){console.error(errors.join('\n'));process.exitCode=1;}else console.log('PASS: source provenance, coverage and inherited fields; certificates NOT_EXECUTED');
