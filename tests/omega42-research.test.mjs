import test from "node:test";
import assert from "node:assert/strict";
import {
  omega42Modulus, omega42OrbitInvariant, analyzeOmega42Orbit,
  enumerateOmega42Orbits, checkOmega42Uniqueness, validateResearchGraph
} from "../site/omega42-research.mjs";

test("canonical Ω42 depth uses modulus 9^d", () => {
  assert.equal(omega42Modulus(1), 9n);
  assert.equal(omega42Modulus(2), 81n);
  assert.equal(omega42Modulus(3), 729n);
});

test("the same sample is canonical depth 1, not depth 2", () => {
  const r = analyzeOmega42Orbit({depth:1,state:[2,5]});
  assert.equal(r.modulus,"9");
  assert.equal(r.period,24);
  assert.equal(r.depth,1);
  assert.equal(r.genericExponent,2);
  assert.equal(r.omega42Depth,1);
  assert.equal(r.canonicalInvariant.depth,1);
});

test("Λ is constant along a representative orbit", () => {
  const r = analyzeOmega42Orbit({depth:2,state:[2,5]});
  const first = r.canonicalInvariant;
  for (const s of r.canonicalCycle) {
    assert.deepEqual(omega42OrbitInvariant(s,2),first);
  }
});

test("zero state has a separate invariant", () => {
  assert.deepEqual(omega42OrbitInvariant([0,0],1), {
    depth:1, valuation:2, normModulus:"1", normUpToSign:"0", zeroState:true
  });
});

test("exhaustive depth-1 census agrees with canonical five-loop result", () => {
  const r=enumerateOmega42Orbits(1);
  assert.equal(r.totalStates,"81");
  assert.equal(r.orbitCount,5);
  assert.equal(r.invariantCompleteForEnumeratedSpace,true);
  assert.equal(r.invariantDistinctAcrossEnumeratedOrbits,true);
});

test("exhaustive depth-2 census agrees with canonical 41-loop result", () => {
  const r=enumerateOmega42Orbits(2);
  assert.equal(r.totalStates,"6561");
  assert.equal(r.orbitCount,41);
  assert.equal(r.invariantCompleteForEnumeratedSpace,true);
  assert.equal(r.invariantDistinctAcrossEnumeratedOrbits,true);
});

test("frozen K1/K2 uniqueness criteria reproduce at canonical depths 1 and 2", () => {
  const d1=checkOmega42Uniqueness(1);
  assert.equal(d1.longestPeriod,24);
  assert.equal(d1.longestPeriodOrbitCount,3);
  assert.equal(d1.k1MatchesLongestPeriod,true);
  assert.equal(d1.k2SeedOccurrencesAmongLongestLoops,1);
  assert.equal(d1.k2Unique,true);
  const d2=checkOmega42Uniqueness(2);
  assert.equal(d2.longestPeriod,216);
  assert.equal(d2.longestPeriodOrbitCount,27);
  assert.equal(d2.k1MatchesLongestPeriod,true);
  assert.equal(d2.k2SeedOccurrencesAmongLongestLoops,1);
  assert.equal(d2.k2Unique,true);
});

test("frozen K1/K2 uniqueness criteria reproduce at canonical depth 3", () => {
  const d3=checkOmega42Uniqueness(3);
  assert.equal(d3.longestPeriod,1944);
  assert.equal(d3.longestPeriodOrbitCount,243);
  assert.equal(d3.k1MatchesLongestPeriod,true);
  assert.equal(d3.k2SeedOccurrencesAmongLongestLoops,1);
  assert.equal(d3.k2Unique,true);
});

test("research graph accepts typed provenance and valid dependencies", () => {
  const g={schema:"omega42.research-graph.k3",nodes:[
    {id:"D1",type:"definition",title:"Transition",status:"proved",provenance:{source:"Core"}},
    {id:"T1",type:"theorem",title:"Orbit census",status:"proved",provenance:{source:"Companion"}}
  ],edges:[{from:"T1",to:"D1",type:"depends_on"}]};
  assert.equal(validateResearchGraph(g).valid,true);
});

test("research graph rejects missing references and dependency cycles", () => {
  const g={schema:"omega42.research-graph.k3",nodes:[
    {id:"A",type:"claim",title:"A",status:"provisional",provenance:{}},
    {id:"B",type:"claim",title:"B",status:"provisional",provenance:{}}
  ],edges:[{from:"A",to:"B",type:"depends_on"},{from:"B",to:"A",type:"depends_on"},{from:"A",to:"X",type:"supports"}]};
  const r=validateResearchGraph(g);
  assert.equal(r.valid,false);
  assert.ok(r.errors.some(e=>e.includes("cycle")));
  assert.ok(r.errors.some(e=>e.includes("unknown target")));
});
