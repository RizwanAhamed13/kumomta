
Test Quality
Test Quality
VERDICT
PASS
ALL 17 TESTS FAIR
PASS — all hidden assertions are fair to an agent with the prompt and repository; unfairTestCount is 0. The tests mostly mirror unusually explicit prompt requirements, while the few extra concrete expectations (rack semantics, latency filtering, and execution-history shape) are directly discoverable in neighboring repository code. Quality is generally high and behavior-oriented. Shared advisory concern: the observability/speculation portions of prepared_and_cached_manual_apis_carry_opaque_continuations and affinity_preserves_metrics_tracing_history_speculation_and_errors orchestrate speculative execution with delayed proxy responses (100 ms) and zero retry delay; although likely stable, they have some scheduler/load sensitivity. This shared timing issue does not affect fairness. Coverage is broad, but continuation opacity/isolation, additional replica routes, and full cross-API observability/error preservation remain worth strengthening.
REQUIREMENT COVERAGE (13/21 COVERED)
Advisory only — prompt-stated requirements and whether the hidden tests pin them.

PARTIAL
Automatic and manual later pages preserve coordinator affinity only after the active policy re-evaluates the previous successful coordinator against current routing and cluster state.
"Make automatic and manual paging preserve coordinator affinity without bypassing the active load-balancing policy. Before every later page, ask that policy whether the preceding page's successful coordinator remains eligible under the current routing and cluster state."
manual_unprepared_affinity_is_policy_gated_and_preserves_raw_api, rejected_custom_policy_hint_falls_back_to_the_fresh_plan, automatic_paging_consults_the_same_policy_hook
COVERED
The LoadBalancingPolicy trait default rejects affinity unless overridden.
"The trait's default must reject affinity unless a custom policy opts in."
policy_default_rejects_retained_coordinators, compile-time public API contracts
PARTIAL
DefaultPolicy accepts only a current, enabled, connected local replica for the routed token/table when active filters pass.
"The default policy accepts only the current enabled, connected local replica for the routed token and table when that target passes its active filters."
default_policy_coordinator_eligibility_matrix — core and topology assertions, default_policy_coordinator_eligibility_matrix — rack-preference assertion, paging_affinity_real_host_filter_rejects_coordinator, paging_affinity_latency_penalized_coordinator_is_rejected
COVERED
DefaultPolicy rejects remote, non-replica, removed, replaced, disabled, disconnected, and filtered targets.
"Reject remote, non-replica, removed, replaced, disabled, disconnected, and filtered targets"
default_policy_coordinator_eligibility_matrix — core and topology assertions, paging_affinity_real_host_filter_rejects_coordinator, paging_affinity_latency_penalized_coordinator_is_rejected
PARTIAL
DefaultPolicy rejects affinity when replica eligibility cannot be established.
"and reject when replica eligibility cannot be established."
default_policy_coordinator_eligibility_matrix — core and topology assertions, manual_unprepared_affinity_is_policy_gated_and_preserves_raw_api
COVERED
An eligible preferred target is attempted once before a fresh plan.
"Attempt an eligible preferred target once, before a fresh plan."
failed_preferred_target_is_tried_once_before_fresh_fallback, preferred_plan_preserves_order_and_suppresses_only_the_selected_target
COVERED
The fresh plan keeps its relative order.
"Preserve the fresh plan's relative order."
preferred_plan_preserves_order_and_suppresses_only_the_selected_target
COVERED
A sharded preference suppresses only the same node-and-shard target later in the plan.
"Suppress only the same node and shard for a sharded preference"
preferred_plan_preserves_order_and_suppresses_only_the_selected_target
COVERED
An unsharded preference suppresses all later targets for that node.
"suppress every later target for an unsharded preferred node."
preferred_plan_preserves_order_and_suppresses_only_the_selected_target
PARTIAL
Manual unprepared, prepared, and caching calls use an opaque continuation carrying server state and the preceding successful coordinator.
"Manual unprepared, prepared, and caching-session calls use an opaque continuation containing server paging state and the preceding successful coordinator."
manual_unprepared_affinity_is_policy_gated_and_preserves_raw_api, prepared_and_cached_manual_apis_carry_opaque_continuations — prepared continuation and legacy API, prepared_and_cached_manual_apis_carry_opaque_continuations — caching continuation and legacy API, compile-time public API contracts
COVERED
The first affinity call has no preferred coordinator.
"The first call has no preference"
manual_unprepared_affinity_is_policy_gated_and_preserves_raw_api, prepared_and_cached_manual_apis_carry_opaque_continuations — prepared continuation and legacy API, automatic_paging_consults_the_same_policy_hook
COVERED
Completed manual results return no continuation.
"completed results return no continuation."
manual_unprepared_affinity_is_policy_gated_and_preserves_raw_api, prepared_and_cached_manual_apis_carry_opaque_continuations — prepared continuation and legacy API, prepared_and_cached_manual_apis_carry_opaque_continuations — caching continuation and legacy API, affinity_preserves_metrics_tracing_history_speculation_and_errors
COVERED
Retries retain normal retry behavior.
"Retry normally"
retries_replace_the_next_affinity_hint_with_the_winner, failed_preferred_target_is_tried_once_before_fresh_fallback
COVERED
The target that ultimately succeeds becomes the next affinity preference.
"the target that ultimately succeeds becomes the next preference."
retries_replace_the_next_affinity_hint_with_the_winner, failed_preferred_target_is_tried_once_before_fresh_fallback
COVERED
Legacy raw PagingState APIs remain available and functional.
"Preserve legacy raw `PagingState` APIs"
manual_unprepared_affinity_is_policy_gated_and_preserves_raw_api, prepared_and_cached_manual_apis_carry_opaque_continuations — prepared continuation and legacy API, prepared_and_cached_manual_apis_carry_opaque_continuations — caching continuation and legacy API
PARTIAL
Error behavior is preserved.
"errors"
affinity_preserves_metrics_tracing_history_speculation_and_errors
PARTIAL
Metrics behavior is preserved.
"metrics"
prepared_and_cached_manual_apis_carry_opaque_continuations — prepared execution features, prepared_and_cached_manual_apis_carry_opaque_continuations — caching execution features, affinity_preserves_metrics_tracing_history_speculation_and_errors
PARTIAL
Tracing behavior is preserved.
"tracing"
prepared_and_cached_manual_apis_carry_opaque_continuations — prepared execution features, prepared_and_cached_manual_apis_carry_opaque_continuations — caching execution features, affinity_preserves_metrics_tracing_history_speculation_and_errors
PARTIAL
Speculative execution behavior is preserved.
"and speculative execution."
prepared_and_cached_manual_apis_carry_opaque_continuations — prepared execution features, prepared_and_cached_manual_apis_carry_opaque_continuations — caching execution features, affinity_preserves_metrics_tracing_history_speculation_and_errors
COVERED
The three named affinity-aware single-page methods are publicly exposed and return the exact stated Result tuple.
"Expose `scylla::client::paging_continuation::PagingContinuation` and the following affinity-aware single-page methods:"
compile-time public API contracts, manual_unprepared_affinity_is_policy_gated_and_preserves_raw_api, prepared_and_cached_manual_apis_carry_opaque_continuations — prepared continuation and legacy API, prepared_and_cached_manual_apis_carry_opaque_continuations — caching continuation and legacy API
COVERED
Policies expose the coordinator-preference hook and Plan exposes the preferred-target constructor with the stated signatures.
"Policies and plans must also expose:"
compile-time public API contracts, preferred_plan_preserves_order_and_suppresses_only_the_selected_target
COVERAGE SUGGESTIONS (5)
Advisory only — these don't affect the check result.

