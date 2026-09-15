
Test Quality
Test Quality
VERDICT
FAIL
1 OF 14 UNFAIR
FAIL: 13 behavioral/API test groups are fair, but the rustdoc opacity test contains one unfair co-assertion: it requires PagingContinuation itself to be a struct, although the prompt requires only an opaque public type at that path and the repository permits public type aliases. The rest of the suite closely tracks the unusually detailed prompt. Advisory suite-wide quality note: the integration group relies on local TCP proxy binding and dry-mode cluster discovery; that shared local-network environment assumption is recorded here once rather than repeated on every integration test. Several speculative/latency checks also have the test-specific timing concerns noted above.
UNFAIR TESTS
NOT FAIR
paging_continuation_representation_is_opaque (including rustdoc JSON checker)
Verifies: Rust compilation must allow importing `scylla::client::paging_continuation::PagingContinuation` and passing `None::<PagingContinuation>`. Separately, rustdoc JSON must contain exactly one public item at that path whose kind is specifically `struct`; a plain struct passes only when it has no public fields and reports stripped private fields, and a tuple struct passes only when it has at least one field and every field is private. Enums and public type aliases fail even if they expose no representation and carry the required private state.
Evidence: The public path and opacity/private-state portions are prompt-stated, but the accepted item kind is not. Refutation battery: searched the prompt for `PagingContinuation`, `opaque`, `struct`, `enum`, and type/alias wording; it names the type and calls the continuation opaque but never requires a struct. Searched the repository for `PagingContinuation`, `Continuation`, `opaque`, `pub struct Paging`, `pub enum Paging`, and `has_stripped_fields`; no same-form convention exists. The repo instead demonstrates that public named API types may be aliases at `scylla/src/client/session_builder.rs:45-57`. A public alias/re-export of an opaque private-field carrier is therefore a grounded alternative that satisfies the stated path and opacity but fails the checker solely because rustdoc reports a non-`struct` kind.
Quality: The privacy check is valuable, but coupling it to rustdoc's `kind == struct` and unstable JSON encoding pins an unstated implementation choice and toolchain representation. The checker also depends on nightly/bootstrapped rustdoc JSON details.
INTERNAL COUPLING
ENV ASSUMPTION
REQUIREMENT COVERAGE (16/20 COVERED)
Advisory only — prompt-stated requirements and whether the hidden tests pin them.

