import test from "node:test";
import assert from "node:assert/strict";
import {readFileSync} from "node:fs";
import {execFileSync} from "node:child_process";
import {analyzeVector} from "./omega42-k4-adapter.mjs";

const fixture=JSON.parse(readFileSync(new URL("./fixtures/omega42-k4-vectors.json",import.meta.url),"utf8"));
const normalize=x=>JSON.stringify(x,Object.keys(x).sort());

test("shared K4 vectors match their frozen expected results",()=>{
  for(const c of fixture.cases){
    const got=analyzeVector(c);
    assert.deepEqual({
      modulus:got.modulus,valuation:got.valuation,normModulus:got.normModulus,
      normUpToSign:got.normUpToSign,zeroState:got.zeroState,period:got.period
    },c.expected,c.id);
  }
});

test("JavaScript and independent Python reference produce identical canonical records",()=>{
  const js=fixture.cases.map(analyzeVector);
  const raw=execFileSync("python3",["tools/omega42_k4_reference.py","tests/fixtures/omega42-k4-vectors.json"],{encoding:"utf8"});
  const py=JSON.parse(raw);
  assert.deepEqual(js,py);
});

test("vector schema is versioned and covers all three canonical depths",()=>{
  assert.equal(fixture.schema,"omega42.cross-language-vectors.k4");
  assert.deepEqual([...new Set(fixture.cases.map(x=>x.depth))],[1,2,3]);
});
