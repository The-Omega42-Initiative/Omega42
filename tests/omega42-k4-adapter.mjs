import { analyzeOmega42Orbit } from "../site/omega42-research.mjs";
export function analyzeVector(c) {
  const r=analyzeOmega42Orbit({depth:c.depth,state:c.state});
  return {
    id:c.id, depth:c.depth, state:r.initialState, modulus:r.modulus,
    valuation:r.canonicalInvariant.valuation,
    normModulus:r.canonicalInvariant.normModulus,
    normUpToSign:r.canonicalInvariant.normUpToSign,
    zeroState:r.canonicalInvariant.zeroState, period:r.period
  };
}
