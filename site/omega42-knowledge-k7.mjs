"use strict";

const NODE_TYPES = new Set(["definition","axiom","lemma","theorem","computation","instrument","interpretation","application","open_question","conjecture","source"]);
const STATUSES = new Set(["proved","computed","reconstructed","source_reported","conjectured","speculative","disputed","open","provisional"]);
const EDGE_TYPES = new Set(["depends_on","derives_from","proves","computed_by","supports","contradicts","applies_to","refines","challenges"]);
const ACYCLIC = new Set(["depends_on","derives_from","proves"]);

export function validateKnowledgeNetwork(graph) {
  const errors = [];
  if (!graph || typeof graph !== "object" || Array.isArray(graph)) return { valid:false, errors:["graph must be an object"] };
  if (graph.schema !== "omega42.knowledge-network.k7") errors.push("unsupported schema");
  if (!Array.isArray(graph.nodes)) errors.push("nodes must be an array");
  if (!Array.isArray(graph.edges)) errors.push("edges must be an array");
  const nodes = Array.isArray(graph.nodes) ? graph.nodes : [];
  const edges = Array.isArray(graph.edges) ? graph.edges : [];
  const ids = new Set();
  for (const [i,n] of nodes.entries()) {
    if (!n || typeof n !== "object" || Array.isArray(n)) { errors.push("node "+i+" must be an object"); continue; }
    if (typeof n.id !== "string" || !n.id.trim()) errors.push("node "+i+" requires id");
    else if (ids.has(n.id)) errors.push("duplicate node id: "+n.id); else ids.add(n.id);
    if (!NODE_TYPES.has(n.type)) errors.push("node "+i+" has invalid type");
    if (!STATUSES.has(n.status)) errors.push("node "+i+" has invalid status");
    if (typeof n.title !== "string" || !n.title.trim()) errors.push("node "+i+" requires title");
    if (typeof n.statement !== "string") errors.push("node "+i+" requires statement");
    if (!n.provenance || typeof n.provenance !== "object" || Array.isArray(n.provenance) || typeof n.provenance.source !== "string" || !n.provenance.source.trim()) errors.push("node "+i+" requires provenance.source");
  }
  const adjacency = new Map([...ids].map(id=>[id,[]]));
  for (const [i,e] of edges.entries()) {
    if (!e || typeof e !== "object" || Array.isArray(e)) { errors.push("edge "+i+" must be an object"); continue; }
    if (!ids.has(e.from)) errors.push("edge "+i+" has unknown from endpoint");
    if (!ids.has(e.to)) errors.push("edge "+i+" has unknown to endpoint");
    if (!EDGE_TYPES.has(e.type)) errors.push("edge "+i+" has invalid type");
    if (ACYCLIC.has(e.type) && ids.has(e.from) && ids.has(e.to)) adjacency.get(e.from).push(e.to);
  }
  const color = new Map();
  function visit(id) {
    color.set(id,1);
    for (const next of adjacency.get(id) || []) {
      if (color.get(next)===1) return true;
      if (!color.has(next) && visit(next)) return true;
    }
    color.set(id,2); return false;
  }
  let cycle=false;
  for (const id of ids) if (!color.has(id) && visit(id)) { cycle=true; break; }
  if (cycle) errors.push("dependency/proof relations contain a directed cycle");
  return { schema:"omega42.knowledge-network-validation.k7", valid:errors.length===0, nodeCount:nodes.length, edgeCount:edges.length, errors };
}

