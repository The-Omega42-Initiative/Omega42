"use strict";
import { analyzeOrbit, fibonacciStep } from "./omega42-engine.mjs";

function pow3(n) { return 3n ** BigInt(n); }
function modBig(n, m) { return ((n % m) + m) % m; }
function valuation3(x, cap) {
  x = x < 0n ? -x : x;
  if (x === 0n) return cap;
  let r = 0;
  while (r < cap && x % 3n === 0n) { x /= 3n; r++; }
  return r;
}

/** Canonical Ω42 tower modulus: 9^depth, not 3^depth. */
export function omega42Modulus(depth) {
  if (!Number.isInteger(depth) || depth < 1 || depth > 15) {
    throw new RangeError("Ω42 depth must be an integer from 1 to 15");
  }
  return 9n ** BigInt(depth);
}

/**
 * The repository's complete orbit invariant:
 * r = min(v3(a), v3(b), 2d);
 * c = Q(a,b)/9^r mod 3^(2d-r), identified with -c.
 * The zero state is represented by r=2d and c=0.
 */
export function omega42OrbitInvariant(state, depth) {
  const modulus = omega42Modulus(depth);
  if (!Array.isArray(state) || state.length !== 2) {
    throw new TypeError("state must be [a,b]");
  }
  const a = modBig(BigInt(state[0]), modulus);
  const b = modBig(BigInt(state[1]), modulus);
  const exponent = 2 * depth;
  const r = Math.min(valuation3(a, exponent), valuation3(b, exponent));
  if (r === exponent) {
    return { depth, valuation: r, normModulus: "1", normUpToSign: "0", zeroState: true };
  }
  const q = pow3(exponent - r);
  const norm = a * a + a * b - b * b;
  const c = modBig(norm / (9n ** BigInt(r)), q);
  const negative = modBig(-c, q);
  const canonical = c <= negative ? c : negative;
  return {
    depth,
    valuation: r,
    normModulus: q.toString(),
    normUpToSign: canonical.toString(),
    zeroState: false
  };
}

/** Ω42-depth wrapper around the generic 3^k engine. */
export function analyzeOmega42Orbit({ depth, state, maxStates = 200000 }) {
  const modulus = omega42Modulus(depth);
  const raw = analyzeOrbit({ k: 2 * depth, state, maxStates });
  return {
    ...raw,
    schema: "omega42.orbit-analysis.k3",
    depth,
    omega42Depth: depth,
    genericExponent: 2 * depth,
    modulus: modulus.toString(),
    canonicalInvariant: omega42OrbitInvariant(state, depth),
    addressRole: "secondary deterministic cycle address; canonical classification is canonicalInvariant"
  };
}

/**
 * Exhaustively partitions the finite Ω42 state space and checks that Lambda
 * is constant on each orbit and distinct between different orbits.
 */
export function enumerateOmega42Orbits(depth, { maxTotalStates = 1000000 } = {}) {
  const modulus = omega42Modulus(depth);
  const total = modulus * modulus;
  if (total > BigInt(maxTotalStates)) {
    throw new RangeError("state-space limit exceeded; increase maxTotalStates explicitly");
  }
  const seen = new Set();
  const invariantToOrbit = new Map();
  const periods = {};
  let orbitCount = 0;
  for (let a = 0n; a < modulus; a++) {
    for (let b = 0n; b < modulus; b++) {
      const startKey = a + "," + b;
      if (seen.has(startKey)) continue;
      const invariant = omega42OrbitInvariant([a, b], depth);
      const invKey = invariant.valuation + ":" + invariant.normModulus + ":" + invariant.normUpToSign;
      if (invariantToOrbit.has(invKey)) {
        throw new Error("Λ collision: distinct orbits share an invariant at " + invKey);
      }
      const orbitIndex = orbitCount++;
      invariantToOrbit.set(invKey, orbitIndex);
      let x = a, y = b, period = 0;
      do {
        const key = x + "," + y;
        if (seen.has(key)) throw new Error("orbit traversal collided with a previously classified orbit");
        seen.add(key);
        const nextInvariant = omega42OrbitInvariant([x, y], depth);
        const nextKey = nextInvariant.valuation + ":" + nextInvariant.normModulus + ":" + nextInvariant.normUpToSign;
        if (nextKey !== invKey) throw new Error("Λ is not invariant under the transition");
        [x, y] = fibonacciStep([x, y], modulus);
        period++;
        if (period > Number(total)) throw new Error("orbit traversal exceeded state-space bound");
      } while (x !== a || y !== b);
      periods[period] = (periods[period] || 0) + 1;
    }
  }
  return {
    schema: "omega42.orbit-census.k3",
    status: "EXECUTED",
    depth,
    modulus: modulus.toString(),
    totalStates: total.toString(),
    orbitCount,
    periods,
    invariantCompleteForEnumeratedSpace: BigInt(seen.size) === total,
    invariantDistinctAcrossEnumeratedOrbits: invariantToOrbit.size === orbitCount
  };
}

