"use strict";
import { validateOmegaSL, temporalDifferences } from "./omega42-engine.mjs";
import {
  analyzeOmega42Orbit, enumerateOmega42Orbits,
  checkOmega42Uniqueness, validateResearchGraph
} from "./omega42-research.mjs";

export const OPERATIONS = Object.freeze({
  orbit: {
    instrument: "Ω42 Orbit Engine",
    description: "Compute a canonical-depth Fibonacci orbit and its Λ invariant.",
    required: ["depth", "state"]
  },
  census: {
    instrument: "Ω42 Orbit Census",
    description: "Exhaustively enumerate a finite canonical state space.",
    required: ["depth"]
  },
  uniqueness: {
    instrument: "K1/K2 Finite Checker",
    description: "Reproduce finite K1/K2 selection checks.",
    required: ["depth"]
  },
  temporal: {
    instrument: "Temporal Difference Engine",
    description: "Compute finite differences for a supplied numeric sequence.",
    required: ["values"]
  },
  omegasl: {
    instrument: "OmegaSL Envelope Validator",
    description: "Validate the provisional typed-record envelope.",
    required: ["record"]
  },
  researchGraph: {
    instrument: "Knowledge Graph Validator",
    description: "Validate graph IDs, evidence statuses, provenance and dependencies.",
    required: ["graph"]
  }
});

const INTENT_RULES = [
  [/\b(census|enumerate|all states|orbit count)\b/i, "census"],
  [/\b(k1|k2|uniqueness|unique seed|longest period)\b/i, "uniqueness"],
  [/\b(temporal|time series|lag|difference|periodicity)\b/i, "temporal"],
  [/\b(omegasl|typed record|structural language)\b/i, "omegasl"],
  [/\b(knowledge graph|research graph|dependency graph)\b/i, "researchGraph"],
  [/\b(orbit|fibonacci|lambda|\bΛ\b|norm invariant)\b/i, "orbit"]
];

export function selectInstrument({ task = "auto", intent = "" } = {}) {
  if (task !== "auto" && !Object.hasOwn(OPERATIONS, task)) {
    throw new RangeError("unknown task: " + task);
  }
  let selected = task;
  let selectionReason = "Explicit task selection.";
  if (task === "auto") {
    const match = INTENT_RULES.find(([pattern]) => pattern.test(String(intent)));
    if (!match) {
      return {
        schema: "omega42.instrument-selection.k6",
        selected: null,
        status: "NEEDS_CLARIFICATION",
        reason: "No unambiguous instrument trigger matched. Choose a task explicitly or provide a more specific intent.",
        availableTasks: Object.keys(OPERATIONS)
      };
    }
    selected = match[1];
    selectionReason = "Deterministic intent-trigger match; review the selected instrument before execution.";
  }
  return {
    schema: "omega42.instrument-selection.k6",
    selected,
    instrument: OPERATIONS[selected].instrument,
    description: OPERATIONS[selected].description,
    required: OPERATIONS[selected].required,
    status: "SELECTED",
    reason: selectionReason
  };
}

function requireFields(input, fields) {
  if (!input || typeof input !== "object" || Array.isArray(input)) {
    throw new TypeError("input must be a JSON object");
  }
  const missing = fields.filter(key => !(key in input));
  if (missing.length) throw new TypeError("missing required input field(s): " + missing.join(", "));
}

export function executeInstrument(task, input = {}) {
  if (!Object.hasOwn(OPERATIONS, task)) throw new RangeError("unknown task: " + task);
  requireFields(input, OPERATIONS[task].required);
  let result;
  switch (task) {
    case "orbit":
      result = analyzeOmega42Orbit({
        depth: Number(input.depth),
        state: input.state,
        maxStates: input.maxStates === undefined ? 200000 : Number(input.maxStates)
      });
      break;
    case "census":
      result = enumerateOmega42Orbits(Number(input.depth), {
        maxTotalStates: input.maxTotalStates === undefined ? 1000000 : Number(input.maxTotalStates)
      });
      break;
    case "uniqueness":
      result = checkOmega42Uniqueness(Number(input.depth), {
        seed: input.seed === undefined ? [2, 5] : input.seed,
        maxTotalStates: input.maxTotalStates === undefined ? 1000000 : Number(input.maxTotalStates)
      });
      break;
    case "temporal":
      result = temporalDifferences(input.values, input.lag === undefined ? 1 : Number(input.lag));
      break;
    case "omegasl":
      result = validateOmegaSL(input.record);
      break;
    case "researchGraph":
      result = validateResearchGraph(input.graph);
      break;
    default:
      throw new RangeError("unsupported task");
  }
  return {
    schema: "omega42.instrument-execution.k6",
    executionStatus: "EXECUTED",
    task,
    instrument: OPERATIONS[task].instrument,
    result
  };
}

