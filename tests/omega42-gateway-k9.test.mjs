import test from "node:test";
import assert from "node:assert/strict";
import {createOmega42Gateway,listGatewayTools} from "../site/omega42-gateway-k9.mjs";
const adapters={
 getApprovedRelease:async()=>({release:"test-1"}),
 getProtocolModule:async a=>({moduleId:a.moduleId,release:a.release}),
 searchOmega42Knowledge:async a=>({query:a.query,nodes:[]}),
 runOmega42Instrument:async a=>({task:a.task,executionStatus:"EXECUTED"}),
 searchExternalSources:async a=>({results:[],query:a.query}),
 retrieveSourceDocument:async a=>({url:a.url,text:"untrusted"}),
 createResearchRecord:async()=>({created:true,id:"r1"}),
 proposeProtocolChange:async()=>({submitted:true,id:"p1"})
};
const ctx={authenticated:true,sessionId:"s1",pinnedRelease:"r1"};
test("default listing exposes read-only tools only",()=>{assert.equal(listGatewayTools().length,6);assert.equal(listGatewayTools({includeWrites:true}).length,8);});
test("unauthenticated calls are denied",async()=>{const g=createOmega42Gateway({adapters});assert.equal((await g.invoke("get_approved_release",{releaseChannel:"stable"},{})).status,"DENIED");});
test("unknown tools are denied",async()=>{const g=createOmega42Gateway({adapters});assert.equal((await g.invoke("shell_exec",{},ctx)).status,"DENIED");});
test("extra arguments and unsafe URLs are rejected",async()=>{const g=createOmega42Gateway({adapters});assert.equal((await g.invoke("get_approved_release",{releaseChannel:"stable",extra:1},ctx)).status,"INVALID_INPUT");assert.equal((await g.invoke("retrieve_source_document",{url:"http://example.org"},ctx)).status,"INVALID_INPUT");});
test("read results are explicitly untrusted",async()=>{const g=createOmega42Gateway({adapters});const r=await g.invoke("get_approved_release",{releaseChannel:"stable"},ctx);assert.equal(r.status,"EXECUTED");assert.equal(r.trust,"UNTRUSTED_RESULT");});
test("write operations fail closed without host approval",async()=>{const g=createOmega42Gateway({adapters});assert.equal((await g.invoke("propose_protocol_change",{proposal:{title:"x"}},ctx)).status,"APPROVAL_REQUIRED");});
test("write operations require host authorizer approval",async()=>{const g=createOmega42Gateway({adapters,authorizeWrite:async x=>x.approvalToken==="host-signed"});assert.equal((await g.invoke("propose_protocol_change",{proposal:{title:"x"}},{...ctx,approvalToken:"host-signed"})).status,"EXECUTED");});
test("per-session call budget is enforced",async()=>{const g=createOmega42Gateway({adapters,limits:{maxCallsPerSession:1}});assert.equal((await g.invoke("get_approved_release",{releaseChannel:"stable"},ctx)).status,"EXECUTED");assert.equal((await g.invoke("get_approved_release",{releaseChannel:"stable"},ctx)).status,"BUDGET_EXHAUSTED");});
test("missing adapter is unavailable",async()=>{const g=createOmega42Gateway();assert.equal((await g.invoke("get_approved_release",{releaseChannel:"stable"},ctx)).status,"UNAVAILABLE");});
test("timeouts are bounded",async()=>{const a={...adapters,getApprovedRelease:()=>new Promise(r=>setTimeout(()=>r({}),200))};const g=createOmega42Gateway({adapters:a,limits:{defaultTimeoutMs:100,maxTimeoutMs:100}});assert.equal((await g.invoke("get_approved_release",{releaseChannel:"stable"},{...ctx,timeoutMs:100})).status,"FAILED");});
test("input and output size budgets are enforced",async()=>{const a={...adapters,searchOmega42Knowledge:async()=>({data:"x".repeat(1000)})};const g=createOmega42Gateway({adapters:a,limits:{maxOutputBytes:100}});assert.equal((await g.invoke("search_omega42_knowledge",{query:"x".repeat(600)},ctx)).status,"INVALID_INPUT");assert.equal((await g.invoke("search_omega42_knowledge",{query:"valid query"},ctx)).status,"OUTPUT_LIMIT");});

test("pinned release is required for all operations except release resolution",async()=>{const g=createOmega42Gateway({adapters});assert.equal((await g.invoke("get_protocol_module",{moduleId:"core",release:"r1"},{authenticated:true,sessionId:"s2"})).status,"DENIED");});
