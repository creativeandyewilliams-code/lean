# ISGPE v8 execution report

Model hash: `797b16e309348bbabba0927c4639aae41a7209584d730505e4b451bdaf607bf3`
Registry hash: `b7a6ef0e1d8c5c13f5699cb62142b2965d2391ecda5bd09e2d969eb191ad0385`
Master seed: `20260715`

## Closure verdict

- Formal: global_coherence_within_declared_finite_witness_class
- Execution: global_coherence
- Propagation: undetermined

The executable synthetic benchmark and codeword model-identification study completed. The independent external language-model receiver study, externally available real-trace collection, and full historical maximality audit could not be executed in this environment. Their associated claims remain undetermined and are not reported as positive results.

## Key numerical results

{
  "model_hash": "797b16e309348bbabba0927c4639aae41a7209584d730505e4b451bdaf607bf3",
  "registry_hash": "b7a6ef0e1d8c5c13f5699cb62142b2965d2391ecda5bd09e2d969eb191ad0385",
  "master_seed": 20260715,
  "deterministic_witnesses": {
    "n": 23,
    "full_pass": 23,
    "ablation_successes": 0
  },
  "fitness_triad": [
    {
      "model": "two_coordinate_without_current",
      "accuracy": 0.5,
      "status": "defeated"
    },
    {
      "model": "two_coordinate_without_target",
      "accuracy": 0.5,
      "status": "defeated"
    },
    {
      "model": "two_coordinate_without_projected",
      "accuracy": 0.5,
      "status": "defeated"
    },
    {
      "model": "full_three_coordinate_controller",
      "accuracy": 1.0,
      "status": "pass"
    }
  ],
  "lower_order_decoder_max_accuracy": 0.4805714285714286,
  "higher_order": {
    "full_cns_target_accuracy": 0.5845588235294118,
    "best_matched_comparator_target_accuracy": 0.39950980392156865,
    "full_cns_certified_reach": 0.4349877450980392,
    "best_matched_comparator_certified_reach": 0.003308823529411765,
    "full_cns_recursive_reuse": 0.34681372549019607
  },
  "no_higher_order": {
    "full_cns_target_accuracy": 0.6788793103448276,
    "best_comparator_target_accuracy": 0.5948275862068966
  },
  "coherence": {
    "full_cns_pareto_containment": 0.98671875,
    "incoherent_cns_pareto_containment": 0.7171875,
    "full_cns_fraction_harmed": 0.012109375,
    "incoherent_cns_fraction_harmed": 0.155712890625
  },
  "bounded_observation": {
    "K256_r1_generic_L2": 0.3,
    "K256_r1_generic_L16": 0.0,
    "K256_r1_monitor_false_confidence": 0.0,
    "best_retention_model": "correlation_aware_logistic"
  },
  "model_identification": {
    "selected_tests": 27,
    "minimum_candidate_accuracy": 0.932,
    "canonical_accuracy": 0.94,
    "heldout_min_distance_to_canonical": 3
  },
  "propagation_surrogate": {
    "complete_mean_pass_rate": 0.8555555555555556,
    "article_only_mean_pass_rate": 0.0,
    "status": "algorithmic artifact stress test only; independent semantic receiver criterion not executed"
  },
  "closure_verdicts": {
    "formal": "global_coherence_within_declared_finite_witness_class",
    "execution": "global_coherence",
    "propagation": "undetermined"
  },
  "title_status": 3,
  "unexecuted_external_boundaries": [
    "independent language-model receiver study across three external model families",
    "real externally available trace collection",
    "full historical maximality audit"
  ]
}

## Retention models

| model                      |   heldout_log_loss |     brier |
|:---------------------------|-------------------:|----------:|
| correlation_aware_logistic |           0.258278 | 0.0812389 |
| heterogeneous_independence |           0.46498  | 0.154729  |
| homogeneous_independence   |           1.02363  | 0.31681   |