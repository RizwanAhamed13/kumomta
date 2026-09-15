# Review 27 repair

- Execution host: `codespaces-14482c`
- Repository commit: `611d43b595fb0ad7010f2bdbd887acae3d962d65`
- Solved worktree: `/tmp/olympus-scylla-v27c-solved`
- Test-only worktree: `/tmp/olympus-scylla-v27b-testonly`
- Artifact set: `6344947a8687f991bc5fb6fa085854e42169bd4900129866c0e7762470e621a8`
- Test patch SHA-256: `b1002dc2b999f9a7949fc611aaea64b53b45db9d6f340c0130f89df0d0144701`

The test patch now materializes its cfg-gated fixture support at patch-application time. `test.sh` no longer invokes an installer or rewrites production sources. The solved `new` suite also passed with the complete checkout made read-only.

Speculative execution no longer depends on a fixed delayed response. The selected proxy rule deterministically drops the primary matching request, the other node responds immediately, and a zero speculative interval starts the fallback. Both pages retain exact four-attempt and one-fiber-per-request assertions.

Four-state result:

- Unsolved base: 1/1 pass.
- Unsolved new: 0/13 pass, 13 expected failures.
- Solved base: 1/1 pass.
- Solved new: 13/13 pass, no failures, errors, or skips.
- Read-only solved new: 13/13 pass.

The exact test patch applies cleanly after the reference solution and after saved genuine Nova patches 2, 4, 6, 8, and 9. Hosted checks tied to earlier artifact bytes remain stale.
