"use strict";

export const ACTIVATION_PHRASES = ["start omega42 navigator","start omega 42 navigator","welcome navigator"];
export const RUNTIME_STATES = ["IDLE","TRIGGERED","RESOLVING_RELEASE","VERIFYING_RELEASE","INITIALIZING","READY","BLOCKED","FAILED"];
const shaPattern=/^[a-f0-9]{64}$/i;

export function classifyActivation(input) {
  const text=String(input ?? "").trim().toLowerCase().replace(/[.!?]+$/,"").replace(/\s+/g," ");
  if (ACTIVATION_PHRASES.includes(text)) return {kind:"activate",trigger:text};
  if (/\b(prior art|protocol proposal|navigator submission|review this protocol)\b/.test(text)) return {kind:"intake_review",trigger:text};
  return {kind:"ordinary_question",trigger:text};
}

export function validateApprovedRelease(manifest) {
  const errors=[];
  if(!manifest || typeof manifest!=="object" || Array.isArray(manifest)) return {valid:false,errors:["manifest must be an object"]};
  if(manifest.protocol_id!=="Omega42") errors.push("protocol_id must be Omega42");
  if(typeof manifest.release!=="string" || !manifest.release.trim()) errors.push("release is required");
  if(manifest.approval_status!=="approved") errors.push("release is not approved");
  if(!Array.isArray(manifest.documents) || manifest.documents.length===0) errors.push("documents must be a non-empty array");
  for(const [i,d] of (Array.isArray(manifest.documents)?manifest.documents:[]).entries()){
    if(!d || typeof d!=="object") {errors.push("document "+i+" must be an object");continue;}
    if(typeof d.id!=="string" || !d.id.trim()) errors.push("document "+i+" requires id");
    if(typeof d.url!=="string" || !/^https:\/\//.test(d.url)) errors.push("document "+i+" requires HTTPS url");
    if(typeof d.sha256!=="string" || !shaPattern.test(d.sha256)) errors.push("document "+i+" requires SHA-256");
    if(d.required!==true && d.required!==false) errors.push("document "+i+" requires boolean required flag");
  }
  return {valid:errors.length===0,errors};
}

export async function verifyDocumentDigest(content,expectedHex) {
  if(!globalThis.crypto?.subtle) throw new Error("Web Crypto SHA-256 unavailable");
  const bytes=typeof content==="string"?new TextEncoder().encode(content):content;
  const digest=await crypto.subtle.digest("SHA-256",bytes);
  const actual=[...new Uint8Array(digest)].map(x=>x.toString(16).padStart(2,"0")).join("");
  return {valid:actual.toLowerCase()===String(expectedHex).toLowerCase(),actual,expected:String(expectedHex).toLowerCase()};
}

export function createRuntimeSession({sessionId,manifest,model,capabilities=[]}) {
  const validation=validateApprovedRelease(manifest);
  if(!validation.valid) return {state:"BLOCKED",session:null,errors:validation.errors};
  if(typeof sessionId!=="string" || !sessionId.trim()) throw new TypeError("sessionId required");
  if(typeof model!=="string" || !model.trim()) throw new TypeError("model identifier required");
  const required=manifest.documents.filter(d=>d.required).map(d=>d.id);
  return {state:"INITIALIZING",session:{
    sessionId,protocolId:"Omega42",release:manifest.release,manifestDigest:manifest.manifest_sha256 || null,
    documentDigests:Object.fromEntries(manifest.documents.map(d=>[d.id,d.sha256.toLowerCase()])),
    requiredDocuments:required,model,capabilities:[...new Set(capabilities)],
    policy:"release-pinned",executionStatus:"INITIALIZED",createdAt:new Date().toISOString()
  },errors:[]};
}

export function markRuntimeReady(session,verifiedDocumentIds) {
  if(!session || session.policy!=="release-pinned") throw new TypeError("invalid runtime session");
  const verified=new Set(verifiedDocumentIds);
  const missing=session.requiredDocuments.filter(id=>!verified.has(id));
  if(missing.length) return {state:"BLOCKED",session:{...session,executionStatus:"BLOCKED"},errors:["required documents not verified: "+missing.join(", ")]};
  return {state:"READY",session:{...session,executionStatus:"READY",verifiedDocuments:[...verified]} ,errors:[]};
}
