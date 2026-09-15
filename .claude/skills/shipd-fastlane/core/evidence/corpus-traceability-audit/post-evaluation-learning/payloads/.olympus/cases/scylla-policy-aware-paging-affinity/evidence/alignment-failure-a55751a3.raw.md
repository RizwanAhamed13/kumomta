# Problem and tests are aligned (AI, up to 1 min)

Failed

Your problem description says policies should explicitly decide coordinator eligibility and plans should support an optional preferred target, but the tests expect exact public interfaces that are not specified; please update the description with explicit Test Assumptions:

1. Interface information [ERROR]: Tests require these specific interfaces and paths:
   - trait method: `scylla::policies::load_balancing::LoadBalancingPolicy::is_coordinator_preferred(&self, routing: &scylla::policies::load_balancing::RoutingInfo, cluster: &scylla::cluster::ClusterState, coordinator: &scylla::response::Coordinator) -> bool`
   - constructor/helper: `scylla::policies::load_balancing::Plan::new_with_preferred_target(policy: &dyn LoadBalancingPolicy, routing: &RoutingInfo, cluster: &ClusterState, preferred: Option<(scylla::cluster::NodeRef, Option<scylla::routing::Shard>)>) -> Plan`
   These names, signatures, module paths, and parameter types should be stated so implementers can match the tests.
2. Behaviors [OK]: The high-level behaviors in the problem statement agree with what the tests imply (explicit coordinator eligibility decision by the policy and plan construction with an optional preferred target).
