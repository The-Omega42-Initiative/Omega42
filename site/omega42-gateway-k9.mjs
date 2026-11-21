"use strict";

export const GATEWAY_VERSION = "k9";
export const GATEWAY_LIMITS = Object.freeze({maxCallsPerSession:24,maxInputBytes:32768,maxOutputBytes:128000,defaultTimeoutMs:12000,maxTimeoutMs:30000});
const READ="read", WRITE="write";
const DEFINITIONS=[
{name:"get_approved_release",description:"Return approved Ω42 release metadata.",sideEffect:READ,required:["releaseChannel"],schema:{type:"object",additionalProperties:false,properties:{releaseChannel:{type:"string",enum:["stable"]}},required:["releaseChannel"]}},
{name:"get_protocol_module",description:"Retrieve one allow-listed module from the pinned approved release.",sideEffect:READ,required:["moduleId","release"],schema:{type:"object",additionalProperties:false,properties:{moduleId:{type:"string",minLength:1,maxLength:80},release:{type:"string",minLength:1,maxLength:80}},required:["moduleId","release"]}},
{name:"search_omega42_knowledge",description:"Search the Ω42 knowledge network by terms, status and node type.",sideEffect:READ,required:["query"],schema:{type:"object",additionalProperties:false,properties:{query:{type:"string",minLength:2,maxLength:500},statuses:{type:"array",items:{type:"string"},maxItems:8},types:{type:"array",items:{type:"string"},maxItems:8},limit:{type:"integer",minimum:1,maximum:20}},required:["query"]}},
{name:"run_omega42_instrument",description:"Run one named deterministic Ω42 instrument with bounded input.",sideEffect:READ,required:["task","input"],schema:{type:"object",additionalProperties:false,properties:{task:{type:"string",enum:["orbit","census","uniqueness","temporal","omegasl","researchGraph"]},input:{type:"object"}},required:["task","input"]}},
{name:"search_external_sources",description:"Search external sources through a host-configured search adapter; results are untrusted evidence.",sideEffect:READ,required:["query"],schema:{type:"object",additionalProperties:false,properties:{query:{type:"string",minLength:2,maxLength:500},domains:{type:"array",items:{type:"string"},maxItems:10},recencyDays:{type:"integer",minimum:0,maximum:3650}},required:["query"]}},
{name:"retrieve_source_document",description:"Retrieve a document from an allow-listed HTTPS source; content remains untrusted.",sideEffect:READ,required:["url"],schema:{type:"object",additionalProperties:false,properties:{url:{type:"string",format:"uri",maxLength:2048}},required:["url"]}},
{name:"create_research_record",description:"Create a research record in an authorized workspace. Requires host-issued approval.",sideEffect:WRITE,required:["record"],schema:{type:"object",additionalProperties:false,properties:{record:{type:"object"}},required:["record"]}},
{name:"propose_protocol_change",description:"Submit a protocol-change proposal for human review; does not alter the approved protocol. Requires host-issued approval.",sideEffect:WRITE,required:["proposal"],schema:{type:"object",additionalProperties:false,properties:{proposal:{type:"object"}},required:["proposal"]}}
];
const ADAPTERS={get_approved_release:"getApprovedRelease",get_protocol_module:"getProtocolModule",search_omega42_knowledge:"searchOmega42Knowledge",run_omega42_instrument:"runOmega42Instrument",search_external_sources:"searchExternalSources",retrieve_source_document:"retrieveSourceDocument",create_research_record:"createResearchRecord",propose_protocol_change:"proposeProtocolChange"};
const plain=o=>o!==null&&typeof o==="object"&&!Array.isArray(o);
const bytes=o=>new TextEncoder().encode(JSON.stringify(o)).length;
function validateArgs(def,args){
 const errors=[];
 if(!plain(args))return ["arguments must be a JSON object"];
 for(const k of Object.keys(args))if(!Object.hasOwn(def.schema.properties,k))errors.push("unknown argument: "+k);
 for(const k of def.required)if(!Object.hasOwn(args,k))errors.push("missing required argument: "+k);
 for(const [k,v] of Object.entries(args)){
  const r=def.schema.properties[k];if(!r)continue;
  if(r.type==="string"&&(typeof v!=="string"||v.length<(r.minLength||0)||v.length>(r.maxLength||Infinity)))errors.push(k+" must be a string within its length bounds");
  if(r.type==="integer"&&(!Number.isInteger(v)||v<r.minimum||v>r.maximum))errors.push(k+" must be an integer in range");
  if(r.type==="object"&&!plain(v))errors.push(k+" must be an object");
  if(r.type==="array"&&(!Array.isArray(v)||v.length>r.maxItems||v.some(x=>typeof x!=="string")))errors.push(k+" must be a bounded string array");
  if(r.enum&&!r.enum.includes(v))errors.push(k+" is not an allowed value");
  if(k==="url"&&typeof v==="string"){try{if(new URL(v).protocol!=="https:")errors.push("url must use HTTPS");}catch{errors.push("url must be a valid HTTPS URL");}}
 }
 return errors;
}
function withTimeout(promise,ms,controller){let timer;return Promise.race([Promise.resolve(promise),new Promise((_,reject)=>{timer=setTimeout(()=>{controller.abort();reject(new Error("tool timed out; adapter cancellation requested"));},ms);})]).finally(()=>clearTimeout(timer));}
export function listGatewayTools({includeWrites=false}={}){return DEFINITIONS.filter(d=>includeWrites||d.sideEffect===READ).map(d=>({type:"function",name:d.name,description:d.description,parameters:d.schema,strict:true}));}
export function createOmega42Gateway({adapters={},authorizeWrite=async()=>false,limits={},clock=()=>Date.now()}={}){
 const budget={...GATEWAY_LIMITS,...limits},counters=new Map();
 async function invoke(name,args,context={}){
  const def=DEFINITIONS.find(d=>d.name===name);
  if(!def)return {ok:false,status:"DENIED",error:"tool is not on the Ω42 allow-list"};
  if(context.authenticated!==true)return {ok:false,status:"DENIED",error:"authenticated runtime principal required"};
  if(bytes(args)>budget.maxInputBytes)return {ok:false,status:"DENIED",error:"tool input exceeds size limit"};
  const errors=validateArgs(def,args);if(errors.length)return {ok:false,status:"INVALID_INPUT",errors};
  const sessionId=String(context.sessionId||"");if(!sessionId)return {ok:false,status:"DENIED",error:"runtime session required"};
  if(name!=="get_approved_release"&&!(typeof context.pinnedRelease==="string"&&context.pinnedRelease.trim()))return {ok:false,status:"DENIED",error:"release-pinned session required"};
  const count=counters.get(sessionId)||0;if(count>=budget.maxCallsPerSession)return {ok:false,status:"BUDGET_EXHAUSTED",error:"session tool-call budget exhausted"};
  if(def.sideEffect===WRITE){
   const approved=await authorizeWrite({tool:name,args,approvalToken:context.approvalToken||null,principal:context.principal||null,sessionId});
   if(approved!==true)return {ok:false,status:"APPROVAL_REQUIRED",error:"valid host-issued approval required"};
  }
  const adapter=adapters[ADAPTERS[name]];
  if(typeof adapter!=="function")return {ok:false,status:"UNAVAILABLE",error:"configured adapter is unavailable"};
  counters.set(sessionId,count+1);
  const timeoutMs=Math.min(Math.max(Number(context.timeoutMs)||budget.defaultTimeoutMs,100),budget.maxTimeoutMs);
  try{
   const controller=new AbortController();
   const result=await withTimeout(adapter(args,{sessionId,principal:context.principal||null,release:context.pinnedRelease||null,trustBoundary:"UNTRUSTED_TOOL_RESULT",signal:controller.signal}),timeoutMs,controller);
   if(bytes(result)>budget.maxOutputBytes)return {ok:false,status:"OUTPUT_LIMIT",error:"tool output exceeds size limit"};
   return {ok:true,status:"EXECUTED",tool:name,sideEffect:def.sideEffect,trust:"UNTRUSTED_RESULT",result,remainingCalls:budget.maxCallsPerSession-count-1,timestamp:new Date(clock()).toISOString()};
  }catch(error){return {ok:false,status:"FAILED",tool:name,error:String(error?.message||error)};}
 }
 return Object.freeze({listTools:options=>listGatewayTools(options),invoke,usage:id=>({used:counters.get(String(id))||0,limit:budget.maxCallsPerSession})});
}
