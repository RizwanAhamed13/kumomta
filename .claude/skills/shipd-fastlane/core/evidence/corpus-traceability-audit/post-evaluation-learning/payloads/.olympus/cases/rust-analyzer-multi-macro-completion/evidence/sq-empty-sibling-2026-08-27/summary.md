# Solution Quality empty-sibling repair

- Base commit: `d2e55da49132fa70a13dfbdc99122432b02cf464`
- Environment: Google Cloud Shell CLI, Rust 1.97.0, Cargo offline, shared target on `/tmp`
- Finding: filtering unsupported ordinary multi-site roles by the number of successful analyses allowed a sole type, pattern, or binding analysis to leak when another mapped sibling expanded empty.
- Repair: carry `multiple_mapped_sites` in expansion state and filter by observed mapped fan-out, including branches that yield no analysis.
- Test: the existing `repeated_occurrences_do_not_contaminate_each_other` logical test now includes empty-sibling discriminators for type, pattern, and binding roles. Logical hidden-test count remains 29.

## Results

- Prior golden plus repaired test: targeted test failed, leaking `TypeOnly` (`pre-fix.log`).
- Repaired golden plus repaired test: targeted test passed (`post-fix.log`).
- Repaired reference, new mode: 29/29 passed (`reference-new.xml`).
- Repaired reference, base mode: 747/747 passed (`reference-base.xml`).
- Untouched production plus test patch, new mode: 29/29 failed (`testonly-new.xml`).
- Untouched production plus test patch, base mode: 747/747 passed (`testonly-base.xml`).

The prompt was not broadened. This closes a stated exclusion already present in `problem.md`.
