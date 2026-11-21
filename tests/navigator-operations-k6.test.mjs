import test from "node:test";
import assert from "node:assert/strict";
import {
  OPERATIONS, selectInstrument, executeInstrument, runNavigation,
  createResearchRecord, validateResearchRecord, appendResearchRecord,
  createEmptyRegister
} from "../site/navigator-operations-k6.mjs";

test("all supported instruments have declared required inputs", () => {
  for (const item of Object.values(OPERATIONS)) assert.ok(item.required.length);
});

test("explicit selection is deterministic", () => {
  assert.equal(selectInstrument({task:"orbit"}).selected, "orbit");
});

test("ambiguous auto intent requests clarification rather than guessing", () => {
  const r = selectInstrument({task:"auto",intent:"help me understand"});
  assert.equal(r.status,"NEEDS_CLARIFICATION");
  assert.equal(r.selected,null);
});

test("intent selector routes census before generic orbit", () => {
  assert.equal(selectInstrument({intent:"enumerate all orbit states"}).selected,"census");
});

test("intent selector routes temporal work", () => {
  assert.equal(selectInstrument({intent:"compute temporal lag differences"}).selected,"temporal");
});

test("missing inputs fail before execution", () => {
  assert.throws(()=>executeInstrument("orbit",{}),/missing required/);
});

test("orbit execution uses canonical Ω42 depth", () => {
  const r=executeInstrument("orbit",{depth:1,state:[2,5]});
  assert.equal(r.executionStatus,"EXECUTED");
  assert.equal(r.result.modulus,"9");
  assert.equal(r.result.period,24);
  assert.equal(r.result.canonicalInvariant.valuation,0);
});

test("census execution returns finite-computation status", () => {
  const r=executeInstrument("census",{depth:1});
  assert.equal(r.result.status,"EXECUTED");
  assert.equal(r.result.orbitCount,5);
});

test("K1/K2 execution is explicitly finite", () => {
  const r=executeInstrument("uniqueness",{depth:1});
  assert.equal(r.result.k1MatchesLongestPeriod,true);
  assert.equal(r.result.k2Unique,true);
  assert.match(r.result.interpretation,/Finite reproduction/);
});

test("temporal execution uses supplied sequence", () => {
  const r=executeInstrument("temporal",{values:[1,2,4,7],lag:1});
  assert.deepEqual(r.result.firstDifference,[1,2,3]);
});

test("OmegaSL task validates its record", () => {
  const r=executeInstrument("omegasl",{record:{
    kind:"claim",content:"T maps a state",modality:"asserted",
    provenance:{source:"fixture",status:"reconstructed"},relations:[]
  }});
  assert.equal(r.result.valid,true);
});

test("research graph task validates dependencies", () => {
  const r=executeInstrument("researchGraph",{graph:{
    schema:"omega42.research-graph.k3",
    nodes:[{id:"D",type:"definition",title:"Transition",status:"proved",provenance:{source:"Core"}}],
    edges:[]
  }});
  assert.equal(r.result.valid,true);
});

test("navigation run preserves selected tool and execution status", () => {
  const r=runNavigation({task:"orbit",input:{depth:1,state:[2,5]}});
  assert.equal(r.selection.status,"SELECTED");
  assert.equal(r.executionStatus,"EXECUTED");
});

test("navigation run does not execute when auto-selection is ambiguous", () => {
  const r=runNavigation({intent:"maybe something",input:{}});
  assert.equal(r.executionStatus,"NOT_EXECUTED");
});

test("research record keeps computed distinct from proved", () => {
  const execution=executeInstrument("orbit",{depth:1,state:[2,5]});
  const record=createResearchRecord({
    id:"K6-TEST-001",title:"Sample orbit",task:"orbit",
    input:{depth:1,state:[2,5]},execution
  });
  assert.equal(record.status,"computed");
  assert.equal(validateResearchRecord(record).valid,true);
});

test("register append is immutable and rejects duplicate ids", () => {
  const execution=executeInstrument("orbit",{depth:1,state:[2,5]});
  const record=createResearchRecord({id:"A1",title:"Orbit",task:"orbit",input:{depth:1,state:[2,5]},execution});
  const register=createEmptyRegister();
  const next=appendResearchRecord(register,record);
  assert.equal(register.records.length,0);
  assert.equal(next.records.length,1);
  assert.throws(()=>appendResearchRecord(next,record),/duplicate/);
});

test("record validator rejects promotion to proved", () => {
  const execution=executeInstrument("orbit",{depth:1,state:[2,5]});
  const record=createResearchRecord({id:"A2",title:"Orbit",task:"orbit",input:{depth:1,state:[2,5]},execution});
  record.status="proved";
  assert.equal(validateResearchRecord(record).valid,false);
});
