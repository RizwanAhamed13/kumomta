
Test Quality
Test Quality
VERDICT
FAIL
1 OF 14 UNFAIR
FAIL: 13 reviewed test units are fair, but the rustdoc opacity test contains one unfair representation constraint, so unfairTestCount is 1. The behavioral suite is otherwise unusually well aligned with the detailed prompt and existing execution machinery. Advisory suite-wide environment note: integration tests assume the harness can bind multiple loopback proxy nodes, and the opacity check assumes Python 3 plus unstable rustdoc JSON/RUSTC_BOOTSTRAP; these are harness environment assumptions affecting groups of tests rather than test-specific fairness findings.
UNFAIR TESTS
NOT FAIR
paging_continuation_representation_is_opaque
Verifies: The public type can be passed as Option<PagingContinuation>. In addition, the rustdoc checker requires exactly one public item at scylla::client::paging_continuation::PagingContinuation, requires its rustdoc kind to be a plain (named-field) struct, requires no public fields, and requires at least one stripped private representation field.
Evidence: The public path and opacity are prompt-stated, but the assertion specifically accepts only rustdoc's `plain` struct form. Refutation battery: searched the problem text for “PagingContinuation”, “opaque”, “struct”, “plain”, and “fields”; it names the type and opacity but never says named-field/plain struct. Searched the repo for `Continuation`, `opaque`, `has_stripped_fields`, `pub struct PagingState`, and `pub enum PagingState` across source/tests/docs. There is no continuation convention or rustdoc-shape checker; the closest visible paging abstraction is the equally valid opaque tuple struct `pub struct PagingState(Option<Arc<[u8]>>)` at scylla-cql-core/src/frame/request/query.rs:57-63. A solver could naturally implement `pub struct PagingContinuation(PagingState, Coordinator);`, satisfying the public path, hidden representation, and required contents, but rustdoc reports tuple rather than plain and the checker rejects it. Thus the hidden test pins the author's representation choice.
Quality: The no-public-fields and nonempty-private-representation checks are appropriate opacity checks. Requiring rustdoc `plain` rather than accepting an opaque tuple struct is unnecessary representation coupling.
INTERNAL COUPLING
REQUIREMENT COVERAGE (29/33 COVERED)
Advisory only — prompt-stated requirements and whether the hidden tests pin them.