Continuation isolation and opacity
NOT DISCRIMINATING
PROMPT-STATED
Requirement: Manual unprepared, prepared, and caching-session calls use an opaque continuation carrying server state and the preceding successful coordinator.
Interleave two manual paging sequences on one Session/CachingSession and resume them out of order, proving that each continuation independently carries its own server state and coordinator rather than relying on session-global state. Add a compile-fail privacy check showing external code cannot destructure or mutate continuation internals.
DefaultPolicy route breadth
SINGLE POINT
PROMPT-STATED
Requirement: DefaultPolicy accepts only a current, enabled, connected local replica for the routed token/table when active filters pass.
Add eligibility checks for at least one additional token/table strategy and for a remote replica while DC failover is enabled. This would reject implementations hardcoded to token 160/TABLE_NTS_RF_2 or implementations that mistakenly equate failover eligibility with affinity eligibility.
Unestablishable replica metadata
SINGLE POINT
PROMPT-STATED
Requirement: DefaultPolicy rejects affinity when replica eligibility cannot be established.
Test a supplied token/table pair whose table or keyspace is absent/invalid in current schema, not only missing token or missing table fields, and require rejection.
Current RoutingInfo delivered to custom hooks
NOT DISCRIMINATING
PROMPT-STATED
Requirement: Automatic and manual later pages preserve coordinator affinity only after the active policy re-evaluates the previous successful coordinator against current routing and cluster state.
Use a prepared token-aware query and a recording custom policy to assert that later-page hook calls receive the expected token and table, alongside the current ClusterState. Existing tests prove dynamic cluster state and gating but do not inspect routed fields passed to a custom hook.
Cross-API preservation of execution behavior
SINGLE POINT
PROMPT-STATED
Requirement: Error behavior is preserved.
Exercise errors and the relevant request/error metrics for prepared and caching affinity APIs, and add an automatic-paging observability/speculation regression case. A shortcut could preserve these paths only for the tested unprepared manual API while violating the broader preservation requirement.
QUALITY NOTES (17)
PROMPT-STATED
default_policy_coordinator_eligibility_matrix — core and topology assertions
The matrix closely tracks the stated rejection list and constructs realistic topology variants. Its positive replica check is concentrated on one token/table route, so a route-specific hardcode could evade it.
OVERFIT
REPO-DISCOVERABLE
default_policy_coordinator_eligibility_matrix — rack-preference assertion
This is a useful ambiguity-resolving assertion and is supported directly by the pre-existing policy documentation and implementation.
PROMPT-STATED
paging_affinity_real_host_filter_rejects_coordinator
Fair but substantially redundant with the host-filter-disabled assertion in the larger eligibility matrix.
REPO-DISCOVERABLE
paging_affinity_latency_penalized_coordinator_is_rejected
The expectation is well grounded. It uses Instant::now() and the default finite 10-second retry period, so an extreme test stall could theoretically let the penalty expire before assertion.
TIMING
PROMPT-STATED
manual_unprepared_affinity_is_policy_gated_and_preserves_raw_api
Strong end-to-end coverage of state propagation, coordinator retention, exact hook frequency, completion, and legacy compatibility.
PROMPT-STATED
prepared_and_cached_manual_apis_carry_opaque_continuations — prepared continuation and legacy API
Fair and behaviorally useful. The state assertion is permissive (>=1), so it verifies carriage but not absence of duplicate state-bearing attempts.
REPO-DISCOVERABLE
prepared_and_cached_manual_apis_carry_opaque_continuations — prepared execution features
Fair integration check that the new wrapper stays on the common execution path. The delayed-response/zero-interval orchestration is noted as a shared timing concern in the overall assessment.
PROMPT-STATED
prepared_and_cached_manual_apis_carry_opaque_continuations — caching continuation and legacy API
Fair coverage of the caching wrapper. As in the prepared branch, the >=1 state assertion does not reject duplicate transmissions.
REPO-DISCOVERABLE
prepared_and_cached_manual_apis_carry_opaque_continuations — caching execution features
Fair and appropriately checks the wrapper rather than only Session. It shares the suite's delay-based speculative-execution timing concern.
PROMPT-STATED
rejected_custom_policy_hint_falls_back_to_the_fresh_plan
Cleanly distinguishes dynamic policy gating from unconditional stickiness.
PROMPT-STATED
automatic_paging_consults_the_same_policy_hook
Strong multi-branch coverage of acceptance, rejection, prepared/unprepared automatic paging, and live topology changes. The prepared branch checks stability but does not independently assert its hook-call count.
PROMPT-STATED
policy_default_rejects_retained_coordinators
Directly discriminates a false/default-accept implementation.
PROMPT-STATED
retries_replace_the_next_affinity_hint_with_the_winner
Good discriminating test against retaining the initially attempted loser rather than the successful retry target.
PROMPT-STATED
failed_preferred_target_is_tried_once_before_fresh_fallback
Precisely tests the important once-before-fallback semantics without pinning an error message.
REPO-DISCOVERABLE
affinity_preserves_metrics_tracing_history_speculation_and_errors
Fair. Error compatibility is checked only at the variant/discriminant level, which is robust but intentionally shallow. The successful speculation branch shares the suite's delay-based timing concern.
PROMPT-STATED
preferred_plan_preserves_order_and_suppresses_only_the_selected_target
A strong direct plan test covering sharded, materialized duplicate, unsharded, and no-preference branches. Dry proxy nodes have one materializable shard, avoiding effective RNG variation despite Plan's generic random-shard support.
PROMPT-STATED
compile-time public API contracts
Appropriate compile-time protection for exact public surface and object safety. It does not by itself prove that PagingContinuation's internals are actually opaque.
TASK SUMMARY
The task asks the driver to retain the coordinator that successfully served one page, but only as a policy-approved preference for the next page. Before every later automatic or affinity-aware manual page, the active load-balancing policy must re-evaluate that coordinator against current routing and cluster state. The trait default rejects affinity; DefaultPolicy opts in only for a current, enabled, connected, local replica whose replica status can be established from token/table routing and which passes active filters. An approved preference is prepended once to a newly generated plan without disturbing the plan's relative order, with node+shard-specific suppression for sharded targets and whole-node suppression for unsharded targets. New manual APIs use an opaque continuation carrying the server paging state and successful coordinator, while old raw PagingState APIs and execution behavior (retry, errors, metrics, tracing, history/config propagation, and speculation) must remain intact. The repository already had unconditional automatic coordinator stability in scylla/src/client/pager.rs:301-359, existing raw single-page APIs in scylla/src/client/session.rs:745-752 and 922-939, and the common execution/configuration machinery in scylla/src/client/execution.rs:90-159.
Completed in 279.1s

