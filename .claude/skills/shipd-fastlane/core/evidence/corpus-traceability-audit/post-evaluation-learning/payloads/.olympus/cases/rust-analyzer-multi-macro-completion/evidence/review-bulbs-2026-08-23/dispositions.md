# Review-bulb dispositions

Artifact source reviewed: the attached Auto Review and Test Fairness outputs for the 22-test artifact set.

| Finding or suggestion | Classification | Disposition |
|---|---|---|
| Direct multi-site attribute expansion | PROMPT-STATED | Incorporated as `unions_sites_produced_directly_by_an_attribute_expansion`. A faithful attribute-first-only mutant passed the prior 22-test suite and failed this discriminator; the reference passes. |
| `_` suppression crossed with the 64-site cap | PROMPT-STATED | Incorporated as `suppressed_underscore_sites_do_not_consume_the_viable_site_budget`; the reference budget and isolated-target recovery were repaired. |
| `(` non-visibility crossed with the 64-site cap | PROMPT-STATED | Incorporated as `non_visibility_sites_do_not_consume_the_parenthesis_viable_site_budget`; the reference now caps contributing analyses. |
| Attribute/declarative budget integration | PROMPT-STATED but advisory | Not added. Direct attribute traversal is now covered, while nested depth-first/global budgeting and attribute-to-declarative traversal are already independently enforced. No exact surviving implementation was supplied or reproduced for the additional combination. |
| Repeated punctuation/dot non-identifier route | REPO-DISCOVERABLE but advisory | Not added. Existing non-identifier compatibility and two pinned dot-completion regressions remain covered; no stable repeated-punctuation public oracle or discriminating mutant was demonstrated. |

The two omitted advisory suggestions remain non-blocking hypotheses, not readiness claims or deferred mutation entries.
