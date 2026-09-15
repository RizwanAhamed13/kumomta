# Rollout audit — agent-runs-3.zip

- ZIP SHA-256: `79f4eae7ec376cd9e9bb870f043dd83a54ad31e9c660b94a1a1befe686ee5af8`
- Runs: 18 total — 15 Nova, 2 Orion, 1 Vega.
- Every run passed the 747-test baseline.
- Raw verifier passes: 1/18 (`Orion_Nova_2`).
- Hosted durable passes: 0/18 after the sole passer was adjudicated a high-confidence keyword false positive.
- Nova verifier passes: 0/15; ten Nova runs reached 28/29 and failed unsupported-role safety.
- Vega: 27/29, missing both opening-parenthesis visibility cases.

The sole passer enabled fan-out for keyword tokens and panicked while isolating `self`. Exact repaired replay on artifact set `2a5f993e076ffd017bd7727bfb14039f74f39fccfa5712aebb808f1fb6506a07` gives reference 29/29, preserved genuine Nova 29/29, and the Orion FP 28/29 with the keyword panic.

The dominant Nova difficulty is distinguishing fan-out eligibility from mapped-role contribution: only a non-keyword original identifier enables fan-out, while one common supported-role rule must govern direct, nested, and attribute-expanded results without analyzing unsupported sites unsafely. The repaired description states these behavioral checkpoints explicitly without naming repository functions or removing requirements.