COVERED
Automatic and manual paging preserve coordinator affinity while remaining policy-gated.
"Make automatic and manual paging preserve coordinator affinity without bypassing the active load-balancing policy."
manual_unprepared_affinity_is_policy_gated_and_preserves_raw_api, prepared_and_cached_manual_apis_carry_opaque_continuations, automatic_paging_consults_the_same_policy_hook
PARTIAL
Before every later page, re-check the preceding successful coordinator using current routing and cluster state.
"Before every later page, ask that policy whether the preceding page's successful coordinator remains eligible under the current routing and cluster state."
manual_unprepared_affinity_is_policy_gated_and_preserves_raw_api, automatic_paging_consults_the_same_policy_hook
COVERED
The trait default rejects affinity unless overridden.
"The trait's default must reject affinity unless a custom policy opts in."
policy_default_rejects_retained_coordinators
PARTIAL
Default policy accepts only a current, enabled, connected local replica for the routed token/table that passes active filters.
"The default policy accepts only the current enabled, connected local replica for the routed token and table when that target passes its active filters."
default_policy_coordinator_eligibility_matrix, paging_affinity_real_host_filter_rejects_coordinator, paging_affinity_latency_penalized_coordinator_is_rejected
COVERED
Default policy rejects all explicitly named ineligible categories and unknown replica eligibility.
"Reject remote, non-replica, removed, replaced, disabled, disconnected, and filtered targets, and reject when replica eligibility cannot be established."
default_policy_coordinator_eligibility_matrix, paging_affinity_real_host_filter_rejects_coordinator, paging_affinity_latency_penalized_coordinator_is_rejected
COVERED
An eligible preferred target is attempted once before a fresh plan.
"Attempt an eligible preferred target once, before a fresh plan."
failed_preferred_target_is_tried_once_before_fresh_fallback, preferred_plan_preserves_order_and_suppresses_only_the_selected_target
COVERED
The fresh plan retains its relative order.
"Preserve the fresh plan's relative order."
preferred_plan_preserves_order_and_suppresses_only_the_selected_target
PARTIAL
A sharded preference suppresses only the same node-and-shard target.
"Suppress only the same node and shard for a sharded preference;"
preferred_plan_preserves_order_and_suppresses_only_the_selected_target
COVERED
An unsharded preferred node suppresses all later targets for that node.
"suppress every later target for an unsharded preferred node."
preferred_plan_preserves_order_and_suppresses_only_the_selected_target
PARTIAL
Manual unprepared, prepared, and caching calls use an opaque continuation carrying server state and the preceding successful coordinator.
"Manual unprepared, prepared, and caching-session calls use an opaque continuation containing server paging state and the preceding successful coordinator."
manual_unprepared_affinity_is_policy_gated_and_preserves_raw_api, prepared_and_cached_manual_apis_carry_opaque_continuations, paging_continuation_representation_is_opaque (including rustdoc JSON checker)
COVERED
The first call has no preference.
"The first call has no preference"
manual_unprepared_affinity_is_policy_gated_and_preserves_raw_api, prepared_and_cached_manual_apis_carry_opaque_continuations
COVERED
Completed results return no continuation.
"completed results return no continuation."
manual_unprepared_affinity_is_policy_gated_and_preserves_raw_api, prepared_and_cached_manual_apis_carry_opaque_continuations, rejected_custom_policy_hint_falls_back_to_the_fresh_plan
COVERED
Retries remain normal and the successful retry target becomes the next preference.
"Retry normally; the target that ultimately succeeds becomes the next preference."
retries_replace_the_next_affinity_hint_with_the_winner, failed_preferred_target_is_tried_once_before_fresh_fallback
COVERED
Legacy raw PagingState APIs and errors, metrics, tracing, and speculative execution are preserved.
"Preserve legacy raw `PagingState` APIs, errors, metrics, tracing, and speculative execution."
manual_unprepared_affinity_is_policy_gated_and_preserves_raw_api, prepared_and_cached_manual_apis_carry_opaque_continuations, affinity_preserves_metrics_tracing_history_speculation_and_errors
COVERED
Expose the unprepared Session affinity-aware method.
"`Session::query_single_page_with_affinity(statement, values, Option<PagingContinuation>)`."
compile-time public API contracts (exact_affinity_return_types and public_contracts), manual_unprepared_affinity_is_policy_gated_and_preserves_raw_api
COVERED
Expose the prepared Session affinity-aware method.
"`Session::execute_single_page_with_affinity(prepared, values, Option<PagingContinuation>)`."
compile-time public API contracts (exact_affinity_return_types and public_contracts), prepared_and_cached_manual_apis_carry_opaque_continuations
COVERED
Expose the CachingSession affinity-aware method.
"`CachingSession::execute_single_page_with_affinity(statement, values, Option<PagingContinuation>)`."
compile-time public API contracts (exact_affinity_return_types and public_contracts), prepared_and_cached_manual_apis_carry_opaque_continuations
COVERED
All three methods return the exact stated Result tuple.
"Each returns `Result<(QueryResult, Option<PagingContinuation>), ExecutionError>`."
compile-time public API contracts (exact_affinity_return_types and public_contracts)
COVERED
Expose the policy eligibility hook with the stated signature.
"`LoadBalancingPolicy::is_coordinator_preferred(&self, &RoutingInfo, &ClusterState, &Coordinator) -> bool`."
compile-time public API contracts (exact_affinity_return_types and public_contracts), policy_default_rejects_retained_coordinators
COVERED
Expose the preferred-target Plan constructor with the stated signature.
"`Plan::new_with_preferred_target(&dyn LoadBalancingPolicy, &RoutingInfo, &ClusterState, Option<(NodeRef, Option<Shard>)>) -> Plan`."
compile-time public API contracts (exact_affinity_return_types and public_contracts), preferred_plan_preserves_order_and_suppresses_only_the_selected_target
COVERAGE SUGGESTIONS (5)
Advisory only — these don't affect the check result.

