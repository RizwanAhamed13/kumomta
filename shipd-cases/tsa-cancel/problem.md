
Add a supported way to cancel an active action created by the Traffic Shaping Automation daemon (TSA).

The public HTTP operation is `DELETE /cancel_rule_v1`. It accepts JSON with a string `rule_hash` containing the full applied-action hash, including site names that contain hyphens. TSA suspension and bounce records expose this value in their `rule_hash` field. The TOML returned by `GET /get_config_v1` must expose the same cancellable identity for every active configuration override with a `# rule_hash: <full-rule-hash>` line in the comment block preceding that override's option. Malformed hashes must return HTTP 400, and a valid hash with no active action must return HTTP 404. A successful HTTP 200 response is JSON with `rule_hash`, numeric `config_overrides`, `ready_q_suspensions`, `scheduled_q_suspensions`, and `scheduled_q_bounces`, plus the `suppress_until` timestamp. Repeating an active cancellation must be safe and idempotent.

Cancellation must remove every active effect associated with that hash. It must be persisted across TSA restart and suppress delayed or replayed log records for the canceled action until the latest removed effect would have expired. A changed rule must receive a different hash and remain eligible to apply immediately.

The generic TSA websocket stream must delimit its initial snapshot with externally serialized `SnapshotStart` and `SnapshotEnd` items and publish cancellations as `RuleCancellation` items containing `rule_hash` and `suppress_until`.


Authorize the trusted HTTP-listener group to invoke `DELETE /cancel_rule_v1` in the default ACL configuration.
