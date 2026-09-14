# Review v2 dispositions

Artifact hashes at intake:

- `problem.md`: `46f5d1abaa9e548e95bb9a9ee63f480671c42c37d3e690e4816d031ae72db35c`
- `test.patch`: `273cad6ad65fe8c4f78e588c4cbe1bde872c7e2ead75dcd06c2dd7d716be5886`
- `solution.patch`: `b6d0d28f9d56367b4559bc29612f0ce16a0935bfa728df9f84f0db4fa394658b`
- `Dockerfile`: `ee8e4fc4c84a9df9ded752c4e5d6b020b1c794383f84182e04a224979eac9ef6`

| Finding | Classification | Disposition |
|---|---|---|
| Unsupported binding/pattern/type contribution | Prompt-stated test gap and golden bug | Restrict ordinary fan-out to expression paths, dot access, and record-literal fields; test negative binding/pattern/type-only labels in the existing mixed-context scenario. |
| Token-start edit application | Prompt-stated test gap | Extend the boundary scenario with normal and raw `check_edit` assertions. |
| Generic ordinary interior identifier | Prompt-stated test gap | Add `fi$0eld` to the existing boundary matrix. |
| String first-site identity | Repository-preservation test gap | Strengthen the existing helper to require `capture_first` and reject `capture_second`. |
| Lifetime first-site identity | Repository-preservation test gap | Strengthen the existing helper to require `'first` and reject `'second`. |
| Positive underscore behavior | Repository-preservation test gap | Add an expression-only baseline and expression-first repeated mapping to the existing helper; reject type/pattern-only labels. |
| Nested and enclosing-attribute expression route | Prompt-stated test gap | Extend the existing nested and attribute-nested record scenarios with an expression occurrence. |
| Broad `Name`/`NameRef` reference filter | Golden bug | Filter by public syntactic role; preserve the separate `(` visibility path. |

No prompt expansion is required. The description remains unchanged. The logical test count remains 29 because existing scenarios are strengthened.

The previously preserved Nova 10 patch must be replayed on the new exact bytes. A failure caused by unsupported-context leakage is a real mismatch with the narrowed current prompt, not permission to weaken the discriminator. At least one conformant saved or fresh solver must pass before readiness; zero durable solves is not acceptable.