COVERED
Automatic and manual paging retain coordinator affinity without bypassing the active load-balancing policy.
"Make automatic and manual paging preserve coordinator affinity without bypassing the active load-balancing policy."
manual_unprepared_affinity_is_policy_gated_and_preserves_raw_api, prepared_and_cached_manual_apis_carry_opaque_continuations, automatic_paging_consults_the_same_policy_hook
PARTIAL
Before each page after the first, query the policy about the preceding successful coordinator using current routing and cluster state.
"Before every later page, ask that policy whether the preceding page's successful coordinator remains eligible under the current routing and cluster state."
manual_unprepared_affinity_is_policy_gated_and_preserves_raw_api, automatic_paging_consults_the_same_policy_hook, rejected_custom_policy_hint_falls_back_to_the_fresh_plan
COVERED
The trait default rejects affinity unless a policy overrides it.
"The trait's default must reject affinity unless a custom policy opts in."
policy_default_rejects_retained_coordinators, compile-time affinity API contracts
COVERED
DefaultPolicy accepts the current enabled, connected local replica for the routed token/table when active filters pass.
"The default policy accepts only the current enabled, connected local replica for the routed token and table when that target passes its active filters."
default_policy_coordinator_eligibility_matrix
COVERED
DefaultPolicy rejects remote targets.
"Reject remote, non-replica, removed, replaced, disabled, disconnected, and filtered targets, and reject when replica eligibility cannot be established."
default_policy_coordinator_eligibility_matrix
COVERED
DefaultPolicy rejects non-replicas.
"Reject remote, non-replica, removed, replaced, disabled, disconnected, and filtered targets, and reject when replica eligibility cannot be established."
default_policy_coordinator_eligibility_matrix
COVERED
DefaultPolicy rejects removed targets.
"Reject remote, non-replica, removed, replaced, disabled, disconnected, and filtered targets, and reject when replica eligibility cannot be established."
default_policy_coordinator_eligibility_matrix
COVERED
DefaultPolicy rejects replaced targets.
"Reject remote, non-replica, removed, replaced, disabled, disconnected, and filtered targets, and reject when replica eligibility cannot be established."
default_policy_coordinator_eligibility_matrix
COVERED
DefaultPolicy rejects disabled targets.
"Reject remote, non-replica, removed, replaced, disabled, disconnected, and filtered targets, and reject when replica eligibility cannot be established."
default_policy_coordinator_eligibility_matrix, paging_affinity_real_host_filter_rejects_coordinator
COVERED
DefaultPolicy rejects disconnected targets.
"Reject remote, non-replica, removed, replaced, disabled, disconnected, and filtered targets, and reject when replica eligibility cannot be established."
default_policy_coordinator_eligibility_matrix
COVERED
DefaultPolicy rejects targets filtered by active host or latency filters.
"Reject remote, non-replica, removed, replaced, disabled, disconnected, and filtered targets, and reject when replica eligibility cannot be established."
paging_affinity_real_host_filter_rejects_coordinator, paging_affinity_latency_penalized_coordinator_is_rejected
COVERED
DefaultPolicy rejects when replica eligibility cannot be established.
"Reject remote, non-replica, removed, replaced, disabled, disconnected, and filtered targets, and reject when replica eligibility cannot be established."
default_policy_coordinator_eligibility_matrix, manual_unprepared_affinity_is_policy_gated_and_preserves_raw_api
COVERED
Try an eligible preferred target exactly once before using a fresh plan.
"Attempt an eligible preferred target once, before a fresh plan."
failed_preferred_target_is_tried_once_before_fresh_fallback, preferred_plan_preserves_order_and_suppresses_only_the_selected_target
COVERED
Preserve the fresh plan's relative order.
"Preserve the fresh plan's relative order."
preferred_plan_preserves_order_and_suppresses_only_the_selected_target
COVERED
For a sharded preference, suppress only the identical node+shard later in the plan.
"Suppress only the same node and shard for a sharded preference; suppress every later target for an unsharded preferred node."
preferred_plan_preserves_order_and_suppresses_only_the_selected_target
COVERED
For an unsharded preferred node, suppress every later target on that node.
"Suppress only the same node and shard for a sharded preference; suppress every later target for an unsharded preferred node."
preferred_plan_preserves_order_and_suppresses_only_the_selected_target
COVERED
Manual unprepared, prepared, and caching-session calls use an opaque continuation carrying server paging state and the prior successful coordinator.
"Manual unprepared, prepared, and caching-session calls use an opaque continuation containing server paging state and the preceding successful coordinator."
manual_unprepared_affinity_is_policy_gated_and_preserves_raw_api, prepared_and_cached_manual_apis_carry_opaque_continuations, paging_continuation_representation_is_opaque
COVERED
The first manual affinity call has no preferred coordinator.
"The first call has no preference and completed results return no continuation."
manual_unprepared_affinity_is_policy_gated_and_preserves_raw_api, prepared_and_cached_manual_apis_carry_opaque_continuations
COVERED
Completed manual results return no continuation.
"The first call has no preference and completed results return no continuation."
manual_unprepared_affinity_is_policy_gated_and_preserves_raw_api, prepared_and_cached_manual_apis_carry_opaque_continuations
PARTIAL
Manual affinity calls retain normal retry behavior.
"Retry normally; the target that ultimately succeeds becomes the next preference."
retries_replace_the_next_affinity_hint_with_the_winner, failed_preferred_target_is_tried_once_before_fresh_fallback
PARTIAL
The target that ultimately succeeds becomes the next preference.
"Retry normally; the target that ultimately succeeds becomes the next preference."
retries_replace_the_next_affinity_hint_with_the_winner
COVERED
Legacy raw PagingState APIs remain available and functional.
"Preserve legacy raw `PagingState` APIs, errors, metrics, tracing, and speculative execution."
manual_unprepared_affinity_is_policy_gated_and_preserves_raw_api, prepared_and_cached_manual_apis_carry_opaque_continuations
PARTIAL
Existing error behavior is preserved.
"Preserve legacy raw `PagingState` APIs, errors, metrics, tracing, and speculative execution."
affinity_preserves_metrics_tracing_history_speculation_and_errors
COVERED
Existing metrics behavior is preserved.
"Preserve legacy raw `PagingState` APIs, errors, metrics, tracing, and speculative execution."
prepared_and_cached_manual_apis_carry_opaque_continuations, affinity_preserves_metrics_tracing_history_speculation_and_errors
COVERED
Existing tracing behavior is preserved.
"Preserve legacy raw `PagingState` APIs, errors, metrics, tracing, and speculative execution."
prepared_and_cached_manual_apis_carry_opaque_continuations, affinity_preserves_metrics_tracing_history_speculation_and_errors
COVERED
Existing speculative execution behavior is preserved.
"Preserve legacy raw `PagingState` APIs, errors, metrics, tracing, and speculative execution."
prepared_and_cached_manual_apis_carry_opaque_continuations, affinity_preserves_metrics_tracing_history_speculation_and_errors
COVERED
Expose PagingContinuation at the specified public module path.
"Expose `scylla::client::paging_continuation::PagingContinuation` and the following affinity-aware single-page methods:"
compile-time affinity API contracts, paging_continuation_representation_is_opaque
COVERED
Expose Session::query_single_page_with_affinity with the specified parameters.
"- `Session::query_single_page_with_affinity(statement, values, Option<PagingContinuation>)`."
compile-time affinity API contracts, manual_unprepared_affinity_is_policy_gated_and_preserves_raw_api
COVERED
Expose Session::execute_single_page_with_affinity with the specified parameters.
"- `Session::execute_single_page_with_affinity(prepared, values, Option<PagingContinuation>)`."
compile-time affinity API contracts, prepared_and_cached_manual_apis_carry_opaque_continuations
COVERED
Expose CachingSession::execute_single_page_with_affinity with the specified parameters.
"- `CachingSession::execute_single_page_with_affinity(statement, values, Option<PagingContinuation>)`."
compile-time affinity API contracts, prepared_and_cached_manual_apis_carry_opaque_continuations
COVERED
All three affinity-aware methods return the exact stated Result tuple.
"Each returns `Result<(QueryResult, Option<PagingContinuation>), ExecutionError>`."
compile-time affinity API contracts
COVERED
Expose LoadBalancingPolicy::is_coordinator_preferred with the exact stated signature.
"- `LoadBalancingPolicy::is_coordinator_preferred(&self, &RoutingInfo, &ClusterState, &Coordinator) -> bool`."
compile-time affinity API contracts, policy_default_rejects_retained_coordinators
COVERED
Expose Plan::new_with_preferred_target with the exact stated signature.
"- `Plan::new_with_preferred_target(&dyn LoadBalancingPolicy, &RoutingInfo, &ClusterState, Option<(NodeRef, Option<Shard>)>) -> Plan`."
preferred_plan_preserves_order_and_suppresses_only_the_selected_target
COVERAGE SUGGESTIONS (4)
Advisory only — these don't affect the check result.

