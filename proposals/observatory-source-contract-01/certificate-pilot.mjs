export const manifest = {
  "schema": "omega42.certificate.pilot.v1",
  "revision": "bf72fe90290481fbdd0194a3b57cf060105f9540",
  "source_blob": "5db44e140940ffb935a1ded423c9c4f7f69a528f",
  "certificate": {
    "path": "tools/space_prob.py",
    "blob": "2d413c848cb7f41362bcf057a9af8da70a2be1f2",
    "argv": [
      "python3",
      "tools/space_prob.py",
      "--selftest"
    ],
    "timeout_seconds": 15,
    "expected_summary": "SPACE AND PROBABILITY SELFTEST: 8 of 8"
  },
  "records": [
    {
      "id": "MF-01",
      "marker": "phi -> 5 + i, a ring isomorphism of Z[phi]/9 onto Z[i]/9"
    },
    {
      "id": "MF-02",
      "marker": "the norm goes to x^2 + y^2"
    },
    {
      "id": "MF-03",
      "marker": "phi^6 = 5 + 8 phi squares to -1"
    }
  ],
  "execution": "NOT_EXECUTED"
};
export function compareEvidence(manifest,id,evidence){
 const record=manifest.records.find(r=>r.id===id);
 if(!record||!evidence||evidence.revision!==manifest.revision||evidence.blob!==manifest.certificate.blob||JSON.stringify(evidence.argv)!==JSON.stringify(manifest.certificate.argv)||!Number.isInteger(evidence.exit_code)||typeof evidence.stdout!=="string"||evidence.stdout.length>50000)return {status:"REJECTED"};
 const lines=evidence.stdout.split(/\r?\n/);
 const marker=lines.some(l=>l.trimEnd().endsWith("PASS")&&l.trimEnd().slice(0,-4).trim()===record.marker);
 const summary=lines.includes(manifest.certificate.expected_summary);
 return {status:evidence.exit_code===0&&marker&&summary?"OUTPUT_MATCH":"OUTPUT_MISMATCH",execution:"SELF_REPORTED_EXECUTION",mathematical_verdict:"NOT_ADJUDICATED",id,marker,summary};
}
