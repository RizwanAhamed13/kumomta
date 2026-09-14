# Description-only solvability clarification

- Artifact set: `403ae75dfa820859ccd9d46c2aba8fa62d2d9ef0f37dbc993ff6edde053d0732`
- Changed artifact: `problem.md` only.
- Preserved artifacts: `test.patch`, `solution.patch`, and `Dockerfile` are byte-identical to set `c7d3b766...`.

## Saved-rollout evidence

The preserved batches contain 25 Nova run entries—2 in batch 01, 4 in batch 64, 9 in batch 65, and 10 in batch 79—with repeated run IDs retained across historical batches. Their recurring missed behaviors were dynamic-expression validation, nested default-aware zero construction, recursive-enum field lowering, enum-field comment attachment, and declaration ownership. The first four are already explicit in current problem lines 5, 7, and 13. The newest false-positive family showed that line 9's private-sibling example did not make the parallel public-constant and enum-identifier ownership cases sufficiently salient.

## Exact change and grounding

Problem line 9 now states that declaration ownership also applies to a public bare constant, a payload-less enum value, and an enum constructor function value autofilled during foreign construction. These are not new behaviors: `mica_q7m_preserves_values_across_owners_and_cache` already observes all three through cold and warm runtime builds, and the requirement map already assigns them to `ownership-and-order`.

No oracle was removed or relaxed. The added sentence is behavioral and does not prescribe materialization, caching, AST shape, name lowering, or emitter architecture. It therefore cannot admit a previously rejected broken implementation. It only exposes behavior already enforced by the hidden suite.

## Calibration

Historical rollouts cannot measure the new prompt's pass rate because they saw older wording. A small fresh cohort is still required. Based on the saved failure clusters, the defensible forecast is 2–4 genuine passes in ten runs, centered at 3/10; the observed result must still be reported literally.
