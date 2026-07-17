# Component-test summary

All implemented experiment components passed their local component tests. The tests cover packet generation, schema validation, sealed-key separation, scorer plumbing, mock-output round trips, shell syntax, and the expanded Lean source's static preflight.

The mock agents used by these tests read sealed keys and therefore validate software plumbing only. They are not scientific receiver results and must never be included in the experiment analysis.