Current routing re-evaluation
NOT DISCRIMINATING
PROMPT-STATED
Requirement: Before every later page, re-check the preceding successful coordinator using current routing and cluster state.
Resume a continuation while changing the statement/serialized partition-key values so a custom policy can assert that the later hook receives newly computed RoutingInfo rather than routing cached from the preceding page. The existing topology mutation covers current ClusterState but not the independent current-routing clause.
Default-policy generality across routing points
SINGLE POINT
PROMPT-STATED
Requirement: Default policy accepts only a current, enabled, connected local replica for the routed token/table that passes active filters.
Repeat positive and negative eligibility checks with a second token and table whose replica/shard assignment differs. This would prevent an implementation special-cased to token 160/TABLE_NTS_RF_2 from satisfying the matrix.
Nonzero explicit sharded suppression
SINGLE POINT
PROMPT-STATED
Requirement: A sharded preference suppresses only the same node-and-shard target.
Use ExplicitShardPolicy with both `(preferred_node, shard 1)` and `(preferred_node, shard 0)`, prefer shard 1, and assert shard 1 is emitted once while shard 0 remains in relative order. The current duplicate-shard assertion only exercises materialized shard 0.
End-to-end shard retention in manual continuation
NOT DISCRIMINATING
PROMPT-STATED
Requirement: Manual unprepared, prepared, and caching calls use an opaque continuation carrying server state and the preceding successful coordinator.
Use a sharded coordinator fixture and verify that a later manual call prefers the exact preceding node and shard, not merely the same node. A continuation implementation that stores server state plus node but drops the coordinator's shard would pass the current end-to-end tests.
Policy rejection for automatic prepared paging
NOT DISCRIMINATING
PROMPT-STATED
Requirement: Automatic and manual paging preserve coordinator affinity while remaining policy-gated.
Add an execute_iter branch whose policy rejects the preceding coordinator and assert that the coordinator changes and the hook is called for every later page. The current prepared automatic branch only uses an accepting policy, so unconditional prepared-page pinning could pass it.
QUALITY NOTES (13)
PROMPT-STATED
default_policy_coordinator_eligibility_matrix
Fair and unusually broad across the named rejection categories. It nevertheless uses only one concrete routed token/table pair, so a special case for that pair could evade the intended general rule.
OVERFIT
PROMPT-STATED
paging_affinity_real_host_filter_rejects_coordinator
Fair, but largely redundant with the host-filter case in the larger eligibility matrix and again exercises only one routing point.
OVERFIT
PROMPT-STATED
paging_affinity_latency_penalized_coordinator_is_rejected
Fair and directly checks that affinity does not bypass latency awareness. It uses `Instant::now()` and an asynchronous updater, and it checks only one penalized routing case.
TIMING
OVERFIT
PROMPT-STATED
manual_unprepared_affinity_is_policy_gated_and_preserves_raw_api
Fair and discriminating: three pages prove that the policy is consulted repeatedly rather than only once. Coordinator equality is mainly checked via connection address in this proxy scenario, which is narrower than host-id-plus-shard identity but does not make the test unfair.
PROMPT-STATED
prepared_and_cached_manual_apis_carry_opaque_continuations
Fair and comprehensive across both APIs. The speculative assertions depend on fixed response delays to ensure the extra fiber starts before either request completes.
TIMING
PROMPT-STATED
rejected_custom_policy_hint_falls_back_to_the_fresh_plan
Fair and directly distinguishes policy-gated affinity from unconditional coordinator pinning.
PROMPT-STATED
automatic_paging_consults_the_same_policy_hook
Fair and strong for unprepared automatic paging, including dynamic topology. The prepared automatic branch only tests acceptance, so unconditional prepared-page pinning would not be caught by that branch alone.
PROMPT-STATED
policy_default_rejects_retained_coordinators
Fair and specifically protects backward-compatible behavior for policies that do not opt in.
PROMPT-STATED
retries_replace_the_next_affinity_hint_with_the_winner
Fair and discriminates the successful coordinator from the initially attempted coordinator.
PROMPT-STATED
failed_preferred_target_is_tried_once_before_fresh_fallback
Fair and directly checks both the once-only rule and fallback behavior.
PROMPT-STATED
affinity_preserves_metrics_tracing_history_speculation_and_errors
Fair and compares the new and legacy error categories without brittle message matching. The speculative-count portion uses fixed 100 ms response delays, so it has some scheduler/timing sensitivity.
TIMING
PROMPT-STATED
preferred_plan_preserves_order_and_suppresses_only_the_selected_target
Fair and checks both raw explicit shards and shard materialization. The only duplicate-sharded suppression case uses materialized shard 0, so a shard-0 special case could pass that portion.
OVERFIT
PROMPT-STATED
compile-time public API contracts (exact_affinity_return_types and public_contracts)
Fair compile-time contract checking; it pins public API surface rather than implementation internals.
TASK SUMMARY
The task adds policy-gated coordinator affinity to both automatic paging and three new manual single-page APIs. A continuation must carry the server paging state plus the coordinator that actually won the preceding page; before each later page, the active load-balancing policy must re-evaluate that coordinator against current routing/topology. Eligible preferences are tried once ahead of an otherwise unchanged fresh plan. The built-in policy must conservatively accept only a current, connected, enabled, local replica on the routed shard that also passes active host/latency filters; the trait default rejects. Existing raw PagingState APIs and execution behavior (retry, metrics, tracing, history, speculative execution, and errors) must remain intact. The prompt also fixes the public module path, method signatures, return type, policy hook, and preferred-plan constructor.
Completed in 371.6s

