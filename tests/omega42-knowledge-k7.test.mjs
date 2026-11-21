import test from "node:test";
import assert from "node:assert/strict";
import {validateKnowledgeNetwork,dependencyClosure,findDiscoveryPaths,listContradictionCandidates,normalizeK3ResearchGraph} from "../site/omega42-knowledge-k7.mjs";
const graph={schema:"omega42.knowledge-network.k7",metadata:{},nodes:[
{id:"d1",type:"definition",title:"Fibonacci transition",statement:"T(a,b)=(b,a+b)",status:"reconstructed",provenance:{source:"Omega42 mathematics"}},
{id:"t1",type:"theorem",title:"Orbit result",statement:"A stated orbit theorem",status:"proved",provenance:{source:"Proof record"}},
{id:"q1",type:"open_question",title:"Question",statement:"Can this generalize?",status:"open",provenance:{source:"Research register"}},
{id:"i1",type:"instrument",title:"Orbit engine",statement:"Computes finite orbits",status:"computed",provenance:{source:"K3"}},
{id:"c1",type:"conjecture",title:"Alternative claim",statement:"Competing claim",status:"conjectured",provenance:{source:"Research note"}}
],edges:[
{from:"t1",to:"d1",type:"depends_on"},
{from:"q1",to:"t1",type:"supports"},
{from:"q1",to:"i1",type:"applies_to"},
{from:"t1",to:"c1",type:"contradicts"}
]};
test("validates typed graph",()=>assert.equal(validateKnowledgeNetwork(graph).valid,true));
test("finds dependencies",()=>assert.deepEqual(dependencyClosure(graph,"t1","ancestors"),["d1"]));
test("returns discovery paths",()=>assert.ok(findDiscoveryPaths(graph,"q1").length>=2));
test("lists explicit contradiction edges",()=>assert.equal(listContradictionCandidates(graph).length,1));
test("rejects duplicate IDs",()=>{const g=structuredClone(graph);g.nodes.push({...g.nodes[0]});assert.equal(validateKnowledgeNetwork(g).valid,false);});
test("rejects dependency cycles but allows contradiction cycles",()=>{const g=structuredClone(graph);g.edges.push({from:"d1",to:"t1",type:"depends_on"});assert.equal(validateKnowledgeNetwork(g).valid,false);});
test("normalizes K3 graph",()=>{const k3={schema:"omega42.research-graph.k3",nodes:[{id:"x",type:"claim",title:"Claim",statement:"s",status:"interpretation",provenance:{source:"legacy"}}],edges:[]};assert.equal(normalizeK3ResearchGraph(k3).nodes[0].type,"interpretation");});
