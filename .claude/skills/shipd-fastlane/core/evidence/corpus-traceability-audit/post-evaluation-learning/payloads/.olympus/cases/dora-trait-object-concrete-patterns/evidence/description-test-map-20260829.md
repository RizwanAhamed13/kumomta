# Description-to-test alignment map

The description has eleven behavioral clauses. Every clause below has an
observable oracle; rejection cases assert only compilation rejection.

| Description clause | Enforcing tests and oracle |
|---|---|
| Inspect the concrete value stored in a trait object using existing patterns. | Reference, literals, enum, generic, control, and catchall runtime files erase values to traits and recover the concrete branch and payload. |
| Constructor patterns are compatible when the concrete type implements the trait. | Reference class, inline struct, enum, and generic class/struct/enum cases compile and return concrete payloads. |
| Literal patterns are compatible when the concrete type implements the trait. | Literal runtime covers UInt8, Int32, Int64, Bool, Char, Float32, Float64, and String with matching and nearby nonmatching values. |
| Compatibility includes trait arguments and associated-type bindings. | Reference and generic positives use both; separate constructor and literal rejection files independently reject a wrong trait argument and a wrong associated binding. |
| Incompatible and ambiguous patterns are compile-time errors. | Six independent rejection commands cover constructor trait arguments, constructor associated bindings, literal trait arguments, literal associated bindings, plus fully and partially unconstrained generic ambiguity. |
| Check concrete runtime type before fields or payloads. | Control mismatch uses a zero-field class against a nested payload pattern; enum `is` distinguishes empty, single-payload, and pair variants before extraction. |
| A mismatch continues without evaluating nested patterns or guards. | Control tests both values of the latent guard while a wrong shape keeps the guard count at zero; nested wrong-shape extraction also falls back. Matching shapes cover both true and false guards. |
| Successful matches expose concrete specialized fields and bindings. | Reference returns `Cell` identity; generic class returns Int64, generic struct returns String, and generic enum returns specialized payloads. |
| Behavior works in `is`, conditional chains, `match`, nested patterns, and alternatives. | Literal, enum, struct, and generic `is`; reference and catchall chains; all positive files use `match`; control and enum nest patterns; control and reference use alternatives. |
| Trait objects remain open-ended; concrete-only matches are not exhaustive, while wildcard and variable fallbacks are. | Top-level and nested concrete-only files are rejected; catchall executes wildcard and variable fallbacks; nested positive matches include fallback arms. |
| Preserve identity, mutation visibility, GC safety, backend parity, and existing behavior. | Reference checks identity before/after mutation and collection. InlineRef extracts a managed `Cell` from an inline implementation before/after mutation and collection. Every successful file runs Cannon and Boots. Base mode runs direct class/struct/enum/literal patterns, trait-object dispatch, casts and failed-cast diagnostics, bytecode tests, and compiler/AOT tests. |

Reverse direction: every hidden runtime assertion belongs to one of the clauses
above. Base assertions are pinned-repository regressions. Error-path commands
are rejection-only and do not pin diagnostic text, error variants, payloads, or
exit-code representation.