Hide raw output
{
  "completed": true,
  "coverageSuggestions": [
    {
      "area": "Continuation isolation and opacity",
      "gapKind": "not_discriminating",
      "requirement": "Manual unprepared, prepared, and caching-session calls use an opaque continuation carrying server state and the preceding successful coordinator.",
      "sourceIfAdded": "Prompt-stated",
      "suggestion": "Interleave two manual paging sequences on one Session/CachingSession and resume them out of order, proving that each continuation independently carries its own server state and coordinator rather than relying on session-global state. Add a compile-fail privacy check showing external code cannot destructure or mutate continuation internals."
    },
    {
      "area": "DefaultPolicy route breadth",
      "gapKind": "single_point",
      "requirement": "DefaultPolicy accepts only a current, enabled, connected local replica for the routed token/table when active filters pass.",
      "sourceIfAdded": "Prompt-stated",
      "suggestion": "Add eligibility checks for at least one additional token/table strategy and for a remote replica while DC failover is enabled. This would reject implementations hardcoded to token 160/TABLE_NTS_RF_2 or implementations that mistakenly equate failover eligibility with affinity eligibility."
    },
    {
      "area": "Unestablishable replica metadata",
      "gapKind": "single_point",
      "requirement": "DefaultPolicy rejects affinity when replica eligibility cannot be established.",
      "sourceIfAdded": "Prompt-stated",
      "suggestion": "Test a supplied token/table pair whose table or keyspace is absent/invalid in current schema, not only missing token or missing table fields, and require rejection."
    },
    {
      "area": "Current RoutingInfo delivered to custom hooks",
      "gapKind": "not_discriminating",
      "requirement": "Automatic and manual later pages preserve coordinator affinity only after the active policy re-evaluates the previous successful coordinator against current routing and cluster state.",
      "sourceIfAdded": "Prompt-stated",
      "suggestion": "Use a prepared token-aware query and a recording custom policy to assert that later-page hook calls receive the expected token and table, alongside the current ClusterState. Existing tests prove dynamic cluster state and gating but do not inspect routed fields passed to a custom hook."
    },
    {
      "area": "Cross-API preservation of execution behavior",
      "gapKind": "single_point",
      "requirement": "Error behavior is preserved.",
      "sourceIfAdded": "Prompt-stated",
      "suggestion": "Exercise errors and the relevant request/error metrics for prepared and caching affinity APIs, and add an automatic-paging observability/speculation regression case. A shortcut could preserve these paths only for the tested unprepared manual API while violating the broader preservation requirement."
    }
  ],
  "error": "",
  "executionTimeSeconds": 279.118031,
  "message": "All hidden tests are fair.",
  "overall": "PASS — all hidden assertions are fair to an agent with the prompt and repository; unfairTestCount is 0. The tests mostly mirror unusually explicit prompt requirements, while the few extra concrete expectations (rack semantics, latency filtering, and execution-history shape) are directly discoverable in neighboring repository code. Quality is generally high and behavior-oriented. Shared advisory concern: the observability/speculation portions of prepared_and_cached_manual_apis_carry_opaque_continuations and affinity_preserves_metrics_tracing_history_speculation_and_errors orchestrate speculative execution with delayed proxy responses (100 ms) and zero retry delay; although likely stable, they have some scheduler/load sensitivity. This shared timing issue does not affect fairness. Coverage is broad, but continuation opacity/isolation, additional replica routes, and full cross-API observability/error preservation remain worth strengthening.",
  "requirements": [
    {
      "covered": "partial",
      "coveringTests": [
        "manual_unprepared_affinity_is_policy_gated_and_preserves_raw_api",
        "rejected_custom_policy_hint_falls_back_to_the_fresh_plan",
        "automatic_paging_consults_the_same_policy_hook"
      ],
      "requirement": "Automatic and manual later pages preserve coordinator affinity only after the active policy re-evaluates the previous successful coordinator against current routing and cluster state.",
      "sourceQuote": "Make automatic and manual paging preserve coordinator affinity without bypassing the active load-balancing policy. Before every later page, ask that policy whether the preceding page's successful coordinator remains eligible under the current routing and cluster state."
    },
    {
      "covered": "yes",
      "coveringTests": [
        "policy_default_rejects_retained_coordinators",
        "compile-time public API contracts"
      ],
      "requirement": "The LoadBalancingPolicy trait default rejects affinity unless overridden.",
      "sourceQuote": "The trait's default must reject affinity unless a custom policy opts in."
    },
    {
      "covered": "partial",
      "coveringTests": [
        "default_policy_coordinator_eligibility_matrix — core and topology assertions",
        "default_policy_coordinator_eligibility_matrix — rack-preference assertion",
        "paging_affinity_real_host_filter_rejects_coordinator",
        "paging_affinity_latency_penalized_coordinator_is_rejected"
      ],
      "requirement": "DefaultPolicy accepts only a current, enabled, connected local replica for the routed token/table when active filters pass.",
      "sourceQuote": "The default policy accepts only the current enabled, connected local replica for the routed token and table when that target passes its active filters."
    },
    {
      "covered": "yes",
      "coveringTests": [
        "default_policy_coordinator_eligibility_matrix — core and topology assertions",
        "paging_affinity_real_host_filter_rejects_coordinator",
        "paging_affinity_latency_penalized_coordinator_is_rejected"
      ],
      "requirement": "DefaultPolicy rejects remote, non-replica, removed, replaced, disabled, disconnected, and filtered targets.",
      "sourceQuote": "Reject remote, non-replica, removed, replaced, disabled, disconnected, and filtered targets"
    },
    {
      "covered": "partial",
      "coveringTests": [
        "default_policy_coordinator_eligibility_matrix — core and topology assertions",
        "manual_unprepared_affinity_is_policy_gated_and_preserves_raw_api"
      ],
      "requirement": "DefaultPolicy rejects affinity when replica eligibility cannot be established.",
      "sourceQuote": "and reject when replica eligibility cannot be established."
    },
    {
      "covered": "yes",
      "coveringTests": [
        "failed_preferred_target_is_tried_once_before_fresh_fallback",
        "preferred_plan_preserves_order_and_suppresses_only_the_selected_target"
      ],
      "requirement": "An eligible preferred target is attempted once before a fresh plan.",
      "sourceQuote": "Attempt an eligible preferred target once, before a fresh plan."
    },
    {
      "covered": "yes",
      "coveringTests": [
        "preferred_plan_preserves_order_and_suppresses_only_the_selected_target"
      ],
      "requirement": "The fresh plan keeps its relative order.",
      "sourceQuote": "Preserve the fresh plan's relative order."
    },
    {
      "covered": "yes",
      "coveringTests": [
        "preferred_plan_preserves_order_and_suppresses_only_the_selected_target"
      ],
      "requirement": "A sharded preference suppresses only the same node-and-shard target later in the plan.",
      "sourceQuote": "Suppress only the same node and shard for a sharded preference"
    },
    {
      "covered": "yes",
      "coveringTests": [
        "preferred_plan_preserves_order_and_suppresses_only_the_selected_target"
      ],
      "requirement": "An unsharded preference suppresses all later targets for that node.",
      "sourceQuote": "suppress every later target for an unsharded preferred node."
    },
    {
      "covered": "partial",
      "coveringTests": [
        "manual_unprepared_affinity_is_policy_gated_and_preserves_raw_api",
        "prepared_and_cached_manual_apis_carry_opaque_continuations — prepared continuation and legacy API",
        "prepared_and_cached_manual_apis_carry_opaque_continuations — caching continuation and legacy API",
        "compile-time public API contracts"
      ],
      "requirement": "Manual unprepared, prepared, and caching calls use an opaque continuation carrying server state and the preceding successful coordinator.",
      "sourceQuote": "Manual unprepared, prepared, and caching-session calls use an opaque continuation containing server paging state and the preceding successful coordinator."
    },
    {
      "covered": "yes",
      "coveringTests": [
        "manual_unprepared_affinity_is_policy_gated_and_preserves_raw_api",
        "prepared_and_cached_manual_apis_carry_opaque_continuations — prepared continuation and legacy API",
        "automatic_paging_consults_the_same_policy_hook"
      ],
      "requirement": "The first affinity call has no preferred coordinator.",
      "sourceQuote": "The first call has no preference"
    },
    {
      "covered": "yes",
      "coveringTests": [
        "manual_unprepared_affinity_is_policy_gated_and_preserves_raw_api",
        "prepared_and_cached_manual_apis_carry_opaque_continuations — prepared continuation and legacy API",
        "prepared_and_cached_manual_apis_carry_opaque_continuations — caching continuation and legacy API",
        "affinity_preserves_metrics_tracing_history_speculation_and_errors"
      ],
      "requirement": "Completed manual results return no continuation.",
      "sourceQuote": "completed results return no continuation."
    },
    {
      "covered": "yes",
      "coveringTests": [
        "retries_replace_the_next_affinity_hint_with_the_winner",
        "failed_preferred_target_is_tried_once_before_fresh_fallback"
      ],
      "requirement": "Retries retain normal retry behavior.",
      "sourceQuote": "Retry normally"
    },
    {
      "covered": "yes",
      "coveringTests": [
        "retries_replace_the_next_affinity_hint_with_the_winner",
        "failed_preferred_target_is_tried_once_before_fresh_fallback"
      ],
      "requirement": "The target that ultimately succeeds becomes the next affinity preference.",
      "sourceQuote": "the target that ultimately succeeds becomes the next preference."
    },
    {
      "covered": "yes",
      "coveringTests": [
        "manual_unprepared_affinity_is_policy_gated_and_preserves_raw_api",
        "prepared_and_cached_manual_apis_carry_opaque_continuations — prepared continuation and legacy API",
        "prepared_and_cached_manual_apis_carry_opaque_continuations — caching continuation and legacy API"
      ],
      "requirement": "Legacy raw PagingState APIs remain available and functional.",
      "sourceQuote": "Preserve legacy raw `PagingState` APIs"
    },
    {
      "covered": "partial",
      "coveringTests": [
        "affinity_preserves_metrics_tracing_history_speculation_and_errors"
      ],
      "requirement": "Error behavior is preserved.",
      "sourceQuote": "errors"
    },
    {
      "covered": "partial",
      "coveringTests": [
        "prepared_and_cached_manual_apis_carry_opaque_continuations — prepared execution features",
        "prepared_and_cached_manual_apis_carry_opaque_continuations — caching execution features",
        "affinity_preserves_metrics_tracing_history_speculation_and_errors"
      ],
      "requirement": "Metrics behavior is preserved.",
      "sourceQuote": "metrics"
    },
    {
      "covered": "partial",
      "coveringTests": [
        "prepared_and_cached_manual_apis_carry_opaque_continuations — prepared execution features",
        "prepared_and_cached_manual_apis_carry_opaque_continuations — caching execution features",
        "affinity_preserves_metrics_tracing_history_speculation_and_errors"
      ],
      "requirement": "Tracing behavior is preserved.",
      "sourceQuote": "tracing"
    },
    {
      "covered": "partial",
      "coveringTests": [
        "prepared_and_cached_manual_apis_carry_opaque_continuations — prepared execution features",
        "prepared_and_cached_manual_apis_carry_opaque_continuations — caching execution features",
        "affinity_preserves_metrics_tracing_history_speculation_and_errors"
      ],
      "requirement": "Speculative execution behavior is preserved.",
      "sourceQuote": "and speculative execution."
    },
    {
      "covered": "yes",
      "coveringTests": [
        "compile-time public API contracts",
        "manual_unprepared_affinity_is_policy_gated_and_preserves_raw_api",
        "prepared_and_cached_manual_apis_carry_opaque_continuations — prepared continuation and legacy API",
        "prepared_and_cached_manual_apis_carry_opaque_continuations — caching continuation and legacy API"
      ],
      "requirement": "The three named affinity-aware single-page methods are publicly exposed and return the exact stated Result tuple.",
      "sourceQuote": "Expose `scylla::client::paging_continuation::PagingContinuation` and the following affinity-aware single-page methods:"
    },
    {
      "covered": "yes",
      "coveringTests": [
        "compile-time public API contracts",
        "preferred_plan_preserves_order_and_suppresses_only_the_selected_target"
      ],
      "requirement": "Policies expose the coordinator-preference hook and Plan exposes the preferred-target constructor with the stated signatures.",
      "sourceQuote": "Policies and plans must also expose:"
    }
  ],
  "taskSummary": "The task asks the driver to retain the coordinator that successfully served one page, but only as a policy-approved preference for the next page. Before every later automatic or affinity-aware manual page, the active load-balancing policy must re-evaluate that coordinator against current routing and cluster state. The trait default rejects affinity; DefaultPolicy opts in only for a current, enabled, connected, local replica whose replica status can be established from token/table routing and which passes active filters. An approved preference is prepended once to a newly generated plan without disturbing the plan's relative order, with node+shard-specific suppression for sharded targets and whole-node suppression for unsharded targets. New manual APIs use an opaque continuation carrying the server paging state and successful coordinator, while old raw PagingState APIs and execution behavior (retry, errors, metrics, tracing, history/config propagation, and speculation) must remain intact. The repository already had unconditional automatic coordinator stability in scylla/src/client/pager.rs:301-359, existing raw single-page APIs in scylla/src/client/session.rs:745-752 and 922-939, and the common execution/configuration machinery in scylla/src/client/execution.rs:90-159.",
  "tests": [
    {
      "concerns": [
        "overfit_single_point"
      ],
      "evidence": "The prompt expressly says the default accepts only the \"current enabled, connected local replica for the routed token and table\" and rejects \"remote, non-replica, removed, replaced, disabled, disconnected\" targets and cases where replica eligibility cannot be established. The repository clarifies current-node identity: topology maintenance treats same-host-ID but pointer-distinct nodes as recreated (scylla/src/cluster/state.rs:436-464), and tablet replica identity likewise requires Arc identity rather than host ID alone (scylla/src/routing/locator/tablets.rs:188-208).",
      "fairness": "Prompt-stated",
      "name": "default_policy_coordinator_eligibility_matrix — core and topology assertions",
      "qualityCheck": "The matrix closely tracks the stated rejection list and constructs realistic topology variants. Its positive replica check is concentrated on one token/table route, so a route-specific hardcode could evade it.",
      "verifies": "For token 160 and TABLE_NTS_RF_2 under preferred DC \"eu\", the hook returns true for port-1's connected local replica and false for a remote replica and local non-replica; it also returns false when token or table is absent, when the old coordinator has been removed, when a fresh Node object with the same host ID replaced it, when the current node is host-filter-disabled, and when its pool is disconnected."
    },
    {
      "concerns": [],
      "evidence": "The repository explicitly says a preferred rack only orders local-rack replicas before other replicas in the datacenter (scylla/src/policies/load_balancing/default.rs:1017-1022), and the existing pick implementation falls through from a rack-local replica search to a datacenter-wide replica search (scylla/src/policies/load_balancing/default.rs:177-211). Thus rack is an ordering preference, not an eligibility filter.",
      "fairness": "Repo-discoverable",
      "name": "default_policy_coordinator_eligibility_matrix — rack-preference assertion",
      "qualityCheck": "This is a useful ambiguity-resolving assertion and is supported directly by the pre-existing policy documentation and implementation.",
      "verifies": "With preferred DC \"eu\" and preferred rack \"r1\", a connected local replica in the same DC but rack \"r2\" is still accepted by is_coordinator_preferred."
    },
    {
      "concerns": [],
      "evidence": "The prompt explicitly requires rejecting \"disabled\" and \"filtered targets.\" Repository topology construction sets is_enabled from HostFilter::accept and creates a disabled Node when rejected (scylla/src/cluster/state.rs:328-351), matching the test setup exactly.",
      "fairness": "Prompt-stated",
      "name": "paging_affinity_real_host_filter_rejects_coordinator",
      "qualityCheck": "Fair but substantially redundant with the host-filter-disabled assertion in the larger eligibility matrix.",
      "verifies": "A node retained in ClusterState but disabled by an actual HostFilter is rejected by DefaultPolicy's coordinator-affinity hook, even after test connectivity is enabled for all nodes."
    },
    {
      "concerns": [
        "timing_sensitivity"
      ],
      "evidence": "The prompt requires the target to pass active filters. The repository identifies latency awareness as part of the active pick predicate: penalized nodes are filtered from pick (scylla/src/policies/load_balancing/default.rs:108-121), and the builder constructs pick_predicate as is_alive && latency_predicate (scylla/src/policies/load_balancing/default.rs:959-969). The configured threshold and minimum-measurement semantics are documented at scylla/src/policies/load_balancing/default.rs:3182-3207.",
      "fairness": "Repo-discoverable",
      "name": "paging_affinity_latency_penalized_coordinator_is_rejected",
      "qualityCheck": "The expectation is well grounded. It uses Instant::now() and the default finite 10-second retry period, so an extreme test stall could theoretically let the penalty expire before assertion.",
      "verifies": "After latency statistics make node A's 1-second average penalized relative to node C's 1-millisecond average at the configured minimum sample count, DefaultPolicy returns false for A as the preferred coordinator."
    },
    {
      "concerns": [],
      "evidence": "The prompt says manual unprepared calls carry an opaque continuation containing server state and the prior successful coordinator, the first call has no preference, every later page consults policy, completed results have no continuation, and legacy raw PagingState APIs remain. It also requires rejection when replica eligibility cannot be established. Existing QueryResult exposes the successful Coordinator (scylla/src/response/query_result.rs:71-91,144-148), and the raw API contract is visible at scylla/src/client/session.rs:700-752.",
      "fairness": "Prompt-stated",
      "name": "manual_unprepared_affinity_is_policy_gated_and_preserves_raw_api",
      "qualityCheck": "Strong end-to-end coverage of state propagation, coordinator retention, exact hook frequency, completion, and legacy compatibility.",
      "verifies": "Across three unprepared affinity calls, each server paging state ([11] then [12]) is sent exactly once; the second and third successful coordinators equal the first; the policy hook records exactly the prior successful address before each of the two later pages; the final continuation is None; DefaultPolicy rejects the first coordinator when routing lacks token/table; and the legacy query_single_page API still returns HasMorePages."
    },
    {
      "concerns": [],
      "evidence": "The prompt explicitly names the prepared affinity API, its exact result type, continuation contents, first-page/no-preference rule, completed-result rule, and preservation of raw PagingState APIs. The neighboring prepared raw API returns (QueryResult, PagingStateResponse) and marks execution as manual at scylla/src/client/session.rs:922-939.",
      "fairness": "Prompt-stated",
      "name": "prepared_and_cached_manual_apis_carry_opaque_continuations — prepared continuation and legacy API",
      "qualityCheck": "Fair and behaviorally useful. The state assertion is permissive (>=1), so it verifies carriage but not absence of duplicate state-bearing attempts.",
      "verifies": "For Session::execute_single_page_with_affinity, page one returns Some continuation; page two uses the same coordinator, forwards state [31] at least once, calls the policy hook once, and returns None. The legacy execute_single_page call still succeeds."
    },
    {
      "concerns": [],
      "evidence": "Tracing, metrics, and speculative execution are prompt-stated. The additional exact history shape is repository-discoverable: statement history listeners are public execution configuration (scylla/src/statement/prepared.rs:645-649); RequestExecutionParams carries statement history plus speculative policy (scylla/src/client/execution.rs:90-115,140-159); one history request is opened per run and speculative fibers are separately logged (scylla/src/client/execution.rs:414-445); and StructuredHistory exposes requests/speculative_fibers (scylla/src/observability/history.rs:263-282).",
      "fairness": "Repo-discoverable",
      "name": "prepared_and_cached_manual_apis_carry_opaque_continuations — prepared execution features",
      "qualityCheck": "Fair integration check that the new wrapper stays on the common execution path. The delayed-response/zero-interval orchestration is noted as a shared timing concern in the overall assessment.",
      "verifies": "A completed prepared affinity call returns no continuation, exposes a tracing ID, increments the manually-paged request metric by at least one, creates exactly one structured-history request with exactly one speculative fiber, and succeeds under a one-retry zero-delay speculative policy."
    },
    {
      "concerns": [],
      "evidence": "The prompt explicitly names the caching-session affinity method and continuation semantics and requires retaining raw APIs. The pre-existing caching raw API prepares through the cache and delegates to Session::execute_single_page (scylla/src/client/caching_session.rs:118-136), making the tested integration point predictable.",
      "fairness": "Prompt-stated",
      "name": "prepared_and_cached_manual_apis_carry_opaque_continuations — caching continuation and legacy API",
      "qualityCheck": "Fair coverage of the caching wrapper. As in the prepared branch, the >=1 state assertion does not reject duplicate transmissions.",
      "verifies": "For CachingSession::execute_single_page_with_affinity, page one returns Some continuation; page two uses the same coordinator, forwards state [31] at least once, calls the hook once, and returns None. The legacy CachingSession::execute_single_page call still succeeds."
    },
    {
      "concerns": [],
      "evidence": "The prompt explicitly requires metrics, tracing, and speculation preservation. The exact history behavior follows the repository's wrapper convention: CachingSession delegates execution to Session (scylla/src/client/caching_session.rs:98-136), and Session's common execution parameters preserve history and speculative policy (scylla/src/client/execution.rs:122-159), with one request record and separately logged speculative fibers (scylla/src/client/execution.rs:414-445).",
      "fairness": "Repo-discoverable",
      "name": "prepared_and_cached_manual_apis_carry_opaque_continuations — caching execution features",
      "qualityCheck": "Fair and appropriately checks the wrapper rather than only Session. It shares the suite's delay-based speculative-execution timing concern.",
      "verifies": "A completed caching-session affinity call returns no continuation, exposes a tracing ID, increments the underlying session's manually-paged metric by at least one, and records exactly one history request with exactly one speculative fiber."
    },
    {
      "concerns": [],
      "evidence": "The prompt requires asking the active policy before every later page and says only an eligible preferred target is attempted before a fresh plan. Therefore a newly rejected target must not bypass the fresh rotating plan.",
      "fairness": "Prompt-stated",
      "name": "rejected_custom_policy_hint_falls_back_to_the_fresh_plan",
      "qualityCheck": "Cleanly distinguishes dynamic policy gating from unconditional stickiness.",
      "verifies": "After page one succeeds while affinity is allowed, changing the custom policy to reject affinity causes page two to use a different host from the fresh rotating plan; completion returns None and the hook was called exactly once."
    },
    {
      "concerns": [],
      "evidence": "The prompt explicitly covers automatic paging, requires a policy query \"before every later page,\" requires current routing/cluster state, and permits affinity only while the previous coordinator remains eligible. Three pages imply two checks. The old pager's unconditional stability path is visible at scylla/src/client/pager.rs:301-359, while successful later pages replace stable_coordinator with the actual winner at scylla/src/client/pager.rs:470-485, so the integration location and winner behavior were discoverable.",
      "fairness": "Prompt-stated",
      "name": "automatic_paging_consults_the_same_policy_hook",
      "qualityCheck": "Strong multi-branch coverage of acceptance, rejection, prepared/unprepared automatic paging, and live topology changes. The prepared branch checks stability but does not independently assert its hook-call count.",
      "verifies": "For automatic unprepared paging with affinity allowed, exactly three row markers are returned, all from one server, and the hook is called twice; automatic prepared paging also returns three equal server markers. With affinity rejected, three markers are returned with at least one coordinator change and two hook calls. In a three-page topology-change scenario, hook observations are exactly cluster sizes [2,1] and current-membership results [true,false], the policy performs two fresh picks with different host IDs, and all three rows are returned."
    },
    {
      "concerns": [],
      "evidence": "The prompt unambiguously says: \"The trait's default must reject affinity unless a custom policy opts in.\"",
      "fairness": "Prompt-stated",
      "name": "policy_default_rejects_retained_coordinators",
      "qualityCheck": "Directly discriminates a false/default-accept implementation.",
      "verifies": "A custom LoadBalancingPolicy implementation that omits is_coordinator_preferred does not retain page one's coordinator: page two succeeds on a different host and returns no continuation."
    },
    {
      "concerns": [],
      "evidence": "The prompt says \"Retry normally; the target that ultimately succeeds becomes the next preference.\" Existing execution semantics consume the next plan target for RetryNextTarget (scylla/src/client/execution.rs:627), and QueryResult records the successful request coordinator (scylla/src/response/query_result.rs:71-91). The fixture's first failure plus retry success plus next-page success accounts for the asserted 3/2 totals.",
      "fairness": "Prompt-stated",
      "name": "retries_replace_the_next_affinity_hint_with_the_winner",
      "qualityCheck": "Good discriminating test against retaining the initially attempted loser rather than the successful retry target.",
      "verifies": "When the first request attempt fails and RetryNextTarget succeeds elsewhere, page two runs on that successful winner; totals are exactly three attempts and two successes across both pages, and the later affinity check receives exactly that winner."
    },
    {
      "concerns": [],
      "evidence": "The prompt explicitly says to \"Attempt an eligible preferred target once, before a fresh plan\" and to retry normally. The existing Plan contract describes pick followed by fallback and duplicate filtering (scylla/src/policies/load_balancing/mod.rs:133-156; scylla/src/policies/load_balancing/plan.rs:107-159), supporting the concrete attempt accounting.",
      "fairness": "Prompt-stated",
      "name": "failed_preferred_target_is_tried_once_before_fresh_fallback",
      "qualityCheck": "Precisely tests the important once-before-fallback semantics without pinning an error message.",
      "verifies": "After page one establishes a preferred address, page two first tries that address and fails, then succeeds on a different fresh-plan address; total counts are exactly three attempts and two successes, the eligibility hook sees the preferred address once, and the completed result has no continuation."
    },
    {
      "concerns": [],
      "evidence": "The prompt explicitly requires preserving errors, metrics, tracing, and speculative execution. The exact history assertions are supported by the common execution path: RequestExecutionParams carries metrics, speculative policy, timeout, and history listener (scylla/src/client/execution.rs:90-159); run_request_no_side_effects creates one history request and logs speculative fibers (scylla/src/client/execution.rs:414-445); manual request/error counters are selected by RequestPaging::Manual (scylla/src/client/execution.rs:350-373) and exposed at scylla/src/observability/metrics.rs:432-459.",
      "fairness": "Repo-discoverable",
      "name": "affinity_preserves_metrics_tracing_history_speculation_and_errors",
      "qualityCheck": "Fair. Error compatibility is checked only at the variant/discriminant level, which is robust but intentionally shallow. The successful speculation branch shares the suite's delay-based timing concern.",
      "verifies": "An unprepared affinity call returns no continuation, exposes a tracing ID, increments the manual-request metric, and records one history request with one speculative fiber. With server errors, the affinity and legacy raw APIs return errors with the same enum discriminant, and the manual-error metric rises by at least two."
    },
    {
      "concerns": [],
      "evidence": "The prompt states all accepted forms directly: preferred once before a fresh plan, preserve relative order, suppress only the same node and shard for sharded preference, suppress every later target for an unsharded preferred node, and exposes the exact Plan::new_with_preferred_target signature. Existing Plan already preserves fallback order while filtering its picked target (scylla/src/policies/load_balancing/plan.rs:121-159).",
      "fairness": "Prompt-stated",
      "name": "preferred_plan_preserves_order_and_suppresses_only_the_selected_target",
      "qualityCheck": "A strong direct plan test covering sharded, materialized duplicate, unsharded, and no-preference branches. Dry proxy nodes have one materializable shard, avoiding effective RNG variation despite Plan's generic random-shard support.",
      "verifies": "With a sharded preferred target (node 1, shard 7), output is that target followed by the baseline plan in baseline order excluding only that exact pair; with preferred shard 0, that exact pair occurs once; with an unsharded preferred node, the node appears first and all later targets for that host are removed while other baseline hosts retain order; with None preference, output exactly equals Plan::new's baseline."
    },
    {
      "concerns": [],
      "evidence": "The prompt explicitly gives the public module path, all three method signatures, their exact return type, the policy-hook signature, and the preferred-plan constructor signature.",
      "fairness": "Prompt-stated",
      "name": "compile-time public API contracts",
      "qualityCheck": "Appropriate compile-time protection for exact public surface and object safety. It does not by itself prove that PagingContinuation's internals are actually opaque.",
      "verifies": "The integration crate can import scylla::client::paging_continuation::PagingContinuation; all three affinity methods type-check with exact return type Result<(QueryResult, Option<PagingContinuation>), ExecutionError>; and LoadBalancingPolicy::is_coordinator_preferred is callable through &dyn LoadBalancingPolicy with RoutingInfo, ClusterState, and Coordinator."
    }
  ],
  "unfairTestCount": 0,
  "verdict": "PASS"
}
Close