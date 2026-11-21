import test from "node:test";
import assert from "node:assert/strict";
import {classifyActivation,validateApprovedRelease,createRuntimeSession,markRuntimeReady} from "../site/omega42-runtime-k8.mjs";
const manifest={protocol_id:"Omega42",release:"V335-Rev450-STABLE",approval_status:"approved",documents:[
{id:"core",url:"https://example.org/core.md",sha256:"a".repeat(64),required:true},
{id:"companion",url:"https://example.org/companion.md",sha256:"b".repeat(64),required:false}
]};
test("recognizes explicit activation phrase",()=>assert.equal(classifyActivation("Start Omega42 Navigator").kind,"activate"));
test("recognizes conversational legacy trigger",()=>assert.equal(classifyActivation("Welcome Navigator").kind,"activate"));
test("keeps prior-art intake separate from activation",()=>assert.equal(classifyActivation("Review this prior art protocol").kind,"intake_review"));
test("ordinary question does not auto-activate",()=>assert.equal(classifyActivation("What is Omega42?").kind,"ordinary_question"));
test("validates approved release manifest",()=>assert.equal(validateApprovedRelease(manifest).valid,true));
test("fails closed for unapproved release",()=>assert.equal(validateApprovedRelease({...manifest,approval_status:"proposal"}).valid,false));
test("blocks malformed digest and non-HTTPS document",()=>assert.equal(validateApprovedRelease({...manifest,documents:[{...manifest.documents[0],url:"http://x",sha256:"bad"}]}).valid,false));
test("pins session to exact release and digests",()=>{const r=createRuntimeSession({sessionId:"s1",manifest,model:"configured-model",capabilities:["web_search"]});assert.equal(r.session.release,manifest.release);assert.equal(r.session.documentDigests.core,"a".repeat(64));});
test("blocks readiness when required documents are not verified",()=>{const s=createRuntimeSession({sessionId:"s1",manifest,model:"m"}).session;assert.equal(markRuntimeReady(s,[]).state,"BLOCKED");});
test("marks ready only after required document verification",()=>{const s=createRuntimeSession({sessionId:"s1",manifest,model:"m"}).session;assert.equal(markRuntimeReady(s,["core"]).state,"READY");});