Hide raw output
{
  "completed": true,
  "coverageSuggestions": [
    {
      "area": "Current routing re-evaluation",
      "gapKind": "not_discriminating",
      "requirement": "Before every later page, re-check the preceding successful coordinator using current routing and cluster state.",
      "sourceIfAdded": "Prompt-stated",
      "suggestion": "Resume a continuation while changing the statement/serialized partition-key values so a custom policy can assert that the later hook receives newly computed RoutingInfo rather than routing cached from the preceding page. The existing topology mutation covers current ClusterState but not the independent current-routing clause."
    },
    {
      "area": "Default-policy generality across routing points",
      "gapKind": "single_point",
      "requirement": "Default policy accepts only a current, enabled, connected local replica for the routed token/table that passes active filters.",
      "sourceIfAdded": "Prompt-stated",
      "suggestion": "Repeat positive and negative eligibility checks with a second token and table whose replica/shard assignment differs. This would prevent an implementation special-cased to token 160/TABLE_NTS_RF_2 from satisfying the matrix."
    },
    {
      "area": "Nonzero explicit sharded suppression",
      "gapKind": "single_point",
      "requirement": "A sharded preference suppresses only the same node-and-shard target.",
      "sourceIfAdded": "Prompt-stated",
      "suggestion": "Use ExplicitShardPolicy with both `(preferred_node, shard 1)` and `(preferred_node, shard 0)`, prefer shard 1, and assert shard 1 is emitted once while shard 0 remains in relative order. The current duplicate-shard assertion only exercises materialized shard 0."
    },
    {
      "area": "End-to-end shard retention in manual continuation",
      "gapKind": "not_discriminating",
      "requirement": "Manual unprepared, prepared, and caching calls use an opaque continuation carrying server state and the preceding successful coordinator.",
      "sourceIfAdded": "Prompt-stated",
      "suggestion": "Use a sharded coordinator fixture and verify that a later manual call prefers the exact preceding node and shard, not merely the same node. A continuation implementation that stores server state plus node but drops the coordinator's shard would pass the current end-to-end tests."
    },
    {
      "area": "Policy rejection for automatic prepared paging",
      "gapKind": "not_discriminating",
      "requirement": "Automatic and manual paging preserve coordinator affinity while remaining policy-gated.",
      "sourceIfAdded": "Prompt-stated",
      "suggestion": "Add an execute_iter branch whose policy rejects the preceding coordinator and assert that the coordinator changes and the hook is called for every later page. The current prepared automatic branch only uses an accepting policy, so unconditional prepared-page pinning could pass it."
    }
  ],
  "error": "",
  "executionTimeSeconds": 371.56318,
  "message": "1 test flagged as not fair.",
  "overall": "FAIL: 13 behavioral/API test groups are fair, but the rustdoc opacity test contains one unfair co-assertion: it requires PagingContinuation itself to be a struct, although the prompt requires only an opaque public type at that path and the repository permits public type aliases. The rest of the suite closely tracks the unusually detailed prompt. Advisory suite-wide quality note: the integration group relies on local TCP proxy binding and dry-mode cluster discovery; that shared local-network environment assumption is recorded here once rather than repeated on every integration test. Several speculative/latency checks also have the test-specific timing concerns noted above.",
  "requirements": [
    {
      "covered": "yes",
      "coveringTests": [
        "manual_unprepared_affinity_is_policy_gated_and_preserves_raw_api",
        "prepared_and_cached_manual_apis_carry_opaque_continuations",
        "automatic_paging_consults_the_same_policy_hook"
      ],
      "requirement": "Automatic and manual paging preserve coordinator affinity while remaining policy-gated.",
      "sourceQuote": "Make automatic and manual paging preserve coordinator affinity without bypassing the active load-balancing policy."
    },
    {
      "covered": "partial",
      "coveringTests": [
        "manual_unprepared_affinity_is_policy_gated_and_preserves_raw_api",
        "automatic_paging_consults_the_same_policy_hook"
      ],
      "requirement": "Before every later page, re-check the preceding successful coordinator using current routing and cluster state.",
      "sourceQuote": "Before every later page, ask that policy whether the preceding page's successful coordinator remains eligible under the current routing and cluster state."
    },
    {
      "covered": "yes",
      "coveringTests": [
        "policy_default_rejects_retained_coordinators"
      ],
      "requirement": "The trait default rejects affinity unless overridden.",
      "sourceQuote": "The trait's default must reject affinity unless a custom policy opts in."
    },
    {
      "covered": "partial",
      "coveringTests": [
        "default_policy_coordinator_eligibility_matrix",
        "paging_affinity_real_host_filter_rejects_coordinator",
        "paging_affinity_latency_penalized_coordinator_is_rejected"
      ],
      "requirement": "Default policy accepts only a current, enabled, connected local replica for the routed token/table that passes active filters.",
      "sourceQuote": "The default policy accepts only the current enabled, connected local replica for the routed token and table when that target passes its active filters."
    },
    {
      "covered": "yes",
      "coveringTests": [
        "default_policy_coordinator_eligibility_matrix",
        "paging_affinity_real_host_filter_rejects_coordinator",
        "paging_affinity_latency_penalized_coordinator_is_rejected"
      ],
      "requirement": "Default policy rejects all explicitly named ineligible categories and unknown replica eligibility.",
      "sourceQuote": "Reject remote, non-replica, removed, replaced, disabled, disconnected, and filtered targets, and reject when replica eligibility cannot be established."
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
      "requirement": "The fresh plan retains its relative order.",
      "sourceQuote": "Preserve the fresh plan's relative order."
    },
    {
      "covered": "partial",
      "coveringTests": [
        "preferred_plan_preserves_order_and_suppresses_only_the_selected_target"
      ],
      "requirement": "A sharded preference suppresses only the same node-and-shard target.",
      "sourceQuote": "Suppress only the same node and shard for a sharded preference;"
    },
    {
      "covered": "yes",
      "coveringTests": [
        "preferred_plan_preserves_order_and_suppresses_only_the_selected_target"
      ],
      "requirement": "An unsharded preferred node suppresses all later targets for that node.",
      "sourceQuote": "suppress every later target for an unsharded preferred node."
    },
    {
      "covered": "partial",
      "coveringTests": [
        "manual_unprepared_affinity_is_policy_gated_and_preserves_raw_api",
        "prepared_and_cached_manual_apis_carry_opaque_continuations",
        "paging_continuation_representation_is_opaque (including rustdoc JSON checker)"
      ],
      "requirement": "Manual unprepared, prepared, and caching calls use an opaque continuation carrying server state and the preceding successful coordinator.",
      "sourceQuote": "Manual unprepared, prepared, and caching-session calls use an opaque continuation containing server paging state and the preceding successful coordinator."
    },
    {
      "covered": "yes",
      "coveringTests": [
        "manual_unprepared_affinity_is_policy_gated_and_preserves_raw_api",
        "prepared_and_cached_manual_apis_carry_opaque_continuations"
      ],
      "requirement": "The first call has no preference.",
      "sourceQuote": "The first call has no preference"
    },
    {
      "covered": "yes",
      "coveringTests": [
        "manual_unprepared_affinity_is_policy_gated_and_preserves_raw_api",
        "prepared_and_cached_manual_apis_carry_opaque_continuations",
        "rejected_custom_policy_hint_falls_back_to_the_fresh_plan"
      ],
      "requirement": "Completed results return no continuation.",
      "sourceQuote": "completed results return no continuation."
    },
    {
      "covered": "yes",
      "coveringTests": [
        "retries_replace_the_next_affinity_hint_with_the_winner",
        "failed_preferred_target_is_tried_once_before_fresh_fallback"
      ],
      "requirement": "Retries remain normal and the successful retry target becomes the next preference.",
      "sourceQuote": "Retry normally; the target that ultimately succeeds becomes the next preference."
    },
    {
      "covered": "yes",
      "coveringTests": [
        "manual_unprepared_affinity_is_policy_gated_and_preserves_raw_api",
        "prepared_and_cached_manual_apis_carry_opaque_continuations",
        "affinity_preserves_metrics_tracing_history_speculation_and_errors"
      ],
      "requirement": "Legacy raw PagingState APIs and errors, metrics, tracing, and speculative execution are preserved.",
      "sourceQuote": "Preserve legacy raw `PagingState` APIs, errors, metrics, tracing, and speculative execution."
    },
    {
      "covered": "yes",
      "coveringTests": [
        "compile-time public API contracts (exact_affinity_return_types and public_contracts)",
        "manual_unprepared_affinity_is_policy_gated_and_preserves_raw_api"
      ],
      "requirement": "Expose the unprepared Session affinity-aware method.",
      "sourceQuote": "`Session::query_single_page_with_affinity(statement, values, Option<PagingContinuation>)`."
    },
    {
      "covered": "yes",
      "coveringTests": [
        "compile-time public API contracts (exact_affinity_return_types and public_contracts)",
        "prepared_and_cached_manual_apis_carry_opaque_continuations"
      ],
      "requirement": "Expose the prepared Session affinity-aware method.",
      "sourceQuote": "`Session::execute_single_page_with_affinity(prepared, values, Option<PagingContinuation>)`."
    },
    {
      "covered": "yes",
      "coveringTests": [
        "compile-time public API contracts (exact_affinity_return_types and public_contracts)",
        "prepared_and_cached_manual_apis_carry_opaque_continuations"
      ],
      "requirement": "Expose the CachingSession affinity-aware method.",
      "sourceQuote": "`CachingSession::execute_single_page_with_affinity(statement, values, Option<PagingContinuation>)`."
    },
    {
      "covered": "yes",
      "coveringTests": [
        "compile-time public API contracts (exact_affinity_return_types and public_contracts)"
      ],
      "requirement": "All three methods return the exact stated Result tuple.",
      "sourceQuote": "Each returns `Result<(QueryResult, Option<PagingContinuation>), ExecutionError>`."
    },
    {
      "covered": "yes",
      "coveringTests": [
        "compile-time public API contracts (exact_affinity_return_types and public_contracts)",
        "policy_default_rejects_retained_coordinators"
      ],
      "requirement": "Expose the policy eligibility hook with the stated signature.",
      "sourceQuote": "`LoadBalancingPolicy::is_coordinator_preferred(&self, &RoutingInfo, &ClusterState, &Coordinator) -> bool`."
    },
    {
      "covered": "yes",
      "coveringTests": [
        "compile-time public API contracts (exact_affinity_return_types and public_contracts)",
        "preferred_plan_preserves_order_and_suppresses_only_the_selected_target"
      ],
      "requirement": "Expose the preferred-target Plan constructor with the stated signature.",
      "sourceQuote": "`Plan::new_with_preferred_target(&dyn LoadBalancingPolicy, &RoutingInfo, &ClusterState, Option<(NodeRef, Option<Shard>)>) -> Plan`."
    }
  ],
  "taskSummary": "The task adds policy-gated coordinator affinity to both automatic paging and three new manual single-page APIs. A continuation must carry the server paging state plus the coordinator that actually won the preceding page; before each later page, the active load-balancing policy must re-evaluate that coordinator against current routing/topology. Eligible preferences are tried once ahead of an otherwise unchanged fresh plan. The built-in policy must conservatively accept only a current, connected, enabled, local replica on the routed shard that also passes active host/latency filters; the trait default rejects. Existing raw PagingState APIs and execution behavior (retry, metrics, tracing, history, speculative execution, and errors) must remain intact. The prompt also fixes the public module path, method signatures, return type, policy hook, and preferred-plan constructor.",
  "tests": [
    {
      "concerns": [
        "overfit_single_point"
      ],
      "evidence": "The prompt explicitly says the default policy accepts only the current enabled, connected local replica for the routed token/table when active filters pass, and explicitly rejects remote, non-replica, removed, replaced, disabled, disconnected, filtered, and unestablishable targets. The different-shard check is also supported by the prompt's node-and-shard suppression language and by the repository's replica locator returning `(node, shard)` targets at `scylla/src/policies/load_balancing/default.rs:621-634`. The non-preferred-rack positive form is discoverable from `scylla/src/policies/load_balancing/default.rs:1017-1022`, which says rack preference orders local-rack replicas before other replicas in the same DC rather than excluding the latter.",
      "fairness": "Prompt-stated",
      "name": "default_policy_coordinator_eligibility_matrix",
      "qualityCheck": "Fair and unusually broad across the named rejection categories. It nevertheless uses only one concrete routed token/table pair, so a special case for that pair could evade the intended general rule.",
      "verifies": "For token 160 and TABLE_NTS_RF_2, the test accepts `true` for the current connected local replica both unsharded and on its routed shard; `false` for the same node on a different shard, a remote replica both with and without DC failover, a local non-replica, missing token, missing table, unknown schema, a removed old node, a replaced old node object, a host-filter-disabled node, and a disconnected node. It also requires a same-DC replica in a non-preferred rack to remain eligible."
    },
    {
      "concerns": [
        "overfit_single_point"
      ],
      "evidence": "The prompt explicitly requires filtered and disabled targets to be rejected. Existing default-policy planning filters enabled nodes at `scylla/src/policies/load_balancing/default.rs:451-464`.",
      "fairness": "Prompt-stated",
      "name": "paging_affinity_real_host_filter_rejects_coordinator",
      "qualityCheck": "Fair, but largely redundant with the host-filter case in the larger eligibility matrix and again exercises only one routing point.",
      "verifies": "With the real ClusterState metadata path and a HostFilter rejecting the port-1 peer, `DefaultPolicy::is_coordinator_preferred` must return `false` for that disabled local replica at token 160/TABLE_NTS_RF_2."
    },
    {
      "concerns": [
        "timing_sensitivity",
        "overfit_single_point"
      ],
      "evidence": "The prompt says the target must pass active filters and filtered targets must be rejected. The repository specifically defines the active pick predicate as connectivity plus the latency predicate and says penalized nodes are never picked at `scylla/src/policies/load_balancing/default.rs:109-123`.",
      "fairness": "Prompt-stated",
      "name": "paging_affinity_latency_penalized_coordinator_is_rejected",
      "qualityCheck": "Fair and directly checks that affinity does not bypass latency awareness. It uses `Instant::now()` and an asynchronous updater, and it checks only one penalized routing case.",
      "verifies": "After latency statistics make node A much slower than node C and the latency updater runs, the policy hook must return `false` for node A at token 160/TABLE_NTS_RF_2."
    },
    {
      "concerns": [],
      "evidence": "These accepted forms directly follow the prompt clauses requiring no first-call preference, a policy check before every later page, continuation carriage of server state and preceding successful coordinator, no continuation on completion, rejection when replica eligibility cannot be established, and preservation of raw PagingState APIs. The existing raw API and return form are visible at `scylla/src/client/session.rs:745-753`, while QueryResult exposes the successful coordinator at `scylla/src/response/query_result.rs:140-148`.",
      "fairness": "Prompt-stated",
      "name": "manual_unprepared_affinity_is_policy_gated_and_preserves_raw_api",
      "qualityCheck": "Fair and discriminating: three pages prove that the policy is consulted repeatedly rather than only once. Coordinator equality is mainly checked via connection address in this proxy scenario, which is narrower than host-id-plus-shard identity but does not make the test unfair.",
      "verifies": "The first affinity-aware unprepared call produces a continuation without consulting the hook; two later calls consult it with the immediately preceding coordinators, stay on the first successful coordinator while allowed, transmit paging states `[11]` and `[12]` exactly once each, and return `None` after the last page. The test also requires DefaultPolicy to reject affinity when routing has neither token nor table, and requires the legacy `query_single_page(..., PagingState::start())` API still to return `HasMorePages`."
    },
    {
      "concerns": [
        "timing_sensitivity"
      ],
      "evidence": "The prompt explicitly names both methods, the `Option<PagingContinuation>` lifecycle, coordinator retention, and preservation of raw APIs, metrics, tracing, and speculative execution. Exact metric accounting follows the existing execution path: each actual attempt increments the manual counter at `scylla/src/client/execution.rs:519-551`, and the configured speculative policy has one extra execution because `max_retry_count` excludes the initial request (`scylla/src/policies/speculative_execution.rs:38-55`). Existing caching delegation to prepared single-page execution is visible at `scylla/src/client/caching_session.rs:124-137`.",
      "fairness": "Prompt-stated",
      "name": "prepared_and_cached_manual_apis_carry_opaque_continuations",
      "qualityCheck": "Fair and comprehensive across both APIs. The speculative assertions depend on fixed response delays to ensure the extra fiber starts before either request completes.",
      "verifies": "For both Session prepared execution and CachingSession execution, the first affinity-aware page must return `Some`, increment manually-paged request metrics by exactly 1, and the resumed page must use the same coordinator, invoke the hook once, send paging state `[31]` at least once, and return `None`; each corresponding legacy raw PagingState API must still succeed. In each API's traced/speculative subcase, two page calls must each return a tracing ID, end with no continuation, increase manually-paged attempt metrics by exactly 4 total, produce exactly two history requests, and record exactly one speculative fiber per request."
    },
    {
      "concerns": [],
      "evidence": "The prompt explicitly requires checking eligibility before a later page and, when the preference is not eligible, using a fresh active-policy plan. The custom rotating policy makes the fresh plan's next host concrete in the test setup.",
      "fairness": "Prompt-stated",
      "name": "rejected_custom_policy_hint_falls_back_to_the_fresh_plan",
      "qualityCheck": "Fair and directly distinguishes policy-gated affinity from unconditional coordinator pinning.",
      "verifies": "After page one succeeds and the custom policy is changed to reject affinity, page two must finish with no continuation, use a different host selected by the rotating fresh plan, and call the eligibility hook exactly once."
    },
    {
      "concerns": [],
      "evidence": "The prompt explicitly applies affinity to automatic paging, requires a policy check before every later page, and requires the current cluster state. The repository already stores the successful automatic-page coordinator after each page at `scylla/src/client/pager.rs:386-395` and `scylla/src/client/pager.rs:475-485`, making that coordinator the discoverable input to the new hook. Plan laziness, which explains why an accepted preferred page need not perform a fresh pick, is documented at `scylla/src/policies/load_balancing/plan.rs:16-20`.",
      "fairness": "Prompt-stated",
      "name": "automatic_paging_consults_the_same_policy_hook",
      "qualityCheck": "Fair and strong for unprepared automatic paging, including dynamic topology. The prepared automatic branch only tests acceptance, so unconditional prepared-page pinning would not be caught by that branch alone.",
      "verifies": "For automatic unprepared paging with an accepting policy, exactly three returned marker rows must all come from one proxy node, the hook must be called twice, and history must contain three requests. Automatic prepared paging must likewise yield three equal node markers. With a rejecting policy, exactly three markers must include at least one coordinator change and the hook must be called twice. In the topology-mutation branch, the two hook calls must observe cluster sizes `[2, 1]` and current-membership results `[true, false]`; only two fresh picks may occur, and those picks must be different host IDs."
    },
    {
      "concerns": [],
      "evidence": "The prompt explicitly says the trait default must reject affinity unless a custom policy opts in. The repository trait is designed with default no-op extension methods, as visible around `scylla/src/policies/load_balancing/mod.rs:158-188`, so adding a defaulted hook is also integration-compatible with existing custom policies.",
      "fairness": "Prompt-stated",
      "name": "policy_default_rejects_retained_coordinators",
      "qualityCheck": "Fair and specifically protects backward-compatible behavior for policies that do not opt in.",
      "verifies": "A custom LoadBalancingPolicy that does not override the new hook must return no continuation after page two and must use different host IDs for pages one and two under its rotating plan."
    },
    {
      "concerns": [],
      "evidence": "The prompt explicitly says to retry normally and that the target which ultimately succeeds becomes the next preference. Existing execution constructs the result coordinator from the successful attempt at `scylla/src/client/execution.rs:563-579`, supporting the exact winner used by the assertion.",
      "fairness": "Prompt-stated",
      "name": "retries_replace_the_next_affinity_hint_with_the_winner",
      "qualityCheck": "Fair and discriminates the successful coordinator from the initially attempted coordinator.",
      "verifies": "When the first page's first attempt fails and its retry succeeds elsewhere, page two must use that successful coordinator; there must be exactly 3 total attempts, 2 successes, and the sole later-page eligibility check must receive exactly the first page's winning connection address."
    },
    {
      "concerns": [],
      "evidence": "The prompt explicitly requires an eligible preferred target to be attempted once before a fresh plan, while preserving normal retry behavior. The repository's execution loop advances through plan targets under RetryNextTarget at `scylla/src/client/execution.rs:515-610`, so the exact 1-success + 1-failed-preference + 1-fresh-success count follows from the visible setup.",
      "fairness": "Prompt-stated",
      "name": "failed_preferred_target_is_tried_once_before_fresh_fallback",
      "qualityCheck": "Fair and directly checks both the once-only rule and fallback behavior.",
      "verifies": "On page two, an eligible preferred coordinator must be checked once and attempted once; after that attempt fails, execution must succeed on a different fresh-plan coordinator. Across both pages there must be exactly 3 attempts and 2 successes, and the final continuation must be `None`."
    },
    {
      "concerns": [
        "timing_sensitivity"
      ],
      "evidence": "The prompt explicitly requires preservation of errors, metrics, tracing, and speculative execution. Existing code increments manual request/error metrics by request kind at `scylla/src/client/execution.rs:351-373` and per actual attempt at `scylla/src/client/execution.rs:545-593`; tracing IDs are established observable QueryResult state at `scylla/src/response/query_result.rs:75-93`; and speculative history fibers are created by the existing executor at `scylla/src/client/execution.rs:415-434`.",
      "fairness": "Prompt-stated",
      "name": "affinity_preserves_metrics_tracing_history_speculation_and_errors",
      "qualityCheck": "Fair and compares the new and legacy error categories without brittle message matching. The speculative-count portion uses fixed 100 ms response delays, so it has some scheduler/timing sensitivity.",
      "verifies": "Across two successful affinity-aware unprepared pages under one configured speculative retry per request, both QueryResults must have tracing IDs, the final continuation must be `None`, manually-paged attempt metrics must rise by exactly 4, history must contain exactly 2 requests, and each request must contain exactly 1 speculative fiber. In the error subcase, the first page must return `Some` and add exactly 1 manual request; then an affinity-aware failure and a legacy raw PagingState failure must have the same ExecutionError discriminant and together add exactly 2 manual errors."
    },
    {
      "concerns": [
        "overfit_single_point"
      ],
      "evidence": "The prompt explicitly fixes all of these forms: preferred once before the fresh plan, unchanged relative order, exact node-and-shard suppression for sharded preferences, all-target suppression for an unsharded node, and an optional preferred target. Existing Plan semantics materialize unknown shards before yielding at `scylla/src/policies/load_balancing/plan.rs:96-111` and preserve fallback iteration order while filtering at `scylla/src/policies/load_balancing/plan.rs:135-161`.",
      "fairness": "Prompt-stated",
      "name": "preferred_plan_preserves_order_and_suppresses_only_the_selected_target",
      "qualityCheck": "Fair and checks both raw explicit shards and shard materialization. The only duplicate-sharded suppression case uses materialized shard 0, so a shard-0 special case could pass that portion.",
      "verifies": "With a sharded preference `(node[1], 7)`, iteration must emit that pair first and then the baseline plan in its original order minus only that exact pair. A materialized `(node[1], 0)` preference must occur exactly once even when a fresh unsharded target materializes to shard 0. With an unsharded preference, the preferred node must be first and every later occurrence of that node must be removed, including multiple explicit fallback shards, while another node/shard remains. Passing `None` must produce exactly the baseline plan."
    },
    {
      "concerns": [],
      "evidence": "The problem statement spells out the three fully qualified methods, their argument shapes, their exact result type, the policy-hook signature, and the Plan constructor signature verbatim.",
      "fairness": "Prompt-stated",
      "name": "compile-time public API contracts (exact_affinity_return_types and public_contracts)",
      "qualityCheck": "Fair compile-time contract checking; it pins public API surface rather than implementation internals.",
      "verifies": "The crate must publicly expose all three named affinity-aware methods such that calls type-check as `Result<(QueryResult, Option<PagingContinuation>), ExecutionError>`, and a `dyn LoadBalancingPolicy` must expose `is_coordinator_preferred(&RoutingInfo, &ClusterState, &Coordinator) -> bool`. The integration calls also require `Plan::new_with_preferred_target` with the stated optional `(NodeRef, Option<Shard>)` input."
    },
    {
      "concerns": [
        "internal_coupling",
        "environment_assumption"
      ],
      "evidence": "The public path and opacity/private-state portions are prompt-stated, but the accepted item kind is not. Refutation battery: searched the prompt for `PagingContinuation`, `opaque`, `struct`, `enum`, and type/alias wording; it names the type and calls the continuation opaque but never requires a struct. Searched the repository for `PagingContinuation`, `Continuation`, `opaque`, `pub struct Paging`, `pub enum Paging`, and `has_stripped_fields`; no same-form convention exists. The repo instead demonstrates that public named API types may be aliases at `scylla/src/client/session_builder.rs:45-57`. A public alias/re-export of an opaque private-field carrier is therefore a grounded alternative that satisfies the stated path and opacity but fails the checker solely because rustdoc reports a non-`struct` kind.",
      "fairness": "Not fair",
      "name": "paging_continuation_representation_is_opaque (including rustdoc JSON checker)",
      "qualityCheck": "The privacy check is valuable, but coupling it to rustdoc's `kind == struct` and unstable JSON encoding pins an unstated implementation choice and toolchain representation. The checker also depends on nightly/bootstrapped rustdoc JSON details.",
      "verifies": "Rust compilation must allow importing `scylla::client::paging_continuation::PagingContinuation` and passing `None::<PagingContinuation>`. Separately, rustdoc JSON must contain exactly one public item at that path whose kind is specifically `struct`; a plain struct passes only when it has no public fields and reports stripped private fields, and a tuple struct passes only when it has at least one field and every field is private. Enums and public type aliases fail even if they expose no representation and carry the required private state."
    }
  ],
  "unfairTestCount": 1,
  "verdict": "FAIL"
}
Close