export function normalizeK3ResearchGraph(graph) {
  if (!graph || graph.schema!=="omega42.research-graph.k3" || !Array.isArray(graph.nodes) || !Array.isArray(graph.edges)) throw new TypeError("expected omega42.research-graph.k3");
  const mapType = {claim:"interpretation",derivation:"lemma",test:"computation",dataset:"source",decision:"interpretation"};
  const mapStatus = {"deduced":"reconstructed","source-reported":"source_reported","conjecture":"conjectured","interpretation":"speculative","rejected":"disputed","superseded":"disputed"};
  const nodes = graph.nodes.map(n=>({
    id:n.id, type:mapType[n.type] || n.type, title:n.title, statement:n.statement || "",
    status:mapStatus[n.status] || n.status,
    provenance:{source:n.provenance?.source || "K3 imported record", section:n.provenance?.section || "", commit:n.provenance?.commit || ""}
  }));
  const edgeMap = {implements:"computed_by",tests:"supports",derived_from:"derives_from",supports:"supports",depends_on:"depends_on",contradicts:"contradicts",refines:"refines",supersedes:"challenges",interprets:"supports"};
  const edges = graph.edges.map(e=>({from:e.from,to:e.to,type:edgeMap[e.type] || "supports",note:e.note || "Normalized from K3 research graph"}));
  return {schema:"omega42.knowledge-network.k7",metadata:{importedFrom:"omega42.research-graph.k3"},nodes,edges};
}

export function dependencyClosure(graph, nodeId, direction="ancestors") {
  const check=validateKnowledgeNetwork(graph);
  if (!check.valid) throw new TypeError("invalid knowledge network: "+check.errors.join("; "));
  if (!graph.nodes.some(n=>n.id===nodeId)) throw new RangeError("unknown node id");
  if (!["ancestors","descendants"].includes(direction)) throw new RangeError("direction must be ancestors or descendants");
  const relation = direction==="ancestors" ? new Set(["depends_on","derives_from","proves"]) : new Set(["depends_on","derives_from","proves"]);
  const found=new Set(), queue=[nodeId];
  while(queue.length) {
    const current=queue.shift();
    for(const e of graph.edges) {
      const match=direction==="ancestors" ? e.from===current && relation.has(e.type) : e.to===current && relation.has(e.type);
      if(!match) continue;
      const next=direction==="ancestors" ? e.to : e.from;
      if(!found.has(next) && next!==nodeId) {found.add(next);queue.push(next);}
    }
  }
  return [...found];
}

export function findDiscoveryPaths(graph, openQuestionId, {maxPaths=20}={}) {
  const check=validateKnowledgeNetwork(graph);
  if(!check.valid) throw new TypeError("invalid knowledge network: "+check.errors.join("; "));
  const q=graph.nodes.find(n=>n.id===openQuestionId);
  if(!q || q.type!=="open_question") throw new TypeError("target must be an open_question node");
  const undirected=new Map(graph.nodes.map(n=>[n.id,[]]));
  for(const e of graph.edges) {
    if(["supports","applies_to","computed_by","refines","challenges","contradicts"].includes(e.type)) {
      undirected.get(e.from).push(e.to); undirected.get(e.to).push(e.from);
    }
    if(["depends_on","derives_from","proves"].includes(e.type)) {
      undirected.get(e.from).push(e.to); undirected.get(e.to).push(e.from);
    }
  }
  const paths=[], queue=[[openQuestionId]];
  while(queue.length && paths.length<maxPaths) {
    const path=queue.shift(), last=path[path.length-1];
    for(const next of undirected.get(last)||[]) {
      if(path.includes(next)) continue;
      const nextPath=[...path,next], node=graph.nodes.find(n=>n.id===next);
      if(node && ["theorem","lemma","computation","instrument","definition","axiom"].includes(node.type)) paths.push({nodeId:next,path:nextPath,interpretation:"Connected discovery route; not a proof or validation of the target question."});
      if(nextPath.length<6) queue.push(nextPath);
    }
  }
  return paths.slice(0,maxPaths);
}

export function listContradictionCandidates(graph) {
  const check=validateKnowledgeNetwork(graph);
  if(!check.valid) throw new TypeError("invalid knowledge network: "+check.errors.join("; "));
  const nodes=new Map(graph.nodes.map(n=>[n.id,n]));
  return graph.edges.filter(e=>e.type==="contradicts").map(e=>({
    from:nodes.get(e.from),to:nodes.get(e.to),note:e.note || "Explicit contradiction relation; human or formal review required."
  }));
}