Current routing refresh between pages
NOT DISCRIMINATING
PROMPT-STATED
Requirement: Before each page after the first, query the policy about the preceding successful coordinator using current routing and cluster state.
Add a scenario where routing/schema information visible to the policy changes after page one, and assert that the later-page eligibility hook sees the refreshed routing rather than a snapshot. The current test refreshes cluster membership but not routing metadata, so an implementation that snapshots RoutingInfo could pass.
Automatic prepared paging rejection
NOT DISCRIMINATING
PROMPT-STATED
Requirement: Automatic and manual paging retain coordinator affinity without bypassing the active load-balancing policy.
Add execute_iter with a policy that rejects affinity and assert a coordinator change plus one hook call per later page. Present tests allow affinity for prepared automatic paging but only exercise rejection for query_iter, so an execute-only shortcut that bypasses the hook could pass.
Retries for prepared and caching manual APIs
NOT DISCRIMINATING
PROMPT-STATED
Requirement: Manual affinity calls retain normal retry behavior.
Inject a retriable first-attempt failure separately into Session prepared and CachingSession affinity calls, then verify normal retry and that the ultimate winner is carried in the next continuation. Current retry tests cover only the unprepared affinity method.
Error preservation for prepared and caching APIs
NOT DISCRIMINATING
PROMPT-STATED
Requirement: Existing error behavior is preserved.
Exercise failing affinity continuations for prepared and caching-session methods and compare their public error variants and manual error metrics with the corresponding raw PagingState APIs. A wrapper that maps errors only in those two new methods currently passes.
QUALITY NOTES (13)
REPO-DISCOVERABLE
default_policy_coordinator_eligibility_matrix
Comprehensive matrix with direct boolean assertions. It appropriately distinguishes rack ordering from eligibility and exercises unavailable routing/schema. The removed/replaced fixtures couple to topology identity only to construct the prompt-required public scenario, not to prescribe the solution implementation.
PROMPT-STATED
paging_affinity_real_host_filter_rejects_coordinator
Fair but substantially redundant with the disabled/host-filter branch of the eligibility matrix; its value is confirming construction through the real metadata/filter path.
REPO-DISCOVERABLE
paging_affinity_latency_penalized_coordinator_is_rejected
A focused check of one active dynamic filter. It uses explicit latency values and minimum measurement count, so the penalization state is controlled.
PROMPT-STATED
manual_unprepared_affinity_is_policy_gated_and_preserves_raw_api
Strong end-to-end test: it checks policy gating, coordinator behavior, actual wire paging states, completion, and legacy compatibility. Exact hook count follows the three-page setup and “before every later page.”
REPO-DISCOVERABLE
prepared_and_cached_manual_apis_carry_opaque_continuations
Broad and discriminating across prepared and cache wrappers, though long and somewhat repetitive. The exact +4 and one-fiber assertions correctly pin preservation of existing telemetry/speculation behavior under the configured two pages and two fibers per page.
PROMPT-STATED
rejected_custom_policy_hint_falls_back_to_the_fresh_plan
Clear dynamic-policy test that would fail an implementation which captured eligibility only on the first page.
REPO-DISCOVERABLE
automatic_paging_consults_the_same_policy_hook
Excellent coverage of allow, deny, prepared/unprepared automatic execution, per-page hook count, history, and topology refresh. The prepared branch checks acceptance but not rejection; that is a coverage gap, not an unfair present assertion.
PROMPT-STATED
policy_default_rejects_retained_coordinators
Direct behavioral check of the default trait method rather than merely a compile-time existence check.
PROMPT-STATED
retries_replace_the_next_affinity_hint_with_the_winner
The exact counts are fully determined by one injected first-attempt failure, one retry, and one successful next page. This catches retaining the initially attempted rather than ultimately successful coordinator.
PROMPT-STATED
failed_preferred_target_is_tried_once_before_fresh_fallback
Precisely discriminates a single preferred attempt from repeatedly reinserting the preference or abandoning normal fallback.
REPO-DISCOVERABLE
affinity_preserves_metrics_tracing_history_speculation_and_errors
Broad regression check. Comparing only error discriminants is intentionally tolerant of details, while exact telemetry counts ensure affinity does not bypass the established execution core.
PROMPT-STATED
preferred_plan_preserves_order_and_suppresses_only_the_selected_target
Strong direct API test covering exact-shard, materialized duplicate, unsharded multi-shard suppression, relative order, and no-preference identity. Proxy setup is unnecessary for this pure plan assertion but does not alter its fairness.
PROMPT-STATED
compile-time affinity API contracts
Although implemented as dead helper functions rather than named tests, Rust type-checks them, so they are effective and exact compile-time API assertions.
TASK SUMMARY
Implement policy-gated coordinator affinity for automatic and manual paging. Every page after the first must ask the active load-balancing policy whether the preceding successful coordinator is still eligible using current routing/topology. The policy trait defaults to rejection; DefaultPolicy accepts only a current, enabled, connected, local routed replica that passes filters. An accepted preference is tried once before a newly generated plan, with precise node/shard de-duplication. Add opaque manual continuations and three exact public single-page APIs while retaining raw PagingState behavior and existing retries, errors, metrics, tracing, and speculation.
Completed in 177.2s