export function runNavigation({ task = "auto", intent = "", input = {} } = {}) {
  const selection = selectInstrument({ task, intent });
  if (selection.status !== "SELECTED") {
    return { schema: "omega42.navigation-run.k6", selection, executionStatus: "NOT_EXECUTED" };
  }
  const execution = executeInstrument(selection.selected, input);
  return {
    schema: "omega42.navigation-run.k6",
    selection,
    executionStatus: execution.executionStatus,
    execution
  };
}

export function createResearchRecord({
  id, title, task, input, execution, source = "Ω42 Navigator Workbench K6",
  protocolVersion = "K6-proposal"
} = {}) {
  if (typeof id !== "string" || !id.trim()) throw new TypeError("record id is required");
  if (typeof title !== "string" || !title.trim()) throw new TypeError("record title is required");
  if (!Object.hasOwn(OPERATIONS, task)) throw new RangeError("unknown task");
  if (!execution || execution.schema !== "omega42.instrument-execution.k6" ||
      execution.task !== task || execution.executionStatus !== "EXECUTED") {
    throw new TypeError("a matching executed instrument result is required");
  }
  return {
    schema: "omega42.operations-record.k6",
    id,
    title,
    type: "instrument_result",
    status: "computed",
    executionStatus: "EXECUTED",
    task,
    instrument: OPERATIONS[task].instrument,
    protocolVersion,
    source,
    input,
    result: execution.result,
    epistemicNote: "Computed instrument output. This record does not by itself establish mathematical proof, semantic truth, causation, or application validity."
  };
}

export function validateResearchRecord(record) {
  const errors = [];
  if (!record || typeof record !== "object" || Array.isArray(record)) {
    return { schema: "omega42.operations-record-validation.k6", valid: false, errors: ["record must be an object"] };
  }
  if (record.schema !== "omega42.operations-record.k6") errors.push("unsupported record schema");
  for (const key of ["id", "title", "task", "instrument", "protocolVersion", "source"]) {
    if (typeof record[key] !== "string" || !record[key].trim()) errors.push(key + " must be a non-empty string");
  }
  if (!Object.hasOwn(OPERATIONS, record.task)) errors.push("unknown task");
  if (record.status !== "computed") errors.push("instrument result status must remain computed");
  if (record.executionStatus !== "EXECUTED") errors.push("executionStatus must be EXECUTED");
  if (!record.input || typeof record.input !== "object" || Array.isArray(record.input)) errors.push("input must be an object");
  if (!("result" in record)) errors.push("result field is required");
  if (typeof record.epistemicNote !== "string" || !record.epistemicNote.trim()) errors.push("epistemicNote is required");
  return { schema: "omega42.operations-record-validation.k6", valid: errors.length === 0, errors };
}

export function appendResearchRecord(register, record) {
  if (!register || typeof register !== "object" || Array.isArray(register) ||
      register.schema !== "omega42.operations-register.k6" || !Array.isArray(register.records)) {
    throw new TypeError("register must use omega42.operations-register.k6 schema");
  }
  const check = validateResearchRecord(record);
  if (!check.valid) throw new TypeError("invalid research record: " + check.errors.join("; "));
  if (register.records.some(item => item && item.id === record.id)) {
    throw new RangeError("duplicate research record id: " + record.id);
  }
  return { ...register, records: [...register.records, record] };
}

export function createEmptyRegister(metadata = {}) {
  return {
    schema: "omega42.operations-register.k6",
    metadata: { ...metadata },
    records: []
  };
}