const NODE_TYPES = new Set(["definition","claim","theorem","derivation","instrument","test","dataset","decision","source","open_question"]);
const NODE_STATUSES = new Set(["proved","deduced","computed","source-reported","conjecture","interpretation","provisional","rejected","superseded"]);
const EDGE_TYPES = new Set(["depends_on","supports","implements","tests","contradicts","refines","supersedes","interprets","derived_from"]);

export function validateResearchGraph(graph) {
  const errors = [];
  if (!graph || typeof graph !== "object" || Array.isArray(graph)) {
    return { valid: false, errors: ["graph must be an object"] };
  }
  if (graph.schema !== "omega42.research-graph.k3") errors.push("unsupported graph schema");
  if (!Array.isArray(graph.nodes)) errors.push("nodes must be an array");
  if (!Array.isArray(graph.edges)) errors.push("edges must be an array");
  const nodes = Array.isArray(graph.nodes) ? graph.nodes : [];
  const edges = Array.isArray(graph.edges) ? graph.edges : [];
  const ids = new Set();
  for (const [i, node] of nodes.entries()) {
    if (!node || typeof node !== "object" || Array.isArray(node)) { errors.push("node " + i + " must be an object"); continue; }
    if (typeof node.id !== "string" || !node.id.trim()) errors.push("node " + i + " needs id");
    else if (ids.has(node.id)) errors.push("duplicate node id: " + node.id);
    else ids.add(node.id);
    if (!NODE_TYPES.has(node.type)) errors.push("node " + i + " has invalid type");
    if (!NODE_STATUSES.has(node.status)) errors.push("node " + i + " has invalid status");
    if (typeof node.title !== "string" || !node.title.trim()) errors.push("node " + i + " needs title");
    if (!node.provenance || typeof node.provenance !== "object" || Array.isArray(node.provenance)) errors.push("node " + i + " needs provenance object");
  }
  const dependency = new Map([...ids].map(id => [id, []]));
  for (const [i, edge] of edges.entries()) {
    if (!edge || typeof edge !== "object" || Array.isArray(edge)) { errors.push("edge " + i + " must be an object"); continue; }
    if (!EDGE_TYPES.has(edge.type)) errors.push("edge " + i + " has invalid type");
    if (!ids.has(edge.from)) errors.push("edge " + i + " has unknown source " + edge.from);
    if (!ids.has(edge.to)) errors.push("edge " + i + " has unknown target " + edge.to);
    if (edge.type === "depends_on" && ids.has(edge.from) && ids.has(edge.to)) dependency.get(edge.from).push(edge.to);
  }
  const visiting = new Set(), visited = new Set();
  function visit(id) {
    if (visiting.has(id)) return true;
    if (visited.has(id)) return false;
    visiting.add(id);
    for (const next of dependency.get(id) || []) if (visit(next)) return true;
    visiting.delete(id); visited.add(id); return false;
  }
  for (const id of ids) if (visit(id)) { errors.push("dependency cycle detected"); break; }
  return { schema: "omega42.research-graph-validation.k3", valid: errors.length === 0, nodeCount: nodes.length, edgeCount: edges.length, errors };
}