Hide raw output
{
  "completed": true,
  "coverageSuggestions": [
    {
      "area": "Current routing refresh between pages",
      "gapKind": "not_discriminating",
      "requirement": "Before each page after the first, query the policy about the preceding successful coordinator using current routing and cluster state.",
      "sourceIfAdded": "Prompt-stated",
      "suggestion": "Add a scenario where routing/schema information visible to the policy changes after page one, and assert that the later-page eligibility hook sees the refreshed routing rather than a snapshot. The current test refreshes cluster membership but not routing metadata, so an implementation that snapshots RoutingInfo could pass."
    },
    {
      "area": "Automatic prepared paging rejection",
      "gapKind": "not_discriminating",
      "requirement": "Automatic and manual paging retain coordinator affinity without bypassing the active load-balancing policy.",
      "sourceIfAdded": "Prompt-stated",
      "suggestion": "Add execute_iter with a policy that rejects affinity and assert a coordinator change plus one hook call per later page. Present tests allow affinity for prepared automatic paging but only exercise rejection for query_iter, so an execute-only shortcut that bypasses the hook could pass."
    },
    {
      "area": "Retries for prepared and caching manual APIs",
      "gapKind": "not_discriminating",
      "requirement": "Manual affinity calls retain normal retry behavior.",
      "sourceIfAdded": "Prompt-stated",
      "suggestion": "Inject a retriable first-attempt failure separately into Session prepared and CachingSession affinity calls, then verify normal retry and that the ultimate winner is carried in the next continuation. Current retry tests cover only the unprepared affinity method."
    },
    {
      "area": "Error preservation for prepared and caching APIs",
      "gapKind": "not_discriminating",
      "requirement": "Existing error behavior is preserved.",
      "sourceIfAdded": "Prompt-stated",
      "suggestion": "Exercise failing affinity continuations for prepared and caching-session methods and compare their public error variants and manual error metrics with the corresponding raw PagingState APIs. A wrapper that maps errors only in those two new methods currently passes."
    }
  ],
  "error": "",
  "executionTimeSeconds": 177.199384,
  "message": "1 test flagged as not fair.",
  "overall": "FAIL: 13 reviewed test units are fair, but the rustdoc opacity test contains one unfair representation constraint, so unfairTestCount is 1. The behavioral suite is otherwise unusually well aligned with the detailed prompt and existing execution machinery. Advisory suite-wide environment note: integration tests assume the harness can bind multiple loopback proxy nodes, and the opacity check assumes Python 3 plus unstable rustdoc JSON/RUSTC_BOOTSTRAP; these are harness environment assumptions affecting groups of tests rather than test-specific fairness findings.",
  "requirements": [
    {
      "covered": "yes",
      "coveringTests": [
        "manual_unprepared_affinity_is_policy_gated_and_preserves_raw_api",
        "prepared_and_cached_manual_apis_carry_opaque_continuations",
        "automatic_paging_consults_the_same_policy_hook"
      ],
      "requirement": "Automatic and manual paging retain coordinator affinity without bypassing the active load-balancing policy.",
      "sourceQuote": "Make automatic and manual paging preserve coordinator affinity without bypassing the active load-balancing policy."
    },
    {
      "covered": "partial",
      "coveringTests": [
        "manual_unprepared_affinity_is_policy_gated_and_preserves_raw_api",
        "automatic_paging_consults_the_same_policy_hook",
        "rejected_custom_policy_hint_falls_back_to_the_fresh_plan"
      ],
      "requirement": "Before each page after the first, query the policy about the preceding successful coordinator using current routing and cluster state.",
      "sourceQuote": "Before every later page, ask that policy whether the preceding page's successful coordinator remains eligible under the current routing and cluster state."
    },
    {
      "covered": "yes",
      "coveringTests": [
        "policy_default_rejects_retained_coordinators",
        "compile-time affinity API contracts"
      ],
      "requirement": "The trait default rejects affinity unless a policy overrides it.",
      "sourceQuote": "The trait's default must reject affinity unless a custom policy opts in."
    },
    {
      "covered": "yes",
      "coveringTests": [
        "default_policy_coordinator_eligibility_matrix"
      ],
      "requirement": "DefaultPolicy accepts the current enabled, connected local replica for the routed token/table when active filters pass.",
      "sourceQuote": "The default policy accepts only the current enabled, connected local replica for the routed token and table when that target passes its active filters."
    },
    {
      "covered": "yes",
      "coveringTests": [
        "default_policy_coordinator_eligibility_matrix"
      ],
      "requirement": "DefaultPolicy rejects remote targets.",
      "sourceQuote": "Reject remote, non-replica, removed, replaced, disabled, disconnected, and filtered targets, and reject when replica eligibility cannot be established."
    },
    {
      "covered": "yes",
      "coveringTests": [
        "default_policy_coordinator_eligibility_matrix"
      ],
      "requirement": "DefaultPolicy rejects non-replicas.",
      "sourceQuote": "Reject remote, non-replica, removed, replaced, disabled, disconnected, and filtered targets, and reject when replica eligibility cannot be established."
    },
    {
      "covered": "yes",
      "coveringTests": [
        "default_policy_coordinator_eligibility_matrix"
      ],
      "requirement": "DefaultPolicy rejects removed targets.",
      "sourceQuote": "Reject remote, non-replica, removed, replaced, disabled, disconnected, and filtered targets, and reject when replica eligibility cannot be established."
    },
    {
      "covered": "yes",
      "coveringTests": [
        "default_policy_coordinator_eligibility_matrix"
      ],
      "requirement": "DefaultPolicy rejects replaced targets.",
      "sourceQuote": "Reject remote, non-replica, removed, replaced, disabled, disconnected, and filtered targets, and reject when replica eligibility cannot be established."
    },
    {
      "covered": "yes",
      "coveringTests": [
        "default_policy_coordinator_eligibility_matrix",
        "paging_affinity_real_host_filter_rejects_coordinator"
      ],
      "requirement": "DefaultPolicy rejects disabled targets.",
      "sourceQuote": "Reject remote, non-replica, removed, replaced, disabled, disconnected, and filtered targets, and reject when replica eligibility cannot be established."
    },
    {
      "covered": "yes",
      "coveringTests": [
        "default_policy_coordinator_eligibility_matrix"
      ],
      "requirement": "DefaultPolicy rejects disconnected targets.",
      "sourceQuote": "Reject remote, non-replica, removed, replaced, disabled, disconnected, and filtered targets, and reject when replica eligibility cannot be established."
    },
    {
      "covered": "yes",
      "coveringTests": [
        "paging_affinity_real_host_filter_rejects_coordinator",
        "paging_affinity_latency_penalized_coordinator_is_rejected"
      ],
      "requirement": "DefaultPolicy rejects targets filtered by active host or latency filters.",
      "sourceQuote": "Reject remote, non-replica, removed, replaced, disabled, disconnected, and filtered targets, and reject when replica eligibility cannot be established."
    },
    {
      "covered": "yes",
      "coveringTests": [
        "default_policy_coordinator_eligibility_matrix",
        "manual_unprepared_affinity_is_policy_gated_and_preserves_raw_api"
      ],
      "requirement": "DefaultPolicy rejects when replica eligibility cannot be established.",
      "sourceQuote": "Reject remote, non-replica, removed, replaced, disabled, disconnected, and filtered targets, and reject when replica eligibility cannot be established."
    },
    {
      "covered": "yes",
      "coveringTests": [
        "failed_preferred_target_is_tried_once_before_fresh_fallback",
        "preferred_plan_preserves_order_and_suppresses_only_the_selected_target"
      ],
      "requirement": "Try an eligible preferred target exactly once before using a fresh plan.",
      "sourceQuote": "Attempt an eligible preferred target once, before a fresh plan."
    },
    {
      "covered": "yes",
      "coveringTests": [
        "preferred_plan_preserves_order_and_suppresses_only_the_selected_target"
      ],
      "requirement": "Preserve the fresh plan's relative order.",
      "sourceQuote": "Preserve the fresh plan's relative order."
    },
    {
      "covered": "yes",
      "coveringTests": [
        "preferred_plan_preserves_order_and_suppresses_only_the_selected_target"
      ],
      "requirement": "For a sharded preference, suppress only the identical node+shard later in the plan.",
      "sourceQuote": "Suppress only the same node and shard for a sharded preference; suppress every later target for an unsharded preferred node."
    },
    {
      "covered": "yes",
      "coveringTests": [
        "preferred_plan_preserves_order_and_suppresses_only_the_selected_target"
      ],
      "requirement": "For an unsharded preferred node, suppress every later target on that node.",
      "sourceQuote": "Suppress only the same node and shard for a sharded preference; suppress every later target for an unsharded preferred node."
    },
    {
      "covered": "yes",
      "coveringTests": [
        "manual_unprepared_affinity_is_policy_gated_and_preserves_raw_api",
        "prepared_and_cached_manual_apis_carry_opaque_continuations",
        "paging_continuation_representation_is_opaque"
      ],
      "requirement": "Manual unprepared, prepared, and caching-session calls use an opaque continuation carrying server paging state and the prior successful coordinator.",
      "sourceQuote": "Manual unprepared, prepared, and caching-session calls use an opaque continuation containing server paging state and the preceding successful coordinator."
    },
    {
      "covered": "yes",
      "coveringTests": [
        "manual_unprepared_affinity_is_policy_gated_and_preserves_raw_api",
        "prepared_and_cached_manual_apis_carry_opaque_continuations"
      ],
      "requirement": "The first manual affinity call has no preferred coordinator.",
      "sourceQuote": "The first call has no preference and completed results return no continuation."
    },
    {
      "covered": "yes",
      "coveringTests": [
        "manual_unprepared_affinity_is_policy_gated_and_preserves_raw_api",
        "prepared_and_cached_manual_apis_carry_opaque_continuations"
      ],
      "requirement": "Completed manual results return no continuation.",
      "sourceQuote": "The first call has no preference and completed results return no continuation."
    },
    {
      "covered": "partial",
      "coveringTests": [
        "retries_replace_the_next_affinity_hint_with_the_winner",
        "failed_preferred_target_is_tried_once_before_fresh_fallback"
      ],
      "requirement": "Manual affinity calls retain normal retry behavior.",
      "sourceQuote": "Retry normally; the target that ultimately succeeds becomes the next preference."
    },
    {
      "covered": "partial",
      "coveringTests": [
        "retries_replace_the_next_affinity_hint_with_the_winner"
      ],
      "requirement": "The target that ultimately succeeds becomes the next preference.",
      "sourceQuote": "Retry normally; the target that ultimately succeeds becomes the next preference."
    },
    {
      "covered": "yes",
      "coveringTests": [
        "manual_unprepared_affinity_is_policy_gated_and_preserves_raw_api",
        "prepared_and_cached_manual_apis_carry_opaque_continuations"
      ],
      "requirement": "Legacy raw PagingState APIs remain available and functional.",
      "sourceQuote": "Preserve legacy raw `PagingState` APIs, errors, metrics, tracing, and speculative execution."
    },
    {
      "covered": "partial",
      "coveringTests": [
        "affinity_preserves_metrics_tracing_history_speculation_and_errors"
      ],
      "requirement": "Existing error behavior is preserved.",
      "sourceQuote": "Preserve legacy raw `PagingState` APIs, errors, metrics, tracing, and speculative execution."
    },
    {
      "covered": "yes",
      "coveringTests": [
        "prepared_and_cached_manual_apis_carry_opaque_continuations",
        "affinity_preserves_metrics_tracing_history_speculation_and_errors"
      ],
      "requirement": "Existing metrics behavior is preserved.",
      "sourceQuote": "Preserve legacy raw `PagingState` APIs, errors, metrics, tracing, and speculative execution."
    },
    {
      "covered": "yes",
      "coveringTests": [
        "prepared_and_cached_manual_apis_carry_opaque_continuations",
        "affinity_preserves_metrics_tracing_history_speculation_and_errors"
      ],
      "requirement": "Existing tracing behavior is preserved.",
      "sourceQuote": "Preserve legacy raw `PagingState` APIs, errors, metrics, tracing, and speculative execution."
    },
    {
      "covered": "yes",
      "coveringTests": [
        "prepared_and_cached_manual_apis_carry_opaque_continuations",
        "affinity_preserves_metrics_tracing_history_speculation_and_errors"
      ],
      "requirement": "Existing speculative execution behavior is preserved.",
      "sourceQuote": "Preserve legacy raw `PagingState` APIs, errors, metrics, tracing, and speculative execution."
    },
    {
      "covered": "yes",
      "coveringTests": [
        "compile-time affinity API contracts",
        "paging_continuation_representation_is_opaque"
      ],
      "requirement": "Expose PagingContinuation at the specified public module path.",
      "sourceQuote": "Expose `scylla::client::paging_continuation::PagingContinuation` and the following affinity-aware single-page methods:"
    },
    {
      "covered": "yes",
      "coveringTests": [
        "compile-time affinity API contracts",
        "manual_unprepared_affinity_is_policy_gated_and_preserves_raw_api"
      ],
      "requirement": "Expose Session::query_single_page_with_affinity with the specified parameters.",
      "sourceQuote": "- `Session::query_single_page_with_affinity(statement, values, Option<PagingContinuation>)`."
    },
    {
      "covered": "yes",
      "coveringTests": [
        "compile-time affinity API contracts",
        "prepared_and_cached_manual_apis_carry_opaque_continuations"
      ],
      "requirement": "Expose Session::execute_single_page_with_affinity with the specified parameters.",
      "sourceQuote": "- `Session::execute_single_page_with_affinity(prepared, values, Option<PagingContinuation>)`."
    },
    {
      "covered": "yes",
      "coveringTests": [
        "compile-time affinity API contracts",
        "prepared_and_cached_manual_apis_carry_opaque_continuations"
      ],
      "requirement": "Expose CachingSession::execute_single_page_with_affinity with the specified parameters.",
      "sourceQuote": "- `CachingSession::execute_single_page_with_affinity(statement, values, Option<PagingContinuation>)`."
    },
    {
      "covered": "yes",
      "coveringTests": [
        "compile-time affinity API contracts"
      ],
      "requirement": "All three affinity-aware methods return the exact stated Result tuple.",
      "sourceQuote": "Each returns `Result<(QueryResult, Option<PagingContinuation>), ExecutionError>`."
    },
    {
      "covered": "yes",
      "coveringTests": [
        "compile-time affinity API contracts",
        "policy_default_rejects_retained_coordinators"
      ],
      "requirement": "Expose LoadBalancingPolicy::is_coordinator_preferred with the exact stated signature.",
      "sourceQuote": "- `LoadBalancingPolicy::is_coordinator_preferred(&self, &RoutingInfo, &ClusterState, &Coordinator) -> bool`."
    },
    {
      "covered": "yes",
      "coveringTests": [
        "preferred_plan_preserves_order_and_suppresses_only_the_selected_target"
      ],
      "requirement": "Expose Plan::new_with_preferred_target with the exact stated signature.",
      "sourceQuote": "- `Plan::new_with_preferred_target(&dyn LoadBalancingPolicy, &RoutingInfo, &ClusterState, Option<(NodeRef, Option<Shard>)>) -> Plan`."
    }
  ],
  "taskSummary": "Implement policy-gated coordinator affinity for automatic and manual paging. Every page after the first must ask the active load-balancing policy whether the preceding successful coordinator is still eligible using current routing/topology. The policy trait defaults to rejection; DefaultPolicy accepts only a current, enabled, connected, local routed replica that passes filters. An accepted preference is tried once before a newly generated plan, with precise node/shard de-duplication. Add opaque manual continuations and three exact public single-page APIs while retaining raw PagingState behavior and existing retries, errors, metrics, tracing, and speculation.",
  "tests": [
    {
      "concerns": [],
      "evidence": "The prompt explicitly lists the accepted local/enabled/connected/replica/filter conditions and all rejected categories. The exact rack and shard interpretation is also visible in DefaultPolicy: it falls through from rack replicas to same-DC replicas at scylla/src/policies/load_balancing/default.rs:181-221 and scylla/src/policies/load_balancing/default.rs:330-375, resolves replicas with node+shard at scylla/src/policies/load_balancing/default.rs:620-634, applies active liveness/latency predicates at scylla/src/policies/load_balancing/default.rs:111-121, and exposes current node identity at scylla/src/cluster/state.rs:500-507.",
      "fairness": "Repo-discoverable",
      "name": "default_policy_coordinator_eligibility_matrix",
      "qualityCheck": "Comprehensive matrix with direct boolean assertions. It appropriately distinguishes rack ordering from eligibility and exercises unavailable routing/schema. The removed/replaced fixtures couple to topology identity only to construct the prompt-required public scenario, not to prescribe the solution implementation.",
      "verifies": "For token 160 and TABLE_NTS_RF_2 in preferred DC eu, the policy returns true for the connected local replica with no shard and with its routed shard; false for the same node with a different shard, a remote replica even when DC failover is permitted, and a local non-replica; true for a same-DC replica outside the preferred rack; false when token or table is absent, schema is unknown, the old node is removed or replaced in current topology, the node is host-filter-disabled, or its pool is disconnected."
    },
    {
      "concerns": [],
      "evidence": "The prompt explicitly says the default policy must reject “disabled” and “filtered targets.” The repository documents that a host-filtered node has no pool at scylla/src/cluster/node.rs:91-95 and that such a node is disabled at scylla/src/cluster/node.rs:227-231.",
      "fairness": "Prompt-stated",
      "name": "paging_affinity_real_host_filter_rejects_coordinator",
      "qualityCheck": "Fair but substantially redundant with the disabled/host-filter branch of the eligibility matrix; its value is confirming construction through the real metadata/filter path.",
      "verifies": "DefaultPolicy returns false for the routed local replica when the cluster's real HostFilter rejected that peer, even after test connectivity is enabled."
    },
    {
      "concerns": [],
      "evidence": "The prompt requires preferred targets to pass the policy's active filters. The repository specifically identifies latency penalization as an active pick filter: scylla/src/policies/load_balancing/default.rs:111-121 says penalized nodes are never picked, and scylla/src/policies/load_balancing/default.rs:959-968 composes latency_predicate with is_alive. Thus the exact latency-filter case is discoverable rather than an unstated choice.",
      "fairness": "Repo-discoverable",
      "name": "paging_affinity_latency_penalized_coordinator_is_rejected",
      "qualityCheck": "A focused check of one active dynamic filter. It uses explicit latency values and minimum measurement count, so the penalization state is controlled.",
      "verifies": "After latency statistics make node A much slower than node C and the latency updater runs, DefaultPolicy::is_coordinator_preferred returns false for A under valid token/table routing."
    },
    {
      "concerns": [],
      "evidence": "The prompt explicitly requires a first call with no preference, a policy check before every later page, affinity to the preceding successful coordinator, server paging state in the continuation, no continuation on completion, default rejection when replica eligibility is unavailable, and preservation of raw PagingState APIs. Existing raw API shape is visible at scylla/src/client/session.rs:693-752, and Coordinator identifies its node/shard at scylla/src/response/coordinator.rs:9-24.",
      "fairness": "Prompt-stated",
      "name": "manual_unprepared_affinity_is_policy_gated_and_preserves_raw_api",
      "qualityCheck": "Strong end-to-end test: it checks policy gating, coordinator behavior, actual wire paging states, completion, and legacy compatibility. Exact hook count follows the three-page setup and “before every later page.”",
      "verifies": "The first affinity-aware query page yields a continuation; DefaultPolicy rejects that coordinator when routing cannot establish replica eligibility; pages two and three call the custom hook exactly once each with the preceding page addresses, reuse the first coordinator across all three successful pages, transmit paging states [11] and [12] exactly once, and return None after page three. The legacy query_single_page call still returns PagingStateResponse::HasMorePages."
    },
    {
      "concerns": [],
      "evidence": "The prompt explicitly requires these two APIs, opaque state+coordinator continuations, completion semantics, and preservation of raw APIs, metrics, tracing, and speculative execution. The exact pre-existing integration semantics are discoverable: CachingSession delegates single-page work to Session at scylla/src/client/caching_session.rs:124-138; each execution attempt increments the request counter at scylla/src/client/execution.rs:520-552 and manual executions select the manual counter at scylla/src/client/execution.rs:350-372; history creates one request and attaches speculative fibers at scylla/src/observability/history.rs:377-388 and scylla/src/observability/history.rs:428-440.",
      "fairness": "Repo-discoverable",
      "name": "prepared_and_cached_manual_apis_carry_opaque_continuations",
      "qualityCheck": "Broad and discriminating across prepared and cache wrappers, though long and somewhat repetitive. The exact +4 and one-fiber assertions correctly pin preservation of existing telemetry/speculation behavior under the configured two pages and two fibers per page.",
      "verifies": "For both Session prepared execution and CachingSession execution: page one returns Some continuation and increments manual-request metrics by one; page two reuses page one's coordinator, invokes the hook once, transmits state [31] at least once, and returns None. Both legacy raw PagingState methods still succeed. With tracing and one zero-delay speculative retry configured, each API's two affinity pages return tracing IDs, increment manual request metrics by exactly four, create exactly two history requests, and record exactly one speculative fiber per request."
    },
    {
      "concerns": [],
      "evidence": "The prompt says to ask the active policy before every later page and to attempt a preferred target only when eligible, otherwise using a fresh plan. It also says completed results return no continuation.",
      "fairness": "Prompt-stated",
      "name": "rejected_custom_policy_hint_falls_back_to_the_fresh_plan",
      "qualityCheck": "Clear dynamic-policy test that would fail an implementation which captured eligibility only on the first page.",
      "verifies": "After page one succeeds while affinity is allowed, changing the custom hook to false causes exactly one eligibility check on page two, page two succeeds on a different host selected by the fresh plan, and the completed result has no continuation."
    },
    {
      "concerns": [],
      "evidence": "The prompt explicitly covers automatic paging, checks before every later page, active-policy opt-in/rejection, and current cluster state. The precise one-history-request-per-page behavior is repository-visible: PagingExecutor documents that each page traverses full history machinery at scylla/src/client/pager.rs:119-128, and HistoryCollector creates one RequestHistory per NewRequest at scylla/src/observability/history.rs:377-388. Current topology is exposed through ClusterState::get_nodes_info at scylla/src/cluster/state.rs:500-507.",
      "fairness": "Repo-discoverable",
      "name": "automatic_paging_consults_the_same_policy_hook",
      "qualityCheck": "Excellent coverage of allow, deny, prepared/unprepared automatic execution, per-page hook count, history, and topology refresh. The prepared branch checks acceptance but not rejection; that is a coverage gap, not an unfair present assertion.",
      "verifies": "For three automatic unprepared pages with affinity allowed, exactly three row markers are returned, all markers identify the same server, the hook is called twice, and history contains three requests. Three prepared automatic pages likewise all use one server. With affinity denied, three unprepared pages include at least one server change and the hook is still called twice. When a node is removed after page one, hook observations are exactly cluster sizes [2,1] and current-membership results [true,false], the policy picks twice, and the second picked host differs from the first."
    },
    {
      "concerns": [],
      "evidence": "The prompt explicitly states: “The trait's default must reject affinity unless a custom policy opts in.” It also states that completed results return no continuation.",
      "fairness": "Prompt-stated",
      "name": "policy_default_rejects_retained_coordinators",
      "qualityCheck": "Direct behavioral check of the default trait method rather than merely a compile-time existence check.",
      "verifies": "A custom LoadBalancingPolicy implementation that does not override is_coordinator_preferred does not retain page one's host: page two succeeds on a different host and returns no continuation."
    },
    {
      "concerns": [],
      "evidence": "The prompt explicitly says “Retry normally; the target that ultimately succeeds becomes the next preference.” The repository's plan contract explains that fallback supplies targets after a picked target fails at scylla/src/policies/load_balancing/mod.rs:145-156.",
      "fairness": "Prompt-stated",
      "name": "retries_replace_the_next_affinity_hint_with_the_winner",
      "qualityCheck": "The exact counts are fully determined by one injected first-attempt failure, one retry, and one successful next page. This catches retaining the initially attempted rather than ultimately successful coordinator.",
      "verifies": "With the first attempt failing and RetryNextTarget configured, page one ultimately succeeds elsewhere; page two is sent to that winning coordinator. Across both pages there are exactly three attempts and two successes, and the only eligibility-hook argument is the page-one winner address."
    },
    {
      "concerns": [],
      "evidence": "The prompt explicitly requires: “Attempt an eligible preferred target once, before a fresh plan,” “Retry normally,” and no continuation for completed results. Existing fallback-after-pick behavior is documented at scylla/src/policies/load_balancing/mod.rs:145-156.",
      "fairness": "Prompt-stated",
      "name": "failed_preferred_target_is_tried_once_before_fresh_fallback",
      "qualityCheck": "Precisely discriminates a single preferred attempt from repeatedly reinserting the preference or abandoning normal fallback.",
      "verifies": "Page one's coordinator is approved as page two's preference; that preferred page-two attempt fails once, then fresh fallback succeeds on a different address. Total counts are exactly three attempts and two successes, the hook sees the preferred address once, and completion returns no continuation."
    },
    {
      "concerns": [],
      "evidence": "The prompt explicitly requires preservation of errors, metrics, tracing, and speculative execution. Existing exact behavior is discoverable: attempts increment metrics at scylla/src/client/execution.rs:520-552, manual failures use the manual error counter at scylla/src/client/execution.rs:350-372, counter getters are defined at scylla/src/observability/metrics.rs:431-459, and history/speculative fibers are structured at scylla/src/observability/history.rs:377-388 and scylla/src/observability/history.rs:428-440.",
      "fairness": "Repo-discoverable",
      "name": "affinity_preserves_metrics_tracing_history_speculation_and_errors",
      "qualityCheck": "Broad regression check. Comparing only error discriminants is intentionally tolerant of details, while exact telemetry counts ensure affinity does not bypass the established execution core.",
      "verifies": "Across two affinity-aware query pages with one speculative fiber each, both results have tracing IDs, continuation transitions Some to None, manual request metrics increase by exactly four, history has exactly two requests, and each request has one speculative fiber. In a non-speculative run page one increments requests by one; after servers are switched to errors, the affinity API and legacy raw API return errors with the same enum discriminant, and manual error metrics increase by exactly two."
    },
    {
      "concerns": [],
      "evidence": "The prompt explicitly specifies all accepted forms: preferred once before a fresh plan, relative order preserved, same node+shard suppression for a sharded preference, every later target suppression for an unsharded preference, and the exact Plan::new_with_preferred_target signature. The existing Plan iterator's fallback filtering and order are visible at scylla/src/policies/load_balancing/plan.rs:125-169.",
      "fairness": "Prompt-stated",
      "name": "preferred_plan_preserves_order_and_suppresses_only_the_selected_target",
      "qualityCheck": "Strong direct API test covering exact-shard, materialized duplicate, unsharded multi-shard suppression, relative order, and no-preference identity. Proxy setup is unnecessary for this pure plan assertion but does not alter its fairness.",
      "verifies": "With a sharded preferred target (node 1, shard 7), output is that exact target followed by baseline Plan order excluding only that exact pair. A preferred (node 1, shard 0) appears exactly once after materialization. With an unsharded preference, output begins with node 1 and excludes all later targets for node 1; an explicit fallback containing node 1 shards 0 and 1 plus node 0 shard 4 therefore leaves only node 0/shard 4 after the preferred node. Passing None produces exactly the baseline plan."
    },
    {
      "concerns": [],
      "evidence": "The prompt gives the exact module path, all three method signatures, common return type, and exact policy-hook signature. Existing neighboring raw methods establish the generic statement/value style at scylla/src/client/session.rs:745-752, scylla/src/client/session.rs:924-939, and scylla/src/client/caching_session.rs:124-138.",
      "fairness": "Prompt-stated",
      "name": "compile-time affinity API contracts",
      "qualityCheck": "Although implemented as dead helper functions rather than named tests, Rust type-checks them, so they are effective and exact compile-time API assertions.",
      "verifies": "The integration crate type-checks the exact three method result types Result<(QueryResult, Option<PagingContinuation>), ExecutionError>, imports PagingContinuation from scylla::client::paging_continuation, and calls LoadBalancingPolicy::is_coordinator_preferred with RoutingInfo, ClusterState, and Coordinator to obtain bool."
    },
    {
      "concerns": [
        "internal_coupling"
      ],
      "evidence": "The public path and opacity are prompt-stated, but the assertion specifically accepts only rustdoc's `plain` struct form. Refutation battery: searched the problem text for “PagingContinuation”, “opaque”, “struct”, “plain”, and “fields”; it names the type and opacity but never says named-field/plain struct. Searched the repo for `Continuation`, `opaque`, `has_stripped_fields`, `pub struct PagingState`, and `pub enum PagingState` across source/tests/docs. There is no continuation convention or rustdoc-shape checker; the closest visible paging abstraction is the equally valid opaque tuple struct `pub struct PagingState(Option<Arc<[u8]>>)` at scylla-cql-core/src/frame/request/query.rs:57-63. A solver could naturally implement `pub struct PagingContinuation(PagingState, Coordinator);`, satisfying the public path, hidden representation, and required contents, but rustdoc reports tuple rather than plain and the checker rejects it. Thus the hidden test pins the author's representation choice.",
      "fairness": "Not fair",
      "name": "paging_continuation_representation_is_opaque",
      "qualityCheck": "The no-public-fields and nonempty-private-representation checks are appropriate opacity checks. Requiring rustdoc `plain` rather than accepting an opaque tuple struct is unnecessary representation coupling.",
      "verifies": "The public type can be passed as Option<PagingContinuation>. In addition, the rustdoc checker requires exactly one public item at scylla::client::paging_continuation::PagingContinuation, requires its rustdoc kind to be a plain (named-field) struct, requires no public fields, and requires at least one stripped private representation field."
    }
  ],
  "unfairTestCount": 1,
  "verdict": "FAIL"
}
Close
